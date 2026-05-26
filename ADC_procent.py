def clamp(value, min_value, max_value):
"""Ограничивает значение в заданных пределах (аналог constrain в Arduino)"""
return max(min_value, min(value, max_value))

def map_value(value, in_min, in_max, out_min, out_max):
"""Пропорционально переносит значение из одного диапазона в другой (аналог map)"""
# Формула линейной интерполяции
return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def convert_adc_to_percentage(raw_adc, air_value, water_value):
"""
Переводит сырые данные АЦП в проценты влажности (0-100%).
Учитывает обратную зависимость (сухо = высокое значение, мокро = низкое).
"""
# Масштабируем значение: air_value станет 0%, water_value станет 100%
percentage = map_value(raw_adc, air_value, water_value, 0, 100)

# Округляем до целого числа и зажимаем в рамки 0-100%
final_percentage = clamp(round(percentage), 0, 100)

return final_percentage

# --- ПРИМЕР ИСПОЛЬЗОВАНИЯ (ТЕСТИРОВАНИЕ) ---
if __name__ == "__main__":
# Калибровочные значения (подставьте свои данные)
AIR_VALUE = 850 # Полностью сухой датчик
WATER_VALUE = 400 # Полностью мокрый датчик

# Имитация входящих сырых данных с АЦП
test_signals = [850, 400, 625, 900, 350]

print("Результаты конвертации:")
print("-" * 30)

for raw in test_signals:
moisture = convert_adc_to_percentage(raw, AIR_VALUE, WATER_VALUE)
print(f"Сырой сигнал АЦП: {raw:<4} -> Влажность: {moisture}%")
