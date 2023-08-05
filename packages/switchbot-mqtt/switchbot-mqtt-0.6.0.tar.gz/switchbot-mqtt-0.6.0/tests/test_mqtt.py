# switchbot-mqtt - MQTT client controlling SwitchBot button & curtain automators,
# compatible with home-assistant.io's MQTT Switch & Cover platform
#
# Copyright (C) 2020 Fabian Peter Hammerle <fabian@hammerle.me>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
import typing
import unittest.mock

import pytest
from paho.mqtt.client import MQTT_ERR_QUEUE_SIZE, MQTT_ERR_SUCCESS, MQTTMessage, Client

import switchbot_mqtt

# pylint: disable=protected-access


@pytest.mark.parametrize("mqtt_host", ["mqtt-broker.local"])
@pytest.mark.parametrize("mqtt_port", [1833])
def test__run(caplog, mqtt_host, mqtt_port):
    with unittest.mock.patch(
        "paho.mqtt.client.Client"
    ) as mqtt_client_mock, caplog.at_level(logging.DEBUG):
        switchbot_mqtt._run(
            mqtt_host=mqtt_host,
            mqtt_port=mqtt_port,
            mqtt_username=None,
            mqtt_password=None,
        )
    mqtt_client_mock.assert_called_once_with()
    assert not mqtt_client_mock().username_pw_set.called
    mqtt_client_mock().connect.assert_called_once_with(host=mqtt_host, port=mqtt_port)
    mqtt_client_mock().socket().getpeername.return_value = (mqtt_host, mqtt_port)
    with caplog.at_level(logging.DEBUG):
        mqtt_client_mock().on_connect(mqtt_client_mock(), None, {}, 0)
    assert mqtt_client_mock().subscribe.call_args_list == [
        unittest.mock.call("homeassistant/switch/switchbot/+/set"),
        unittest.mock.call("homeassistant/cover/switchbot-curtain/+/set"),
    ]
    assert mqtt_client_mock().message_callback_add.call_args_list == [
        unittest.mock.call(
            sub="homeassistant/switch/switchbot/+/set",
            callback=switchbot_mqtt._ButtonAutomator._mqtt_command_callback,
        ),
        unittest.mock.call(
            sub="homeassistant/cover/switchbot-curtain/+/set",
            callback=switchbot_mqtt._CurtainMotor._mqtt_command_callback,
        ),
    ]
    mqtt_client_mock().loop_forever.assert_called_once_with()
    assert caplog.record_tuples == [
        (
            "switchbot_mqtt",
            logging.INFO,
            "connecting to MQTT broker {}:{}".format(mqtt_host, mqtt_port),
        ),
        (
            "switchbot_mqtt",
            logging.DEBUG,
            "connected to MQTT broker {}:{}".format(mqtt_host, mqtt_port),
        ),
        (
            "switchbot_mqtt",
            logging.INFO,
            "subscribing to MQTT topic 'homeassistant/switch/switchbot/+/set'",
        ),
        (
            "switchbot_mqtt",
            logging.INFO,
            "subscribing to MQTT topic 'homeassistant/cover/switchbot-curtain/+/set'",
        ),
    ]


@pytest.mark.parametrize("mqtt_host", ["mqtt-broker.local"])
@pytest.mark.parametrize("mqtt_port", [1833])
@pytest.mark.parametrize("mqtt_username", ["me"])
@pytest.mark.parametrize("mqtt_password", [None, "secret"])
def test__run_authentication(mqtt_host, mqtt_port, mqtt_username, mqtt_password):
    with unittest.mock.patch("paho.mqtt.client.Client") as mqtt_client_mock:
        switchbot_mqtt._run(
            mqtt_host=mqtt_host,
            mqtt_port=mqtt_port,
            mqtt_username=mqtt_username,
            mqtt_password=mqtt_password,
        )
    mqtt_client_mock.assert_called_once_with()
    mqtt_client_mock().username_pw_set.assert_called_once_with(
        username=mqtt_username, password=mqtt_password
    )


@pytest.mark.parametrize("mqtt_host", ["mqtt-broker.local"])
@pytest.mark.parametrize("mqtt_port", [1833])
@pytest.mark.parametrize("mqtt_password", ["secret"])
def test__run_authentication_missing_username(mqtt_host, mqtt_port, mqtt_password):
    with unittest.mock.patch("paho.mqtt.client.Client"):
        with pytest.raises(ValueError):
            switchbot_mqtt._run(
                mqtt_host=mqtt_host,
                mqtt_port=mqtt_port,
                mqtt_username=None,
                mqtt_password=mqtt_password,
            )


@pytest.mark.parametrize(
    ("command_topic_levels", "topic", "payload", "expected_mac_address"),
    [
        (
            switchbot_mqtt._ButtonAutomator.MQTT_COMMAND_TOPIC_LEVELS,
            b"homeassistant/switch/switchbot/aa:bb:cc:dd:ee:ff/set",
            b"ON",
            "aa:bb:cc:dd:ee:ff",
        ),
        (
            switchbot_mqtt._ButtonAutomator.MQTT_COMMAND_TOPIC_LEVELS,
            b"homeassistant/switch/switchbot/aa:bb:cc:dd:ee:ff/set",
            b"OFF",
            "aa:bb:cc:dd:ee:ff",
        ),
        (
            switchbot_mqtt._ButtonAutomator.MQTT_COMMAND_TOPIC_LEVELS,
            b"homeassistant/switch/switchbot/aa:bb:cc:dd:ee:ff/set",
            b"on",
            "aa:bb:cc:dd:ee:ff",
        ),
        (
            switchbot_mqtt._ButtonAutomator.MQTT_COMMAND_TOPIC_LEVELS,
            b"homeassistant/switch/switchbot/aa:bb:cc:dd:ee:ff/set",
            b"off",
            "aa:bb:cc:dd:ee:ff",
        ),
        (
            switchbot_mqtt._ButtonAutomator.MQTT_COMMAND_TOPIC_LEVELS,
            b"homeassistant/switch/switchbot/aa:01:23:45:67:89/set",
            b"ON",
            "aa:01:23:45:67:89",
        ),
        (
            ["switchbot", switchbot_mqtt._MQTTTopicPlaceholder.MAC_ADDRESS],
            b"switchbot/aa:01:23:45:67:89",
            b"ON",
            "aa:01:23:45:67:89",
        ),
        (
            switchbot_mqtt._CurtainMotor.MQTT_COMMAND_TOPIC_LEVELS,
            b"homeassistant/cover/switchbot-curtain/aa:01:23:45:67:89/set",
            b"OPEN",
            "aa:01:23:45:67:89",
        ),
    ],
)
def test__mqtt_command_callback(
    caplog,
    command_topic_levels: typing.List[switchbot_mqtt._MQTTTopicLevel],
    topic: bytes,
    payload: bytes,
    expected_mac_address: str,
):
    class _ActorMock(switchbot_mqtt._MQTTControlledActor):
        MQTT_COMMAND_TOPIC_LEVELS = command_topic_levels

        def __init__(self, mac_address):
            super().__init__(mac_address=mac_address)

        def execute_command(self, mqtt_message_payload: bytes, mqtt_client: Client):
            pass

    message = MQTTMessage(topic=topic)
    message.payload = payload
    with unittest.mock.patch.object(
        _ActorMock, "__init__", return_value=None
    ) as init_mock, unittest.mock.patch.object(
        _ActorMock, "execute_command"
    ) as execute_command_mock, caplog.at_level(
        logging.DEBUG
    ):
        _ActorMock._mqtt_command_callback("client_dummy", None, message)
    init_mock.assert_called_once_with(mac_address=expected_mac_address)
    execute_command_mock.assert_called_once_with(
        mqtt_client="client_dummy", mqtt_message_payload=payload
    )
    assert caplog.record_tuples == [
        (
            "switchbot_mqtt",
            logging.DEBUG,
            "received topic={} payload={!r}".format(topic.decode(), payload),
        )
    ]


@pytest.mark.parametrize(
    ("topic", "payload"),
    [
        (b"homeassistant/switch/switchbot/aa:bb:cc:dd:ee:ff", b"on"),
        (b"homeassistant/switch/switchbot/aa:bb:cc:dd:ee:ff/change", b"ON"),
        (b"homeassistant/switch/switchbot/aa:bb:cc:dd:ee:ff/set/suffix", b"ON"),
    ],
)
def test__mqtt_command_callback_unexpected_topic(caplog, topic: bytes, payload: bytes):
    class _ActorMock(switchbot_mqtt._MQTTControlledActor):
        MQTT_COMMAND_TOPIC_LEVELS = (
            switchbot_mqtt._ButtonAutomator.MQTT_COMMAND_TOPIC_LEVELS
        )

        def __init__(self, mac_address):
            super().__init__(mac_address=mac_address)

        def execute_command(self, mqtt_message_payload: bytes, mqtt_client: Client):
            pass

    message = MQTTMessage(topic=topic)
    message.payload = payload
    with unittest.mock.patch.object(
        _ActorMock, "__init__", return_value=None
    ) as init_mock, unittest.mock.patch.object(
        _ActorMock, "execute_command"
    ) as execute_command_mock, caplog.at_level(
        logging.DEBUG
    ):
        _ActorMock._mqtt_command_callback("client_dummy", None, message)
    init_mock.assert_not_called()
    execute_command_mock.assert_not_called()
    assert caplog.record_tuples == [
        (
            "switchbot_mqtt",
            logging.DEBUG,
            "received topic={} payload={!r}".format(topic.decode(), payload),
        ),
        (
            "switchbot_mqtt",
            logging.WARNING,
            "unexpected topic {}".format(topic.decode()),
        ),
    ]


@pytest.mark.parametrize(("mac_address", "payload"), [("aa:01:23:4E:RR:OR", b"ON")])
def test__mqtt_command_callback_invalid_mac_address(
    caplog, mac_address: str, payload: bytes
):
    class _ActorMock(switchbot_mqtt._MQTTControlledActor):
        MQTT_COMMAND_TOPIC_LEVELS = (
            switchbot_mqtt._ButtonAutomator.MQTT_COMMAND_TOPIC_LEVELS
        )

        def __init__(self, mac_address):
            super().__init__(mac_address=mac_address)

        def execute_command(self, mqtt_message_payload: bytes, mqtt_client: Client):
            pass

    topic = "homeassistant/switch/switchbot/{}/set".format(mac_address).encode()
    message = MQTTMessage(topic=topic)
    message.payload = payload
    with unittest.mock.patch.object(
        _ActorMock, "__init__", return_value=None
    ) as init_mock, unittest.mock.patch.object(
        _ActorMock, "execute_command"
    ) as execute_command_mock, caplog.at_level(
        logging.DEBUG
    ):
        _ActorMock._mqtt_command_callback("client_dummy", None, message)
    init_mock.assert_not_called()
    execute_command_mock.assert_not_called()
    assert caplog.record_tuples == [
        (
            "switchbot_mqtt",
            logging.DEBUG,
            "received topic={} payload={!r}".format(topic.decode(), payload),
        ),
        (
            "switchbot_mqtt",
            logging.WARNING,
            "invalid mac address {}".format(mac_address),
        ),
    ]


@pytest.mark.parametrize(
    ("topic", "payload"),
    [(b"homeassistant/switch/switchbot/aa:bb:cc:dd:ee:ff/set", b"ON")],
)
def test__mqtt_command_callback_ignore_retained(caplog, topic: bytes, payload: bytes):
    class _ActorMock(switchbot_mqtt._MQTTControlledActor):
        MQTT_COMMAND_TOPIC_LEVELS = (
            switchbot_mqtt._ButtonAutomator.MQTT_COMMAND_TOPIC_LEVELS
        )

        def __init__(self, mac_address):
            super().__init__(mac_address=mac_address)

        def execute_command(self, mqtt_message_payload: bytes, mqtt_client: Client):
            pass

    message = MQTTMessage(topic=topic)
    message.payload = payload
    message.retain = True
    with unittest.mock.patch.object(
        _ActorMock, "__init__", return_value=None
    ) as init_mock, unittest.mock.patch.object(
        _ActorMock, "execute_command"
    ) as execute_command_mock, caplog.at_level(
        logging.DEBUG
    ):
        _ActorMock._mqtt_command_callback("client_dummy", None, message)
    init_mock.assert_not_called()
    execute_command_mock.assert_not_called()
    assert caplog.record_tuples == [
        (
            "switchbot_mqtt",
            logging.DEBUG,
            "received topic={} payload={!r}".format(topic.decode(), payload),
        ),
        ("switchbot_mqtt", logging.INFO, "ignoring retained message"),
    ]


@pytest.mark.parametrize(
    ("state_topic_levels", "mac_address", "expected_topic"),
    # https://www.home-assistant.io/docs/mqtt/discovery/#switches
    [
        (
            switchbot_mqtt._ButtonAutomator.MQTT_STATE_TOPIC_LEVELS,
            "aa:bb:cc:dd:ee:ff",
            "homeassistant/switch/switchbot/aa:bb:cc:dd:ee:ff/state",
        ),
        (
            ["switchbot", switchbot_mqtt._MQTTTopicPlaceholder.MAC_ADDRESS, "state"],
            "aa:bb:cc:dd:ee:gg",
            "switchbot/aa:bb:cc:dd:ee:gg/state",
        ),
    ],
)
@pytest.mark.parametrize("state", [b"ON", b"CLOSE"])
@pytest.mark.parametrize("return_code", [MQTT_ERR_SUCCESS, MQTT_ERR_QUEUE_SIZE])
def test__report_state(
    caplog,
    state_topic_levels: typing.List[switchbot_mqtt._MQTTTopicLevel],
    mac_address: str,
    expected_topic: str,
    state: bytes,
    return_code: int,
):
    # pylint: disable=too-many-arguments
    class _ActorMock(switchbot_mqtt._MQTTControlledActor):
        MQTT_STATE_TOPIC_LEVELS = state_topic_levels

        def __init__(self, mac_address):
            super().__init__(mac_address=mac_address)

        def execute_command(self, mqtt_message_payload: bytes, mqtt_client: Client):
            pass

    mqtt_client_mock = unittest.mock.MagicMock()
    mqtt_client_mock.publish.return_value.rc = return_code
    with caplog.at_level(logging.DEBUG):
        _ActorMock(mac_address=mac_address).report_state(
            state=state, mqtt_client=mqtt_client_mock
        )
    mqtt_client_mock.publish.assert_called_once_with(
        topic=expected_topic, payload=state, retain=True
    )
    assert caplog.record_tuples[0] == (
        "switchbot_mqtt",
        logging.DEBUG,
        "publishing topic={} payload={!r}".format(expected_topic, state),
    )
    if return_code == MQTT_ERR_SUCCESS:
        assert not caplog.records[1:]
    else:
        assert caplog.record_tuples[1:] == [
            (
                "switchbot_mqtt",
                logging.ERROR,
                "failed to publish state (rc={})".format(return_code),
            )
        ]
