#include <DHT.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

// ==========================================
// DHT11 CONFIGURATION
// ==========================================

#define DHT_PIN D2
#define DHT_TYPE DHT11

DHT dht(DHT_PIN, DHT_TYPE);

// ==========================================
// SOIL SENSOR CONFIGURATION
// ==========================================

#define SOIL_PIN A0

// ==========================================
// WI-FI CONFIGURATION
// ==========================================

const char* WIFI_SSID = "YOUR_WIFI_SSID";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

// ==========================================
// THINGSPEAK CONFIGURATION
// ==========================================

const char* THINGSPEAK_URL =
  "http://api.thingspeak.com/update";

const char* THINGSPEAK_WRITE_API_KEY =
  "YOUR_THINGSPEAK_WRITE_API_KEY";

// ==========================================
// SETUP
// ==========================================

void setup() {

  Serial.begin(115200);
  delay(1000);

  Serial.println();
  Serial.println("================================");
  Serial.println("          AgriSense AI");
  Serial.println("================================");

  // Start DHT11
  dht.begin();

  // ========================================
  // CONNECT TO WI-FI
  // ========================================

  Serial.println();
  Serial.print("Connecting to Wi-Fi");

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  while (WiFi.status() != WL_CONNECTED) {

    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("Wi-Fi Connected!");

  Serial.print("ESP8266 IP Address: ");
  Serial.println(WiFi.localIP());

  Serial.println("--------------------------------");
}

// ==========================================
// LOOP
// ==========================================

void loop() {

  // ========================================
  // READ DHT11
  // ========================================

  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  // ========================================
  // READ SOIL SENSOR
  // ========================================

  int soilRaw = analogRead(SOIL_PIN);

  // ========================================
  // CHECK DHT11
  // ========================================

  if (isnan(temperature) || isnan(humidity)) {

    Serial.println();
    Serial.println("ERROR: Failed to read DHT11!");

    delay(5000);
    return;
  }

  // ========================================
  // DISPLAY SENSOR DATA
  // ========================================

  Serial.println();

  Serial.print("Temperature : ");
  Serial.print(temperature);
  Serial.println(" °C");

  Serial.print("Humidity    : ");
  Serial.print(humidity);
  Serial.println(" %");

  Serial.print("Soil Raw    : ");
  Serial.println(soilRaw);

  // ========================================
  // CHECK WI-FI
  // ========================================

  if (WiFi.status() != WL_CONNECTED) {

    Serial.println();
    Serial.println("Wi-Fi disconnected!");
    Serial.println("Reconnecting...");

    WiFi.disconnect();
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    delay(5000);

    return;
  }

  // ========================================
  // SEND DATA TO THINGSPEAK
  // ========================================

  WiFiClient client;
  HTTPClient http;

  Serial.println();
  Serial.println("Sending data to ThingSpeak...");

  // Initialize HTTP connection
  if (!http.begin(client, THINGSPEAK_URL)) {

    Serial.println(
      "ERROR: Failed to initialize ThingSpeak connection!"
    );

    delay(5000);
    return;
  }

  // Content type
  http.addHeader(
    "Content-Type",
    "application/x-www-form-urlencoded"
  );

  // ========================================
  // CREATE THINGSPEAK DATA
  // ========================================

  String postData =
    "api_key=" + String(THINGSPEAK_WRITE_API_KEY) +
    "&field1=" + String(temperature, 2) +
    "&field2=" + String(humidity, 2) +
    "&field3=" + String(soilRaw);

  Serial.print("Data: ");
  Serial.println(postData);

  // ========================================
  // SEND POST REQUEST
  // ========================================

  int httpResponseCode = http.POST(postData);

  Serial.print("HTTP Response Code: ");
  Serial.println(httpResponseCode);

  // ========================================
  // PROCESS RESPONSE
  // ========================================

  if (httpResponseCode > 0) {

    String response = http.getString();

    Serial.print("ThingSpeak Response: ");
    Serial.println(response);

    if (httpResponseCode == 200) {

      Serial.println("SUCCESS: Sensor data uploaded!");

    } else {

      Serial.println(
        "WARNING: ThingSpeak returned an unexpected response."
      );
    }

  } else {

    Serial.println(
      "ERROR: Failed to connect to ThingSpeak."
    );
  }

  // Close connection
  http.end();

  Serial.println("--------------------------------");

  // ========================================
  // THINGSPEAK UPDATE INTERVAL
  // ========================================

  delay(20000);
}