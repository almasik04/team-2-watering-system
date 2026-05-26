import time
from enum import Enum
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont

try:
    serial = i2c(port=1, address=0x3C)
    device = ssd1306(serial, width=128, height=64)
except Exception as e:
    print(f"Ошибка инициализации дисплея: {e}")
    exit(1)

class SystemState(Enum):
    STATE_IDLE = 1       
    STATE_WATERING = 2   
    STATE_ERROR = 3      

class ErrorCode(Enum):
    ERR_NONE = 0         
    ERR_LOW_WATER = 1    
    ERR_SENSOR_FAULT = 2 
    ERR_PUMP_FAIL = 3   

font_small = ImageFont.load_default()
font_large = ImageFont.load_default() 

def update_oled(state: SystemState, error: ErrorCode, humidity: int):
    """Функция отрисовки интерфейса на OLED-дисплее (с защитой от мерцания)"""

    image = Image.new('1', (device.width, device.height))
    draw = ImageDraw.Draw(image)

    draw.text((0, 0), "SYS STATUS:", font=font_small, fill=255)

    if state == SystemState.STATE_IDLE:
        draw.text((0, 14), "MONITORING", font=font_large, fill=255)
    elif state == SystemState.STATE_WATERING:
        draw.text((0, 14), "WATERING...", font=font_large, fill=255)
    elif state == SystemState.STATE_ERROR:
        draw.text((0, 14), "! ERROR !", font=font_large, fill=255)

    draw.line([(0, 36), (128, 36)], fill=255)

    if state == SystemState.STATE_ERROR:
        error_msg = "UNKNOWN ERROR"
        if error == ErrorCode.ERR_LOW_WATER:
            error_msg = "LOW WATER LEVEL"
        elif error == ErrorCode.ERR_SENSOR_FAULT:
            error_msg = "SENSOR DETACHED"
        elif error == ErrorCode.ERR_PUMP_FAIL:
            error_msg = "PUMP OVERLOAD"
            
        draw.text((0, 42), f"Cause: {error_msg}", font=font_small, fill=255)
        draw.text((0, 54), "Check hardware!", font=font_small, fill=255)
    else:
        draw.text((0, 42), f"Soil Moisture: {humidity}%", font=font_small, fill=255)

        humidity = max(0, min(humidity, 100))
        bar_width = int((humidity / 100.0) * 128)
        draw.rectangle([(0, 58), (bar_width, 62)], fill=255, outline=255)

    device.display(image)

def main():
    init_image = Image.new('1', (device.width, device.height))
    init_draw = ImageDraw.Draw(init_image)
    init_draw.text((10, 20), "WATERING SYSTEM", font=font_small, fill=255)
    init_draw.text((10, 40), "Initializing...", font=font_small, fill=255)
    device.display(init_image)
    time.sleep(2)

    start_time = time.time()
    
    print("Демо-цикл запущен. Для выхода нажмите Ctrl+C")

    try:
        while True:
            elapsed = time.time() - start_time
            
            if elapsed < 4:
                current_state = SystemState.STATE_IDLE
                current_error = ErrorCode.ERR_NONE
                current_humidity = 58
            elif 4 <= elapsed < 8
                current_state = SystemState.STATE_WATERING
                current_error = ErrorCode.ERR_NONE
                current_humidity = 32
            elif 8 <= elapsed < 12:
                current_state = SystemState.STATE_ERROR
                current_error = ErrorCode.ERR_LOW_WATER
                current_humidity = 0
            else:
                current_state = SystemState.STATE_ERROR
                current_error = ErrorCode.ERR_SENSOR_FAULT
                current_humidity = 0

            update_oled(current_state, current_error, current_humidity)
            
            time.sleep(0.5) 
            
    except KeyboardInterrupt:
        device.clear()
        print("\nСкрипт остановлен, экран очищен.")

if __name__ == "__main__":
    main()
