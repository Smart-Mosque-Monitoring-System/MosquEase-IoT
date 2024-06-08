#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <WiFi.h>
#include <HTTPClient.h>

// Replace with your network credentials
const char* ssid = "realme 9 Pro 5G";
const char* password = "z833cw4w";

// Replace with your Supabase details
const char* supabase_url = "https://gwyyixagttragoezrbub.supabase.co/rest/v1/bme280";
const char* supabase_api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd3eXlpeGFndHRyYWdvZXpyYnViIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTc4Njg3MzEsImV4cCI6MjAzMzQ0NDczMX0.52qJhOCoGnNFxLwArSj0C1CXV4CcptpIAphwsUEzc4k";

// Create an instance of the BME280 sensor
Adafruit_BME280 bme; // I2C

hw_timer_t *timer = NULL;

// Function declaration
void IRAM_ATTR onTimer();

void setup() {
  Serial.begin(115200);
  
  // Initialize the BME280 sensor
  if (!bme.begin(0x76)) {
    Serial.println("Could not find a valid BME280 sensor, check wiring!");
    while (1);
  }

  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // // Set up a timer to send data every 10 seconds
  // timer = timerBegin(0, 80, true);
  // timerAttachInterrupt(timer, &onTimer, true);
  // timerAlarmWrite(timer, 10 * 1000000, true);
  // timerAlarmEnable(timer);
}

void loop() {
  // Read temperature and humidity from the BME280 sensor
  float temperature = bme.readTemperature();
  float humidity = bme.readHumidity();

  // Create the JSON payload
  String jsonPayload = "{\"temperature\":" + String(temperature, 2) + ", \"humidity\":" + String(humidity, 2) + ", \"mosque_id\":1}";

  // Send the data to Supabase
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(supabase_url);
    http.addHeader("Content-Type", "application/json");
    http.addHeader("apikey", supabase_api_key);
    http.addHeader("Authorization", "Bearer " + String(supabase_api_key));

    int httpResponseCode = http.POST(jsonPayload);
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  } else {
    Serial.println("Error in WiFi connection");
  }
  
  delay(10000);
}