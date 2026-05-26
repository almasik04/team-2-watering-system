#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 
#define SCREEN_HEIGHT 64 
#define OLED_RESET    -1 
#define SCREEN_ADDRESS 0x3C 

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

enum SystemState {
  STATE_IDLE,       
  STATE_WATERING,   
  STATE_ERROR       
};

enum ErrorCode {
  ERR_NONE,         
  ERR_LOW_WATER,    
  ERR_SENSOR_FAULT, 
  ERR_PUMP_FAIL     
};

SystemState currentState = STATE_IDLE;
ErrorCode currentError = ERR_NONE;
int currentHumidity = 45; 

void setup() {
  Serial.begin(9600);

  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); 
  }
  
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);

  display.setTextSize(1);
  display.setCursor(10, 20);
  display.println(F("WATERING SYSTEM"));
  display.setCursor(10, 40);
  display.println(F("Initializing..."));
  display.display();
  delay(2000);
}

void loop() {
  unsigned long timeMs = millis();
  
  if (timeMs < 4000) {
    currentState = STATE_IDLE;
    currentError = ERR_NONE;
    currentHumidity = 58;
  } else if (timeMs >= 4000 && timeMs < 8000) {
    currentState = STATE_WATERING;
    currentError = ERR_NONE;
    currentHumidity = 32; 
  } else if (timeMs >= 8000 && timeMs < 12000) {
    currentState = STATE_ERROR;
    currentError = ERR_LOW_WATER; 
  } else {
    currentState = STATE_ERROR;
    currentError = ERR_SENSOR_FAULT; 
  }

  updateOLED(currentState, currentError, currentHumidity);
  
  delay(500); 
}

void updateOLED(SystemState state, ErrorCode error, int humidity) {
  display.clearDisplay();

  display.setTextSize(1);
  display.setCursor(0, 0);
  display.print(F("SYS STATUS: "));

  display.setCursor(0, 16);
  switch(state) {
    case STATE_IDLE:
      display.setTextSize(2);
      display.println(F("MONITORING"));
      break;
    case STATE_WATERING:
      display.setTextSize(2);
      display.println(F("WATERING..."));
      break;
    case STATE_ERROR:
      display.setTextSize(2);
      display.setTextColor(SSD1306_WHITE); 
      display.println(F("! ERROR !"));
      break;
  }

  display.drawFastHLine(0, 36, 128, SSD1306_WHITE);

  display.setTextSize(1);
  display.setCursor(0, 44);
  
  if (state == STATE_ERROR) {
    display.print(F("Cause: "));
    switch(error) {
      case ERR_LOW_WATER:
        display.println(F("LOW WATER LEVEL"));
        break;
      case ERR_SENSOR_FAULT:
        display.println(F("SENSOR DETACHED"));
        break;
      case ERR_PUMP_FAIL:
        display.println(F("PUMP OVERLOAD"));
        break;
      default:
        display.println(F("UNKNOWN ERROR"));
        break;
    }
    display.set
Cursor(0, 56);
    display.print(F("Check hardware!"));
  } else {
    display.print(F("Soil Moisture: "));
    display.print(humidity);
    display.println(F("%"));

    int barWidth = map(humidity, 0, 100, 0, 128);
    display.fillRect(0, 58, barWidth, 4, SSD1306_WHITE);
  }

  display.display();
}
