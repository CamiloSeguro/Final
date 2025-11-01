import json, time, threading, os
from typing import Callable, Optional
import paho.mqtt.client as mqtt

# Lee de entorno; usa HiveMQ por defecto
MQTT_BROKER = os.getenv("MQTT_BROKER", "broker.hivemq.com")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
KEEPALIVE = 60

class MqttBridge:
    def __init__(self, client_id: str):
        self.client = mqtt.Client(client_id=client_id, clean_session=True)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self._handlers = {}
        self._connected = False

    def _on_connect(self, c, u, f, rc):
        self._connected = True

    def _on_message(self, c, u, msg):
        handler: Optional[Callable[[str, dict], None]] = self._handlers.get(msg.topic)
        if handler:
            try:
                payload = json.loads(msg.payload.decode("utf-8"))
            except Exception:
                payload = {"raw": msg.payload.decode("utf-8", errors="ignore")}
            handler(msg.topic, payload)

    def connect(self):
        self.client.connect(MQTT_BROKER, MQTT_PORT, KEEPALIVE)
        threading.Thread(target=self.client.loop_forever, daemon=True).start()
        t0 = time.time()
        while not self._connected and time.time() - t0 < 3:
            time.sleep(0.05)

    def publish(self, topic: str, payload: dict):
        self.client.publish(topic, json.dumps(payload), qos=0, retain=False)

    def subscribe(self, topic: str, handler: Callable[[str, dict], None]):
        self._handlers[topic] = handler
        self.client.subscribe(topic, qos=0)
