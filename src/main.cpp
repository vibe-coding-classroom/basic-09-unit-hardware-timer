#include <Arduino.h>
#include "types.h"

// Forward declaration of timer init function
void initTimer(uint32_t frequency);

// Define shared data
SharedData shared = {0, false, 0};

// Pin definition for LED
const int LED_PIN = 2;

void setup() {
    Serial.begin(115200);
    pinMode(LED_PIN, OUTPUT);
    
    Serial.println("Starting Hardware Timer Lab...");
    
    // Initialize timer at 1Hz (1 blink per second)
    initTimer(1);
}

void loop() {
    // Task 1: Precision Timer Blink
    // The ISR updates shared.flag, we handle UI here if needed
    // or the ISR could toggle the pin directly (not recommended for complex logic but okay for blink)
    
    if (shared.flag) {
        shared.flag = false;
        digitalWrite(LED_PIN, !digitalRead(LED_PIN));
        Serial.printf("Timer Triggered! Counter: %u, Timestamp: %u ms\n", shared.counter, shared.last_timestamp);
    }

    // --- Intentional Blocking Section ---
    // Simulate a heavy workload or a "stuck" loop to test timer preemption
    Serial.println("Main loop entering 5-second block...");
    delay(5000); 
    Serial.println("Main loop resumed.");
}
