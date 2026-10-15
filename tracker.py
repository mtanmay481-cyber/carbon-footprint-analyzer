"""
Carbon Footprint Calculator  (EVS project)
------------------------------------------
The user enters their own values (travel, electricity, cooking gas, food, waste).
The program converts them into kg of CO2-equivalent (CO2e) per year and shows
a breakdown, a comparison with India / world averages, and tips to reduce it.

Formula used everywhere:   emissions (kg CO2e) = activity amount x emission factor

Run with:   python carbon_footprint.py
"""

from datetime import datetime

# ---------------------------------------------------------------------------
# EMISSION FACTORS  (edit these if your teacher / reference book gives other values)
# NOTE: apart from the grid factor, these are typical rounded values for a student
# project, not exact figures. Replace them with a source you can cite.
# ---------------------------------------------------------------------------
WEEKS_PER_YEAR = 52
MONTHS_PER_YEAR = 12

# kg CO2e per passenger-km
TRANSPORT_FACTORS = {
    "Car (petrol)": 0.17,
    "Car (diesel)": 0.17,
    "Car (CNG)": 0.12,
    "Two-wheeler (bike/scooter)": 0.06,
    "Bus": 0.09,
    "Train": 0.04,
    "Metro": 0.03,
    "Auto-rickshaw": 0.10,
}
CAR_MODES = ("Car (petrol)", "Car (diesel)", "Car (CNG)")

FLIGHT_FACTOR = 0.15          # kg CO2e per passenger-km (economy, includes high-altitude effect)
GRID_FACTOR = 0.79            # kg CO2e per kWh, Indian grid average (CEA CO2 Baseline Database v16, FY 2019-20;
                              # newer versions exist - update this if you have the latest)
LPG_KG_PER_CYLINDER = 14.2    # domestic LPG cylinder
LPG_FACTOR = 2.98             # kg CO2e per kg of LPG burnt
LANDFILL_FACTOR = 0.45        # kg CO2e per kg of waste sent to landfill

# Rough annual food footprint per person (kg CO2e per year)
DIETS = [
    ("Vegan", 1000),
    ("Vegetarian", 1400),
    ("Eggetarian", 1700),
    ("Non-vegetarian (1-3 times a week)", 2000),
    ("Non-vegetarian (almost daily)", 2600),
]

# Comparison values (tonnes CO2 per person per year, approximate)
INDIA_AVERAGE_T = 2.0
WORLD_AVERAGE_T = 4.7
KG_ABSORBED_PER_TREE_PER_YEAR = 21   # approximate for a mature tree

TIPS = {
    "Transport": "Use bus/metro/train, share rides, walk or cycle for short trips.",
    "Air travel": "Fly less, choose trains for medium distances, avoid unnecessary trips.",
    "Electricity": "Use LED bulbs, 5-star appliances, switch off standby devices, set AC to 24-26 C.",
    "Cooking gas (LPG)": "Use pressure cookers, cover pots, and plan cooking to avoid wasting gas.",
    "Food": "Eat more plant-based meals, buy local and seasonal, avoid wasting food.",
    "Waste": "Segregate waste, compost kitchen waste, recycle, and avoid single-use plastic.",
}


# ---------------------------------------------------------------------------
# INPUT HELPERS  (keep asking until the user types something valid)
# ---------------------------------------------------------------------------
def ask_float(prompt, minimum=0.0, maximum=None):
    """Ask for a number; repeat until it is valid and inside the allowed range."""
    while True:
        text = input(prompt).strip()
        try:
            value = float(text)
        except ValueError:
            print("  Please enter a number (for example 12 or 3.5).")
            continue
        if value < minimum:
            print(f"  The value cannot be less than {minimum:g}.")
            continue
        if maximum is not None and value > maximum:
            print(f"  The value cannot be more than {maximum:g}.")
            continue
        return value


def ask_int(prompt, minimum=0, maximum=None):
    """Ask for a whole number within a range."""
    while True:
        value = ask_float(prompt, minimum, maximum)
        if value == int(value):
            return int(value)
        print("  Please enter a whole number.")


def ask_choice(prompt, options):
    """Show a numbered menu and return the index (0-based) of the chosen option."""
    for number, option in enumerate(options, start=1):
        print(f"  {number}. {option}")
    return ask_int(prompt, 1, len(options)) - 1


def ask_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("  Please type y or n.")


# ---------------------------------------------------------------------------
# CALCULATIONS  (each returns kg CO2e per person per year)
# ---------------------------------------------------------------------------
def calc_transport():
    print("\n--- 1. DAILY TRANSPORT ---")
    print("Enter how many km you travel PER WEEK by each mode (type 0 if you do not use it).")
    car_kg = 0.0
    other_kg = 0.0
    for mode, factor in TRANSPORT_FACTORS.items():
        km_per_week = ask_float(f"  {mode} - km per week: ")
        yearly_kg = km_per_week * WEEKS_PER_YEAR * factor
        if mode in CAR_MODES:
            car_kg += yearly_kg
        else:
            other_kg += yearly_kg
    if car_kg > 0:
        people = ask_int("  How many people usually travel in the car (including you)? ", 1, 10)
        car_kg /= people          # the car's emissions are shared by everyone in it
    return car_kg + other_kg


def calc_flights():
    print("\n--- 2. AIR TRAVEL ---")
    km_per_year = ask_float("  Total distance you fly in a year in km (0 if none; Delhi-Mumbai return is about 2800): ")
    return km_per_year * FLIGHT_FACTOR


def calc_electricity(household):
    print("\n--- 3. ELECTRICITY AT HOME ---")
    kwh_per_month = ask_float("  Units (kWh) used by your household per month (see your electricity bill): ")
    return kwh_per_month * MONTHS_PER_YEAR * GRID_FACTOR / household   # shared by the household


def calc_lpg(household):
    print("\n--- 4. COOKING GAS (LPG) ---")
    cylinders = ask_float(f"  Number of {LPG_KG_PER_CYLINDER:g} kg LPG cylinders your household uses per year (0 if none): ")
    return cylinders * LPG_KG_PER_CYLINDER * LPG_FACTOR / household


def calc_food():
    print("\n--- 5. FOOD ---")
    print("Which best describes your diet?")
    index = ask_choice("  Enter choice number: ", [name for name, _ in DIETS])
    return DIETS[index][1]


def calc_waste():
    print("\n--- 6. WASTE ---")
    kg_per_week = ask_float("  Household waste you throw away per week in kg (0 if you do not know): ")
    recycled_percent = ask_float("  What percentage of it is recycled or composted? (0-100): ", 0, 100)
    landfill_kg = kg_per_week * WEEKS_PER_YEAR * (1 - recycled_percent / 100)
    return landfill_kg * LANDFILL_FACTOR


# ---------------------------------------------------------------------------
# REPORT
# ---------------------------------------------------------------------------
def build_report(name, results):
    total_kg = sum(results.values())
    total_t = total_kg / 1000
    lines = []
    lines.append("=" * 60)
    lines.append(f"CARBON FOOTPRINT REPORT - {name}")
    lines.append(datetime.now().strftime("Date: %d %B %Y, %I:%M %p"))
    lines.append("=" * 60)
    lines.append(f"{'Category':<22}{'kg CO2e / year':>16}{'Share':>9}")
    lines.append("-" * 60)
    for category, kg in sorted(results.items(), key=lambda item: item[1], reverse=True):
        share = (kg / total_kg * 100) if total_kg else 0
        bar = "#" * int(share / 4)
        lines.append(f"{category:<22}{kg:>16,.1f}{share:>8.1f}%  {bar}")
    lines.append("-" * 60)
    lines.append(f"{'TOTAL':<22}{total_kg:>16,.1f}")
    lines.append(f"Your yearly footprint: {total_t:.2f} tonnes CO2e")
    lines.append(f"Per month: {total_kg / 12:,.0f} kg   |   Per day: {total_kg / 365:,.1f} kg")
    lines.append("")
    lines.append("Comparison (tonnes CO2 per person per year, approximate):")
    lines.append(f"  You: {total_t:.2f}   India average: {INDIA_AVERAGE_T}   World average: {WORLD_AVERAGE_T}")
    if total_t <= INDIA_AVERAGE_T:
        lines.append("  Result: LOW - you are at or below the Indian average. Keep it up!")
    elif total_t <= WORLD_AVERAGE_T:
        lines.append("  Result: MODERATE - above the Indian average but below the world average.")
    else:
        lines.append("  Result: HIGH - above the world average. Small changes can reduce this a lot.")
    trees = total_kg / KG_ABSORBED_PER_TREE_PER_YEAR
    lines.append(f"\nTo absorb this much CO2 you would need about {trees:,.0f} trees growing for a year.")
    top_category = max(results, key=results.get)
    lines.append(f"\nBiggest source: {top_category}")
    lines.append(f"Tip: {TIPS[top_category]}")
    lines.append("=" * 60)
    return "\n".join(lines)


def run_once():
    name = input("\nEnter your name: ").strip() or "Student"
    household = ask_int("How many people live in your household (including you)? ", 1, 30)

    results = {
        "Transport": calc_transport(),
        "Air travel": calc_flights(),
        "Electricity": calc_electricity(household),
        "Cooking gas (LPG)": calc_lpg(household),
        "Food": calc_food(),
        "Waste": calc_waste(),
    }

    report = build_report(name, results)
    print("\n" + report)

    if ask_yes_no("\nSave this report to a text file? (y/n): "):
        filename = "carbon_report_" + name.lower().replace(" ", "_") + ".txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(report + "\n")
        print(f"Report saved as {filename}")


def main():
    print("=" * 60)
    print("        CARBON FOOTPRINT CALCULATOR  (EVS PROJECT)")
    print("=" * 60)
    print("Enter your own values when asked. Results are estimates in")
    print("kg of CO2-equivalent (CO2e) per person per year.")
    while True:
        run_once()
        if not ask_yes_no("\nCalculate for another person? (y/n): "):
            break
    print("\nThank you! Every small step to reduce emissions helps the planet.")


if __name__ == "__main__":
    main()