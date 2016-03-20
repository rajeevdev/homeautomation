/*
 *  This sketch sends data via HTTP GET requests to data.sparkfun.com service.
 *
 *  You need to get streamId and privateKey at data.sparkfun.com and paste them
 *  below. Or just customize this script to talk to other HTTP servers.
 *
 */

#include <ESP8266WiFi.h>

const char* ssid     = "mywifi";
const char* password = "mypassword";
const char* host     = "192.168.42.1";
const int port       = 9000;

WiFiClient client;

void setup() {
  Serial.begin(115200);
  delay(10);

  // prepare GPIO2
  pinMode(2, OUTPUT);
  digitalWrite(2, 1);

  pinMode(0, OUTPUT);
  digitalWrite(0, 1);

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
  Serial.println("WiFi connected");  
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // Use WiFiClient class to create TCP connections
  Serial.print("connecting to ");
  Serial.println(host);
  if (!client.connect(host, port)) {
    Serial.println("connection failed");
    return;
  }
  Serial.println("connected");
}

int value = 0;

void loop() {
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    ESP.reset();
    return;
  }

  if (!client.connected()) {
    Serial.println("Client disconnected");
    client.stop();
    Serial.print("Reconnecting to ");
    Serial.println(host);
    if (!client.connect(host, port)) {
      Serial.println("connection failed");
      delay(1000);
      return;
    }
    Serial.println("connected");
  }
  
  // Read all the lines of the reply from server and print them to Serial
  if (client.available()) {
    delay(500);
    String command = client.readStringUntil(']');
    Serial.println(command);
    client.flush();
    int gpio_val = -1;
    String reply;
    if (command.indexOf("[GET /moduleId") != -1) {
      byte mac[6];
      reply += "[/moduleId/";
      WiFi.macAddress(mac);
      reply += String(mac[0], HEX);
      reply += ":";
      reply += String(mac[1], HEX);
      reply += ":";
      reply += String(mac[2], HEX);
      reply += ":";
      reply += String(mac[3], HEX);
      reply += ":";
      reply += String(mac[4], HEX);
      reply += ":";
      reply += String(mac[5], HEX);
      reply += "]";
    }
    else if (command.indexOf("[GET /gpio0") != -1) {
      gpio_val = digitalRead(0);
      reply += "[/gpio0/";
      reply += ((gpio_val) ? "1]" : "0]");
    }
    else if (command.indexOf("[GET /gpio2") != -1) {
      gpio_val = digitalRead(2);
      reply += "[/gpio2/";
      reply += ((gpio_val) ? "1]" : "0]");
    }
    else if (command.indexOf("[SET /gpio0/0") != -1) {
      digitalWrite(0, 0);
      gpio_val = digitalRead(0);
      reply += "[/gpio0/";
      reply += ((gpio_val) ? "1]" : "0]");
    }
    else if (command.indexOf("[SET /gpio0/1") != -1) {
      digitalWrite(0, 1);
      gpio_val = digitalRead(0);
      reply += "[/gpio0/";
      reply += ((gpio_val) ? "1]" : "0]");
    }
    else if (command.indexOf("[SET /gpio2/0") != -1) {
      digitalWrite(2, 0);
      gpio_val = digitalRead(2);
      reply += "[/gpio2/";
      reply += ((gpio_val) ? "1]" : "0]");
    }
    else if (command.indexOf("[SET /gpio2/1") != -1) {
      digitalWrite(2, 1);
      gpio_val = digitalRead(2);
      reply += "[/gpio2/";
      reply += ((gpio_val) ? "1]" : "0]");
    }
    Serial.println(reply);
    client.print(reply);
    client.flush();
  }
}

