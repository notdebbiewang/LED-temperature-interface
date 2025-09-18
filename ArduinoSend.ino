#include <FastLED.h>

#define LED_PIN     4 //arduino pin
#define NUM_LEDS    120 //total LEDs
#define BRIGHTNESS  100
#define LED_TYPE    WS2812B
#define COLOR_ORDER GRB

CRGB leds[NUM_LEDS]; //array of LEDs
float currentTemp;

void setup() {
  //default settings
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);
  
  Serial.begin(9600);
  Serial.setTimeout(10); //changed from 1 to 10
}

// communicating with the python code connected to the lakeshore
void loop() {
  if (Serial.available()) {
    String s = Serial.readStringUntil('\n'); // stop at newline
    currentTemp = s.toFloat();                // parse float
    Serial.println(currentTemp, 3);           // echo back
    temperatureToColor(currentTemp);
    FastLED.show();
  }
}

// changing colour based on temperature
void temperatureToColor(float temp) {
  //bounds (upper --> lower)
  const float t1 = 273.15; // room temp (white above this, no fade)
  const float t2 = 200.00;
  const float t3 = 100.00;
  const float t4 = 40.00;
  const float t5 = 10.00;
  const float t6 = 4.00;
  const float t7 = 0.01;

  //rounding to prevent errors
  auto clamp01 = [](float x){ return x < 0 ? 0.0f : (x > 1 ? 1.0f : x); };

  if (temp > t1) {
    // WHITE | ABOVE 273.15 K
    fill_solid(leds, NUM_LEDS, CRGB(255,255,255));
    return;
  }

  // RED -> ORANGE | 273 K to 200 K
  if (temp > t2) {
    float frac = clamp01((t1 - temp) / (t1 - t2));   // 0 at t1, 1 at t2
    uint8_t g = (uint8_t)(frac * 128);               // 0 → 128
    fill_solid(leds, NUM_LEDS, CRGB(255, g, 0));     // (255,0,0) → (255,128,0)
    return;
  }

  // ORANGE -> YELLOW | 200 K to 100 K
  if (temp > t3) {
    float frac = clamp01((t2 - temp) / (t2 - t3));   // 0 at t2, 1 at t3
    uint8_t g = (uint8_t)(128 + frac * (255 - 128)); // 128 → 255
    fill_solid(leds, NUM_LEDS, CRGB(255, g, 0));     // (255,128,0) → (255,255,0)
    return;
  }

  // YELLOW -> GREEN | 100 K to 40 K
  if (temp > t4) {
    float frac = clamp01((t3 - temp) / (t3 - t4));   // 0 at t3, 1 at t4
    uint8_t r = (uint8_t)(255 * (1.0f - frac));      // 255 → 0
    fill_solid(leds, NUM_LEDS, CRGB(r, 255, 0));     // (255,255,0) → (0,255,0)
    return;
  }

  // GREEN -> CYAN | 40 K to 10 K
  if (temp > t5) {
    float frac = clamp01((t4 - temp) / (t4 - t5));   // 0 at t4, 1 at t5
    uint8_t b = (uint8_t)(255 * frac);               // 0 → 255
    fill_solid(leds, NUM_LEDS, CRGB(0, 255, b));     // (0,255,0) → (0,255,255)
    return;
  }

  // CYAN -> LIGHT BLUE | 10 K to 4 K
  if (temp > t6) {
    float frac = clamp01((t5 - temp) / (t5 - t6));   // 0 at t5, 1 at t6
    uint8_t g = (uint8_t)(255 - frac * (255 - 128)); // 255 → 128
    fill_solid(leds, NUM_LEDS, CRGB(0, g, 255));     // (0,255,255) → (0,128,255)
    return;
  }

  //flashing when at 4 K ± 0.01 K
  if (fabs(temp - t7) < 0.01){
    flash();
  }

  // LIGHT BLUE -> DARK BLUE | 4 K to 0.01 K
  if (temp > t7) {
    float frac = clamp01((t6 - temp) / (t6 - t7));   // 0 at t6, 1 at t7
    uint8_t g = (uint8_t)(128 * (1.0f - frac));      // 128 → 0
    fill_solid(leds, NUM_LEDS, CRGB(0, g, 255));     // (0,128,255) → (0,0,255)
    return;
  }

  // PURPLE | <0.01 K 
  fill_solid(leds, NUM_LEDS, CRGB(128, 0, 128));
}

// flashing when next cooldown stage begins
void flash() {
  // Flash LEDs on
  fill_solid(leds, NUM_LEDS, CRGB::Green);
  FastLED.show();
  delay(200);  // LED on for 200ms

  // Flash LEDs off
  fill_solid(leds, NUM_LEDS, CRGB::Black);
  FastLED.show();
  delay(200);  // LED off for 200ms
}
