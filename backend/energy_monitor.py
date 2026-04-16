import json
import os
import time

DATA_FILE = os.path.join(os.path.dirname(__file__), "energy_data.json")
BASE_POWER = 10
MAX_POWER = 65
CARBON_FACTOR = 0.82
PHONE_CHARGE_KWH = 0.015

def load_energy():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                return data.get("energy_kwh", 0.0)
        except Exception:
            return 0.0
    return 0.0

def save_energy(energy_kwh):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump({"energy_kwh": energy_kwh}, f)
    except Exception as e:
        pass

energy_kwh = load_energy()
last_update_time = time.time()
current_power_watts = BASE_POWER # Default value

def estimate_power(cpu, memory_percent):
    return BASE_POWER + ((cpu * 0.6 + memory_percent * 0.4) / 100) * (MAX_POWER - BASE_POWER)

def update_energy(cpu, memory_percent):
    global energy_kwh, last_update_time, current_power_watts
    current_time = time.time()
    interval = current_time - last_update_time
    last_update_time = current_time
    
    if interval > 0:
        current_power_watts = estimate_power(cpu, memory_percent)
        energy_kwh += (current_power_watts * interval) / (1000 * 3600) # kWh formula
        save_energy(energy_kwh)
        return current_power_watts, energy_kwh
    return current_power_watts, energy_kwh

def get_energy_stats():
    global current_power_watts, energy_kwh
    carbon = energy_kwh * CARBON_FACTOR
    phone_eq = energy_kwh / PHONE_CHARGE_KWH

    return {
        "power_watts": round(current_power_watts, 2),
        "energy_kwh": round(energy_kwh, 4),
        "carbon_kg": round(carbon, 4),
        "equivalent": f"{int(phone_eq)} phone charges"
    }

