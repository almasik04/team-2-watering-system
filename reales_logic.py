from machine import Pin, ADC, I2C
import utime

# 1. Инициализация I2C для OLED и RTC (GP0, GP1)
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

# 2. Датчики влажности (3 зоны)
sensors = [ADC(Pin(26)), ADC(Pin(27)), ADC(Pin(28))]

# 3. Датчик уровня воды (Переключатель)
water_ok = Pin(14, Pin.IN, Pin.PULL_DOWN)

# 4. Реле: Насос (16) и Клапаны (17, 18, 19)
pump = Pin(16, Pin.OUT)
valves = [Pin(17, Pin.OUT), Pin(18, Pin.OUT), Pin(19, Pin.OUT)]

def read_moisture():
    # Чтение значений со всех зон
    return [s.read_u16() for s in sensors]

print("VERSION: Sprint 3 - Active Control Logic")

while True:
    levels = read_moisture()
    
    # Логика защиты: если в баке нет воды (GP14 = 0), насос не включится
    if not water_ok.value():
        print("ALERT: No water in tank! System blocked.")
        pump.off()
    else:
        # Пример: если в зоне 1 сухо (значение > 40000 для сухой почвы)
        if levels[0] > 40000:
            print("Zone 1 dry. Activating watering...")
            valves[0].on()
            pump.on()
        else:
            valves[0].off()
            pump.off()

    print(f"Moisture: {levels} | Water Level: {'OK' if water_ok.value() else 'EMPTY'}")
    utime.sleep(2)

