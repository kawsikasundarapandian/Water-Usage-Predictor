from tabulate import tabulate
import random
from datetime import datetime
from deep_translator import GoogleTranslator
import csv

CROP_WATER_REQUIREMENT = {
    "Wheat": 500,
    "Rice": 800,
    "Maize": 600
}

GROWTH_STAGE_MULTIPLIER = {
    "Seedling": 0.8,
    "Vegetative": 1.0,
    "Flowering": 1.2,
    "Harvest": 1.0
}

DAILY_TIPS = [
    "Water helps plants grow!",
    "Too much water can harm roots!",
    "Rain can reduce your water needs!",
    "Check soil moisture before watering!"
]

def calculate_daily_water(crop, temperature, rainfall, humidity, stage_multiplier):
    water = CROP_WATER_REQUIREMENT[crop] * stage_multiplier

    # Temperature effect
    if temperature > 35:
        water += 100
    elif temperature < 20:
        water -= 50
    if humidity < 40:
        water += 50
    elif humidity > 80:
        water -= 50

    if rainfall > 10:
        water -= 100

    return max(water, 0)

def safety_tips():
    print("\n✅ Safety Tips:")
    print("🌧️ Stay indoors during heavy rain.")
    print("💧 Water crops carefully to avoid overwatering.")
    print("⚡ Avoid going near electric poles during storms.\n")

def daily_advice(water):
    if water > 700:
        return "💧 Water heavily today."
    elif water > 400:
        return "💧 Water moderately today."
    else:
        return "💧 Water lightly today."

def main():
    print("______________\n")
    
    print("   🌊 ADVANCED WATER USAGE PREDICTOR   ")
    print("_____________\n")

    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    print(f"📅 Date & Time: {now}\n")

    name = input("Enter your name: ")
    print(f"Hello {name}! Let's check your irrigation forecast.\n")
    print("Available Crops: Wheat / Rice / Maize")
    crops_input = input("Enter crop(s) separated by comma: ").title().split(",")
    crops = [c.strip() for c in crops_input if c.strip() in CROP_WATER_REQUIREMENT]
    if not crops:
        print("\033[91m❌ No valid crops entered!\033[0m")
        return
    stage = input("Enter growth stage (Seedling/Vegetative/Flowering/Harvest): ").capitalize()
    if stage not in GROWTH_STAGE_MULTIPLIER:
        print("\033[91m❌ Invalid growth stage!\033[0m")
        return
    stage_multiplier = GROWTH_STAGE_MULTIPLIER[stage]
    weather_data = []
    for _ in range(7):
        temperature = round(random.uniform(18, 40), 1)
        rainfall = round(random.uniform(0, 20), 1)
        humidity = round(random.uniform(30, 90), 1)
        weather_data.append((temperature, rainfall, humidity))
    total_water_per_crop = {crop: 0 for crop in crops}
    alert_message = ""
    table_data = []
    for day, (temp, rain, humidity) in enumerate(weather_data, start=1):
        row = [day, f"{temp}°C", f"{rain} mm", f"{humidity}%"]
        for crop in crops:
            required = calculate_daily_water(crop, temp, rain, humidity, stage_multiplier)
            total_water_per_crop[crop] += required
            advice = daily_advice(required)
            emoji = "🌞" if temp > 35 else "🌧️" if rain > 10 else "💧"
            row.append(f"{required} L {emoji} ({advice})")
        table_data.append(row)
        if rain > 15:
            alert_message += f"🌧️ Day {day}: Heavy rain expected. Reduce irrigation.\n"
    headers = ["Day", "Temp", "Rainfall", "Humidity"] + [f"{c} Water" for c in crops]
    print("\n📊 IRRIGATION FORECAST (7 Days)")
    print(tabulate(table_data, headers=headers, tablefmt="Datagrid"))
    print("\n💧 Weekly Summary:")
    for crop in crops:
        print(f"{crop}: {total_water_per_crop[crop]} liters total")

    safety_tips()

    if alert_message:
        print("\033[93m⚠️ Alerts:\033[0m")
        print(alert_message)

    print("💡 Tip of the Day:", random.choice(DAILY_TIPS))

    with open("irrigation_alerts.txt", "w", encoding="utf-8") as file:
        file.write(f"Date & Time: {now}\n")
        file.write(f"Crops: {', '.join(crops)}\n")
        file.write(tabulate(table_data, headers=headers, tablefmt="Datagrid"))
        if alert_message:
            file.write("\n\nAlerts:\n" + alert_message)
        file.write("\n\nWeekly Summary:\n")
        for crop in crops:
            file.write(f"{crop}: {total_water_per_crop[crop]} liters total \n")

    with open("irrigation_forecast.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(table_data)

    try:
        for crop in crops:
            tamil_text = GoogleTranslator(source='auto', target='ta').translate(
                f"Total Water Needed for {crop} for 7 Days: {total_water_per_crop[crop]} liters")
            print(f"🌐 Tamil Translation ({crop}): {tamil_text}")
    except:
        print("⚠️ Tamil translation failed. Check internet connection.")

    print("\n✔ Program completed successfully!")

if _name_ == "_main_":
    main()
