// Arduino sketch for Kamila hardware interface
// Connect sensors and LED to Arduino pins

#define TEMP_SENSOR A0
#define TOUCH_SENSOR 2
#define LED_RED 9
#define LED_GREEN 10
#define LED_BLUE 11

void setup() {
  Serial.begin(9600);
  pinMode(TOUCH_SENSOR, INPUT);
  pinMode(LED_RED, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_BLUE, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "GET_TEMP") {
      int tempValue = analogRead(TEMP_SENSOR);
      float temperature = tempValue * (5.0 / 1023.0) * 100;  // Simple conversion
      Serial.println("TEMP:" + String(temperature));
    } else if (command == "GET_TOUCH") {
      int touchValue = digitalRead(TOUCH_SENSOR);
      if (touchValue == HIGH) {
        Serial.println("TOUCH_DETECTED");
      } else {
        Serial.println("NO_TOUCH");
      }
    } else if (command.startsWith("LED_")) {
      String color = command.substring(4);
      if (color == "RED") {
        digitalWrite(LED_RED, HIGH);
        digitalWrite(LED_GREEN, LOW);
        digitalWrite(LED_BLUE, LOW);
      } else if (color == "GREEN") {
        digitalWrite(LED_RED, LOW);
        digitalWrite(LED_GREEN, HIGH);
        digitalWrite(LED_BLUE, LOW);
      } else if (color == "BLUE") {
        digitalWrite(LED_RED, LOW);
        digitalWrite(LED_GREEN, LOW);
        digitalWrite(LED_BLUE, HIGH);
      } else if (color == "OFF") {
        digitalWrite(LED_RED, LOW);
        digitalWrite(LED_GREEN, LOW);
        digitalWrite(LED_BLUE, LOW);
      }
      Serial.println("LED_SET:" + color);
    }
  }
  delay(100);
}
