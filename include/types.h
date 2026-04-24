#ifndef TYPES_H
#define TYPES_H

#include <Arduino.h>

/**
 * @brief Shared data structure between ISR and main loop
 */
struct SharedData {
    volatile uint32_t counter;
    volatile bool flag;
    volatile uint32_t last_timestamp;
};

#endif // TYPES_H
