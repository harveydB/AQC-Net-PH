
#include <HTTPClient.h>
#include <WiFi.h>
#include "ThingsBoard.h"
#include <SDS011.h>


// "GlobeAtHome_E1B42" //wifi ssid
//"4D9FAEC1" //wifi password
// "04FA_d0a168" //wifi ssid
// "keyboard4life" //wifi password
#define WIFI_AP             "GlobeAtHome_E1B42" //wifi ssid
#define WIFI_PASSWORD       "4D9FAEC1" //wifi password

// See https://thingsboard.io/docs/getting-started-guides/helloworld/
// to understand how to obtain an access token
#define TOKEN               "b7irT7ykdO4OGTGnyctt"
#define THINGSBOARD_SERVER  "thingsboard.cloud"

// Baud rate for debug serial
#define SERIAL_DEBUG_BAUD   115200
float p10,p25,totalp10,totalp25,BP_hi,BP_lo,I_hi,I_lo;
int error,i,counter,Ip;
unsigned Hour = 0;
unsigned Minute = 0;
unsigned long TimeOfLastMinute = 0;
SDS011 my_sds;
HTTPClient httpClient;
// Initialize ThingsBoard client
WiFiClient espClient;
// Initialize ThingsBoard instance
ThingsBoard tb(espClient);
// the Wifi radio's status
int status = WL_IDLE_STATUS;

void setup() {
  // initialize serial for debugging
  my_sds.begin(14,12);
  Serial.begin(SERIAL_DEBUG_BAUD);
  WiFi.begin(WIFI_AP, WIFI_PASSWORD);
  InitWiFi();
}

void loop() {
  //delay(1000);

  if (WiFi.status() != WL_CONNECTED) {
    reconnect();
  }

  if (!tb.connected()) {
    // Connect to the ThingsBoard
    Serial.print("Connecting to: ");
    Serial.print(THINGSBOARD_SERVER);
    Serial.print(" with token ");
    Serial.println(TOKEN);
    if (!tb.connect(THINGSBOARD_SERVER, TOKEN)) {
      Serial.println("Failed to connect");
      return;
    }
  }
  totalp10 = 0;
  totalp25 = 0;

  i = 1;
  while(i <= 1){
      error = my_sds.read(&p25,&p10);
      if (! error) {
        totalp10 = totalp10 + p10; 
        totalp25 = totalp25 + p25;
        Serial.println("Recording: " + String(i)+"th element");
        
        i = i + 1;
      }
      
      //delay(100);
  }

  Serial.println("PM2.5: "+ String(totalp25));
  Serial.println("PM10: "+ String(totalp10));

  Serial.println("Sending data...");

  // Uploads new telemetry to ThingsBoard using MQTT.
  // See https://thingsboard.io/docs/reference/mqtt-api/#telemetry-upload-api
  // for more details

  tb.sendTelemetryFloat("PM10 1-min", totalp10);
  tb.sendTelemetryFloat("PM2.5 1-min", totalp25);
  delay(30000);
  tb.loop();
}

void InitWiFi()
{
  Serial.println("Connecting to AP ...");
  // attempt to connect to WiFi network

  WiFi.begin(WIFI_AP, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connected to AP");
}

void reconnect() {
  // Loop until we're reconnected
  status = WiFi.status();
  if ( status != WL_CONNECTED) {
    WiFi.begin(WIFI_AP, WIFI_PASSWORD);
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
    Serial.println("Connected to AP");
  }
}
