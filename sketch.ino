#include <WiFi.h>
#include <PubSubClient.h>

// WiFi de Wokwi
const char* ssid = "Wokwi-GUEST";
const char* pass = "";

// MQTT
const char* mqtt_server = "broker.hivemq.com";
const char* topic_state = "eafit/camilo/smartlight/state";
const char* topic_cmd   = "eafit/camilo/smartlight/commands";

WiFiClient espClient;
PubSubClient client(espClient);

// Pines LED
const int PIN_SALA = 26;
const int PIN_COC  = 27;
const int PIN_HAB  = 25;

bool sala=false, cocina=false, habitacion=false;

void applyScene(const String& s){
  if (s == "noche")      { sala=false; cocina=false; habitacion=true; }
  else if (s == "trabajo"){ sala=true;  cocina=true;  habitacion=false; }
  else if (s == "todo_on"){ sala=true;  cocina=true;  habitacion=true; }
  else if (s == "todo_off"){sala=false; cocina=false; habitacion=false; }
}

void callback(char* topic, byte* payload, unsigned int length) {
  String msg; for (unsigned int i=0; i<length; i++) msg += (char)payload[i];
  // Muy simple (buscar substrings)
  if (msg.indexOf("\"sala\":true")  >= 0) sala = true;
  if (msg.indexOf("\"sala\":false") >= 0) sala = false;
  if (msg.indexOf("\"cocina\":true")  >= 0) cocina = true;
  if (msg.indexOf("\"cocina\":false") >= 0) cocina = false;
  if (msg.indexOf("\"habitacion\":true")  >= 0) habitacion = true;
  if (msg.indexOf("\"habitacion\":false") >= 0) habitacion = false;
  // Escena (opcional si mandas {"escena":"noche"})
  int i = msg.indexOf("\"escena\":\"");
  if (i >= 0) {
    int j = msg.indexOf("\"", i+10);
    if (j > i) applyScene(msg.substring(i+10, j));
  }
}

void reconnect() {
  while (!client.connected()) {
    if (client.connect("smartlight_esp32")) { client.subscribe(topic_cmd); }
    else { delay(1000); }
  }
}

void setup() {
  pinMode(PIN_SALA, OUTPUT); pinMode(PIN_COC, OUTPUT); pinMode(PIN_HAB, OUTPUT);
  WiFi.begin(ssid, pass); while (WiFi.status() != WL_CONNECTED) delay(200);
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) reconnect();
  client.loop();

  digitalWrite(PIN_SALA, sala ? HIGH : LOW);
  digitalWrite(PIN_COC, cocina ? HIGH : LOW);
  digitalWrite(PIN_HAB, habitacion ? HIGH : LOW);

  char payload[96];
  snprintf(payload, sizeof(payload), "{\"sala\":%s,\"cocina\":%s,\"habitacion\":%s}",
           sala?"true":"false", cocina?"true":"false", habitacion?"true":"false");
  client.publish(topic_state, payload);
  delay(1500);
}
