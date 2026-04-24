import os
import re
import sys

def check_file_exists(filepath):
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        return False
    return True

def analyze_src():
    timer_isr_path = "src/timer_isr.cpp"
    types_h_path = "include/types.h"
    
    score = 0
    total_checks = 5
    results = []

    if not check_file_exists(timer_isr_path) or not check_file_exists(types_h_path):
        return 0, ["Missing source files"]

    with open(timer_isr_path, 'r', encoding='utf-8') as f:
        timer_isr_content = f.read()
    
    with open(types_h_path, 'r', encoding='utf-8') as f:
        types_h_content = f.read()

    # 1. Check for IRAM_ATTR
    if "IRAM_ATTR" in timer_isr_content:
        score += 1
        results.append("[PASS] Found IRAM_ATTR in ISR implementation.")
    else:
        results.append("[FAIL] IRAM_ATTR not found. ISR must be in IRAM.")

    # 2. Check for volatile
    if "volatile" in types_h_content:
        score += 1
        results.append("[PASS] Found volatile keyword for shared variables.")
    else:
        results.append("[FAIL] volatile not found. Shared variables must be marked volatile.")

    # 3. Check for forbidden functions in ISR
    # This is a naive check for the whole file, but effective for this lab
    forbidden = ["Serial.print", "delay(", "delayMicroseconds("]
    found_forbidden = [f for f in forbidden if f in timer_isr_content]
    if not found_forbidden:
        score += 1
        results.append("[PASS] No forbidden functions (Serial, delay) found in ISR file.")
    else:
        results.append(f"[FAIL] Forbidden functions found: {', '.join(found_forbidden)}")

    # 4. Check for Critical Sections
    if "portENTER_CRITICAL" in timer_isr_content or "portMUX_TYPE" in timer_isr_content:
        score += 1
        results.append("[PASS] Critical sections / Mutex structures found.")
    else:
        results.append("[FAIL] Critical sections not implemented for data protection.")

    # 5. Check for timer initialization
    if "timerBegin" in timer_isr_content and "timerAttachInterrupt" in timer_isr_content:
        score += 1
        results.append("[PASS] Hardware timer initialization functions used.")
    else:
        results.append("[FAIL] Hardware timer initialization (timerBegin/Attach) missing.")

    return score, results

if __name__ == "__main__":
    print("--- Starting Auto-Grading Static Analysis ---")
    score, results = analyze_src()
    
    for res in results:
        print(res)
    
    final_percentage = (score / 5) * 100
    print(f"\nFinal Score: {score}/5 ({final_percentage}%)")
    
    if score == 5:
        print("\nGreat job! All hardware timer safety requirements are met.")
        sys.exit(0)
    else:
        print("\nSome requirements are missing. Please review the ISR standards in README.md.")
        sys.exit(1)
