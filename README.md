# Carbon Footprint Calculator

A command-line Python program that estimates a person's yearly carbon footprint from values entered by the user. It was made as part of an Environmental Sustainability (EVS) project.

**Author:** Tanmay Mishra, B.Tech CSE, VIT Bhopal

---

## What is a carbon footprint?

A carbon footprint is the total amount of greenhouse gases released because of a person's activities, such as travelling, using electricity, cooking, eating and throwing away waste. It is measured in **kg of CO2-equivalent (CO2e)**, which puts all greenhouse gases on one common scale.

The calculator uses one simple formula for every activity:

```
emissions (kg CO2e) = activity amount x emission factor
```

For example, travelling 10 km by bus every week:
`10 km x 52 weeks x 0.09 kg CO2e per km = 46.8 kg CO2e per year`

---

## Features

- Asks the user to enter their own values (nothing is hard-coded)
- Covers six categories: transport, air travel, electricity, cooking gas (LPG), food and waste
- Checks every input and asks again if the user types letters, negative numbers or out-of-range values
- Shares household emissions (electricity and LPG) between all people in the home
- Shows a table with the kg CO2e and percentage share of each category
- Compares the result with the India and world per-person averages
- Tells the user how many trees would be needed to absorb their yearly emissions
- Gives a tip to reduce the biggest source of emissions
- Can save the report to a text file
- Can calculate for several people in one run

---

## Requirements

- Python 3.6 or newer
- No extra libraries (it only uses Python's built-in `datetime` module)

---

## How to run

### In VS Code

1. Save the program as `carbon_footprint.py`.
2. Open the file in VS Code (install the Python extension if asked).
3. Click the **Run** (play) button at the top right, **or** open the terminal and type the command below.
4. Type each answer in the terminal and press Enter.

### In a terminal

```bash
python carbon_footprint.py
```

On a Mac or Linux, use `python3 carbon_footprint.py` if `python` is not found.

---

## Inputs the program asks for

| # | Category | What you enter |
|---|----------|----------------|
| 0 | Basic details | Your name and the number of people in your household |
| 1 | Transport | Km travelled **per week** by car (petrol, diesel, CNG), two-wheeler, bus, train, metro and auto-rickshaw. If you use a car, also the number of people travelling in it |
| 2 | Air travel | Total km flown **per year** |
| 3 | Electricity | Units (kWh) used by the household **per month**, from the electricity bill |
| 4 | Cooking gas | Number of 14.2 kg LPG cylinders the household uses **per year** |
| 5 | Food | Your diet type, chosen from a menu |
| 6 | Waste | Household waste in kg **per week** and the percentage recycled or composted |

Type `0` for anything you do not use.

---

## How each category is calculated

| Category | Calculation |
|----------|-------------|
| Transport | km per week x 52 x factor for each mode (car emissions are divided by the number of people in the car) |
| Air travel | km per year x 0.15 |
| Electricity | kWh per month x 12 x 0.79 / household size |
| Cooking gas (LPG) | cylinders per year x 14.2 kg x 2.98 / household size |
| Food | fixed yearly value for the chosen diet |
| Waste | kg per week x 52 x (1 - recycled share) x 0.45 |

**Total footprint = sum of all six categories** (kg CO2e per person per year).

---

## Emission factors used

All values are stored together near the top of `carbon_footprint.py`, so they are easy to change.

| Item | Value | Unit |
|------|-------|------|
| Car (petrol) | 0.17 | kg CO2e per passenger-km |
| Car (diesel) | 0.17 | kg CO2e per passenger-km |
| Car (CNG) | 0.12 | kg CO2e per passenger-km |
| Two-wheeler | 0.06 | kg CO2e per passenger-km |
| Bus | 0.09 | kg CO2e per passenger-km |
| Train | 0.04 | kg CO2e per passenger-km |
| Metro | 0.03 | kg CO2e per passenger-km |
| Auto-rickshaw | 0.10 | kg CO2e per passenger-km |
| Flights | 0.15 | kg CO2e per passenger-km |
| Electricity (Indian grid) | 0.79 | kg CO2e per kWh |
| LPG | 2.98 | kg CO2e per kg of LPG |
| Waste to landfill | 0.45 | kg CO2e per kg of waste |
| Diet: vegan / vegetarian / eggetarian / non-veg (1-3 times a week) / non-veg (almost daily) | 1000 / 1400 / 1700 / 2000 / 2600 | kg CO2e per year |

**Source notes**

- The electricity factor of 0.79 is from the Central Electricity Authority (CEA) CO2 Baseline Database, version 16 (financial year 2019-20). Newer versions are published, so update this value if you have the latest one.
- The other factors are typical rounded values for a student project, not exact measurements. If your teacher or report needs cited figures, replace them with values from a source you can reference.
- The averages used for comparison (India about 2.0 tonnes and world about 4.7 tonnes of CO2 per person per year) and the figure of about 21 kg of CO2 absorbed by one tree in a year are also approximate.

---

## Sample run

Inputs: household of 4, two-wheeler 30 km, bus 10 km, metro 20 km and auto-rickshaw 5 km per week, flights 1600 km per year, electricity 150 kWh per month, 8 LPG cylinders per year, vegetarian diet, 7 kg waste per week with 30% recycled.

```
Category                kg CO2e / year    Share
------------------------------------------------------------
Food                           1,400.0    58.5%  ##############
Electricity                      355.5    14.9%  ###
Air travel                       240.0    10.0%  ##
Transport                        197.6     8.3%  ##
Waste                            114.7     4.8%  #
Cooking gas (LPG)                 84.6     3.5%
------------------------------------------------------------
TOTAL                          2,392.4
Your yearly footprint: 2.39 tonnes CO2e
Per month: 199 kg   |   Per day: 6.6 kg

Comparison (tonnes CO2 per person per year, approximate):
  You: 2.39   India average: 2.0   World average: 4.7
  Result: MODERATE - above the Indian average but below the world average.

To absorb this much CO2 you would need about 114 trees growing for a year.

Biggest source: Food
Tip: Eat more plant-based meals, buy local and seasonal, avoid wasting food.
```

---

## How the program is organised

| Part of the code | Purpose |
|------------------|---------|
| Emission factor constants | All numbers used in the calculations, in one place |
| `ask_float`, `ask_int`, `ask_choice`, `ask_yes_no` | Read and validate user input |
| `calc_transport`, `calc_flights`, `calc_electricity`, `calc_lpg`, `calc_food`, `calc_waste` | One function per category, each returns kg CO2e per year |
| `build_report` | Creates the result table, comparison, trees and tip |
| `run_once` / `main` | Runs the questions in order, prints and optionally saves the report |

---

## Limitations

- The results are **estimates**, because real emissions depend on the exact vehicle, appliance, food and location.
- Food is estimated from a diet type, not from the exact meals eaten.
- Only the main sources of household emissions are included. Shopping, clothing, water use and online activity are not counted.

## Possible improvements

- Add a graphical interface or a chart of the category shares
- Add more categories such as shopping, water and clothing
- Keep a history of past results to track progress over time
- Load the emission factors from a separate file so they can be updated without changing the code

---

## References

- Central Electricity Authority (CEA), Government of India: CO2 Baseline Database for the Indian Power Sector
- Add the other books, reports or websites your class or teacher recommended for the remaining emission factors
