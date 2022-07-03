#include <WiFi.h>
#include <SDS011.h>

const char* ssid     = "GlobeAtHome_E1B42";
const char* password = "4D9FAEC1";
const char* ssid2 = "Kapeng Barako";
const char* password2 = "coffee4life";
float p10,p25,totalp10,totalp25,BP_hi,BP_lo,I_hi,I_lo;
int error,i,counter,Ip,AQI_PM10,AQI_PM25,cat;
SDS011 my_sds;
WiFiServer server(80);

int AQI_cat(int AQI){
  int cat;
  if ( AQI <= 50 ){
    cat = 0;
    return cat;
  } else if ( AQI <= 100) {
    cat = 1;
    return cat;
  } else if ( AQI <= 150) {
    cat = 2;
    return cat;
  } else if ( AQI <= 200) {
    cat = 3;
    return cat;
  } else if ( AQI <= 250) {
    cat = 4;
    return cat;
  } else {
    cat = 5;
    return cat;
  }
}
int AQI_Calc_PM10(float p10){
  if ( p10 <= 54 ){
    //Good
     BP_hi = 54;
     BP_lo = 0;
     I_hi = 50; 
     I_lo = 0; 
  } else if ( p10 <= 154 ){
    //Moderate
     BP_hi = 154;
     BP_lo = 55;
     I_hi = 100; 
     I_lo = 51; 
  } else if ( p10 <= 254 ){
    //Unhealty for Sensitive
     BP_hi = 254;
     BP_lo = 155;
     I_hi = 150; 
     I_lo = 101; 
  } else if ( p10 <= 354 ){
    //Unhealthy
     BP_hi = 354;
     BP_lo = 255;
     I_hi = 200; 
     I_lo = 151; 
  } else if ( p10 <= 424 ){
    //Very Unhealthy
     BP_hi = 424;
     BP_lo = 355;
     I_hi = 201; 
     I_lo = 300; 
  } else if ( p10 <= 504 ){
    //Hazardous
     BP_hi = 504;
     BP_lo = 425;
     I_hi = 400; 
     I_lo = 301; 
  } else if ( p10 <= 604 ){
    //Hazardous
     BP_hi = 604;
     BP_lo = 505;
     I_hi = 500; 
     I_lo = 401; 
  }
  Ip = trunc(((I_hi - I_lo) / (BP_hi - BP_lo)) * (trunc(p10) - BP_lo) + I_lo);
  return Ip;
}
int AQI_Calc_PM25(float p25){
  if ( p25 <= 12 ){
    //Good
     BP_hi = 12;
     BP_lo = 0;
     I_hi = 50; 
     I_lo = 0; 
  } else if ( p25 <= 35.4 ){
    //Moderate
     BP_hi = 35.4;
     BP_lo = 12.1;
     I_hi = 100; 
     I_lo = 51; 
  } else if ( p25 <= 55.4 ){
    //Unhealty for Sensitive
     BP_hi = 55.4;
     BP_lo = 35.5;
     I_hi = 150; 
     I_lo = 101; 
  } else if ( p25 <= 150.4 ){
    //Unhealthy
     BP_hi = 150.4;
     BP_lo = 55.5;
     I_hi = 200; 
     I_lo = 151; 
  } else if ( p25 <= 250.4 ){
    //Very Unhealthy
     BP_hi = 250.4;
     BP_lo = 150.5;
     I_hi = 201; 
     I_lo = 300; 
  } else if ( p25 <= 350.4 ){
    //Hazardous
     BP_hi = 350.4;
     BP_lo = 250.5;
     I_hi = 400; 
     I_lo = 301; 
  } else if ( p25 <= 500.4 ){
    //Hazardous
     BP_hi = 500.4;
     BP_lo = 350.5;
     I_hi = 500; 
     I_lo = 401; 
  }
  Ip = trunc(((I_hi - I_lo) / (BP_hi - BP_lo)) * (trunc(p25) - BP_lo) + I_lo);
  return Ip;
}
void setup()
{
    my_sds.begin(14,12);
    Serial.begin(115200);      // set the LED pin mode

    delay(10);

    // We start by connecting to a WiFi network

    Serial.println();
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("");
    Serial.println("WiFi connected.");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
    
    server.begin();

}

int value = 0;

void loop(){
 WiFiClient client = server.available();   // listen for incoming clients
  totalp10 = 0;
  totalp25 = 0;
  i = 1;
  if (client) {                             // if you get a client,
    Serial.println("New Client.");           // print a message out the serial port
    String currentLine = "";                // make a String to hold incoming data from the client
    while (client.connected()) {            // loop while the client's connected
      if (client.available()) {             // if there's bytes to read from the client,
        char c = client.read();             // read a byte, then
        Serial.write(c);                    // print it out the serial monitor
        if (c == '\n') {                    // if the byte is a newline character

          // if the current line is blank, you got two newline characters in a row.
          // that's the end of the client HTTP request, so send a response:
          if (currentLine.length() == 0) {
            // HTTP headers always start with a response code (e.g. HTTP/1.1 200 OK)
            // and a content-type so the client knows what's coming, then a blank line:
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println();
            client.println("Click <a href=\"/H\">here</a> to update PM reading.<br>");
            client.println();
            // break out of the while loop:
            break;
          } else {    // if you got a newline, then clear currentLine:
            currentLine = "";
          }
        } else if (c != '\r') {  // if you got anything else but a carriage return character,
          currentLine += c;      // add it to the end of the currentLine
        }

        
        if (currentLine.endsWith("GET /H")) {
          while(i <= 600){
            error = my_sds.read(&p25,&p10);
            if (! error) {
              totalp10 = totalp10 + p10;
              totalp25 = totalp25 + p25;
              Serial.println("Recording: " + String(i)+"th element");
              i = i + 1;
            }
      
            delay(100);
          }
          totalp10 = totalp10 / 600;
          totalp25 = totalp25/ 600;
          Serial.println("PM2.5: "+ String(totalp25));
          Serial.println("PM10: "+ String(totalp10));
          AQI_PM25 = AQI_Calc_PM25(totalp25);
          AQI_PM10 = AQI_Calc_PM10(totalp10);
          if (AQI_PM25 > AQI_PM10){
            cat = (AQI_cat(AQI_PM25));
            client.println("AQI category is: " + String(cat));
            client.println("PM2.5 AQI is :" + String(AQI_PM25));
            client.println("PM2.5: " + String(totalp25));
            client.println("PM10: " + String(totalp10));
            Serial.println("AQI category is: " + String(cat));
            Serial.println("PM2.5 AQI is :" + String(AQI_PM25));
            Serial.println("PM2.5: " + String(totalp25));
            Serial.println("PM10: " + String(totalp10));
          } else {
            cat = (AQI_cat(AQI_PM10));
            client.println("AQI category is: " + String(cat));
            client.println("PM10 AQI is :" + String(AQI_PM10));
            client.println("PM2.5: " + String(totalp25));
            client.println("PM10: " + String(totalp10));
            Serial.println("AQI category is: " + String(cat));
            Serial.println("PM10 AQI is :" + String(AQI_PM10));
            Serial.println("PM2.5: " + String(totalp25));
            Serial.println("PM10: " + String(totalp10));
          }
            break;     
          }

      }
    }
    // close the connection:
    client.stop();
    Serial.println("Client Disconnected.");
  }
}
