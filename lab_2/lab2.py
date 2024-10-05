import numpy as np
import csv
import matplotlib.pyplot as plt
from datetime import datetime

def read_column_from_csv(filename, column_name):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        col_index = headers.index(column_name)
        data = [row[col_index] for row in reader]
        return np.array(data)

def parse_date(date_str):
    for fmt in ('%m/%d/%Y', '%Y-%m-%d'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Date {date_str} does not match expected formats")

tank_losses = read_column_from_csv('C:/Dev/University/Python/lab_2/russia_losses_equipment.csv', 'tank').astype(float)
daily_losses = np.diff(tank_losses[::-1])
largest_losses = (np.sort(daily_losses))[-4:]
print('Найбільщі добові втрати:', largest_losses)

def get_spring_losses(filename):
    dates = read_column_from_csv(filename, 'date')
    dates = np.array([parse_date(date) for date in dates])
    start_date = datetime.strptime('2023-03-01', '%Y-%m-%d')
    end_date = datetime.strptime('2023-05-31', '%Y-%m-%d')
    spring_mask = (dates >= start_date) & (dates <= end_date)

    return np.sum(tank_losses[spring_mask])

spring_losses = get_spring_losses('C:/Dev/University/Python/lab_2/russia_losses_equipment.csv')
average_last_100_days = np.mean(daily_losses[-100:])

def plot_tank_losses_over_year(tank_losses):
    plt.figure(figsize=(8, 16), dpi=100)
    plt.plot(tank_losses[-365:][::-1], linestyle='--', label='Втрати танків')
    plt.title('Втрати танків за минулий рік')
    plt.xlabel('Дні')
    plt.ylabel('Кількість танків')
    plt.grid(True, linestyle=':', color='gray')
    plt.legend()
    plt.savefig('tank_losses.png')
    plt.show()

plot_tank_losses_over_year(tank_losses)
