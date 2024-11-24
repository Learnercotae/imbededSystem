import RPi.GPIO as GPIO
import time

# 핀 정의
KEYPAD_PINS = [6, 12, 13, 16, 19, 20, 26, 21]  # Keypad PB4 ~ PB1, PB8 ~ PB5 GPIO 핀
LED_PINS = [4, 17, 18, 27, 22, 23, 24, 25]     # LED1 ~ LED8 GPIO 핀

# 사용자 정의 매핑
KEYPAD_TO_LED_MAP = {
    4: 1,  # PB4 → LED1
    3: 2,  # PB3 → LED2
    2: 3,  # PB2 → LED3
    1: 4,  # PB1 → LED4
    8: 5,  # PB8 → LED5
    7: 6,  # PB7 → LED6
    6: 7,  # PB6 → LED7
    5: 8,  # PB5 → LED8
}

# LED 상태 정의
LED_ON = GPIO.HIGH
LED_OFF = GPIO.LOW
MAX_KEY_BT_NUM = len(KEYPAD_PINS)
MAX_LED_NUM = len(LED_PINS)

# LED 상태 추적 (최소한의 제어를 위한 상태 저장)
led_states = [False] * MAX_LED_NUM

def setup_pins():
    """GPIO 핀 설정"""
    GPIO.setmode(GPIO.BCM)
    # LED 핀을 출력으로 설정
    for pin in LED_PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, LED_OFF)  # 초기화: LED 끄기

    # Keypad 핀을 입력으로 설정 및 풀업 저항 활성화
    for pin in KEYPAD_PINS:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def keypad_read():
    """키패드 상태 읽기"""
    keypad_state = 0
    for i in range(MAX_KEY_BT_NUM):
        if not GPIO.input(KEYPAD_PINS[i]):  # 버튼이 눌린 경우 (LOW 상태)
            keypad_state |= (1 << (i + 1))  # PB4부터 시작하므로 i+1
    return keypad_state

def led_control(led_num, cmd):
    """LED 제어"""
    global led_states
    if 1 <= led_num <= MAX_LED_NUM:
        index = led_num - 1  # LED 번호를 인덱스로 변환
        if led_states[index] != (cmd == LED_ON):  # 상태가 변경된 경우만
            GPIO.output(LED_PINS[index], cmd)
            led_states[index] = (cmd == LED_ON)

def main():
    """메인 함수"""
    setup_pins()

    try:
        while True:
            keypad_state = keypad_read()  # 키패드 상태 읽기

            # 키패드 상태에 따라 LED 제어
            for pb_num, led_num in KEYPAD_TO_LED_MAP.items():
                if keypad_state & (1 << pb_num):  # 해당 버튼이 눌렸다면
                    led_control(led_num, LED_ON)  # LED 켜기
                else:
                    led_control(led_num, LED_OFF)  # LED 끄기

            time.sleep(0.1)  # 디바운싱을 위한 딜레이

    except KeyboardInterrupt:
        print("프로그램 종료")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
