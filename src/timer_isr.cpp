#include <Arduino.h>
#include "types.h"

// External reference to shared data
extern SharedData shared;

// Timer handle
hw_timer_t * timer = NULL;
portMUX_TYPE timerMux = portMUX_INITIALIZER_UNLOCKED;

/**
 * @brief Hardware Timer ISR
 * Must be in IRAM for performance and reliability
 */
void IRAM_ATTR onTimer() {
    portENTER_CRITICAL_ISR(&timerMux);
    shared.counter++;
    shared.flag = true;
    shared.last_timestamp = millis();
    portEXIT_CRITICAL_ISR(&timerMux);
}

/**
 * @brief Initialize hardware timer
 * @param frequency Frequency in Hz
 */
void initTimer(uint32_t frequency) {
    // Timer 0, divider 80 (1 tick = 1us at 80MHz)
    timer = timerBegin(0, 80, true);
    
    // Attach onTimer function to our timer
    timerAttachInterrupt(timer, &onTimer, true);
    
    // Set alarm to call onTimer function every second (1,000,000 ticks)
    // Formula: 1,000,000 / frequency
    timerAlarmWrite(timer, 1000000 / frequency, true);
    
    // Start an alarm
    timerAlarmEnable(timer);
}
