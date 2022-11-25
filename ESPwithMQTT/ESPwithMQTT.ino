#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN D8
#define RST_PIN D0
#define RESISTOR_PIN A0

const char* ssid = "Wee Fee";
const char* password = "Pr1cel3$$";

const char* mqtt_server = "192.168.2.141";

WiFiClient vanieriot;
PubSubClient client(vanieriot);

MFRC522 rfid(SS_PIN, RST_PIN);
MFRC522::MIFARE_Key key;
byte nuidPICC[4];


void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("WiFi connected - ESP-8266 IP address: ");
  Serial.println(WiFi.localIP());
}


void callback(String topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messagein;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messagein += (char)message[i];
  }
}


void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
 
    // Attempt to connect
           if (client.connect("vanieriot")) {

      Serial.println("connected");  
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}


void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  pinMode(RESISTOR_PIN, INPUT);
  SPI.begin();
  rfid.PCD_Init();
}

void loop() {
  if (!client.connected())
    reconnect();
  if(!client.loop())
    client.connect("vanieriot");

  light_read();
  rfid_read();
  delay(1500);
}

void light_read() {
  float intensity = analogRead(RESISTOR_PIN);

  char intensityArr [8];
  dtostrf(intensity,4,2,intensityArr);
  Serial.println(intensity);
    
  client.publish("/IoTlab/lightIntensity", intensityArr);
}

void rfid_read() {
  if ( ! rfid.PICC_IsNewCardPresent())
    return;

  // Verify if the NUID has been readed
  if ( ! rfid.PICC_ReadCardSerial())
    return;

  MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);
  if (piccType != MFRC522::PICC_TYPE_MIFARE_MINI &&
    piccType != MFRC522::PICC_TYPE_MIFARE_1K &&
    piccType != MFRC522::PICC_TYPE_MIFARE_4K) {
    return;
  }
  if (rfid.uid.uidByte[0] != nuidPICC[0] ||
    rfid.uid.uidByte[1] != nuidPICC[1] ||
    rfid.uid.uidByte[2] != nuidPICC[2] ||
    rfid.uid.uidByte[3] != nuidPICC[3] ) {
    for (byte i = 0; i < 4; i++) {
      nuidPICC[i] = rfid.uid.uidByte[i];
    }
    getHex(rfid.uid.uidByte, rfid.uid.size);
  }
}

void getHex(byte *buffer, byte bufferSize) {
  String hexValue = "";
  for (byte i = 0; i < bufferSize; i++) {
    hexValue += buffer[i] < 0x10 ? " 0" : " ";
    hexValue += String(buffer[i], HEX);
  }
  char rfidVal [hexValue.length() + 1];
  hexValue.toCharArray(rfidVal, hexValue.length() + 1);
  Serial.println(rfidVal);
  client.publish("/IoTlab/rfidVals", rfidVal);
}