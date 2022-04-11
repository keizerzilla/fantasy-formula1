# genetic_team.py
# Artur Rodrigues (artur.rodrigues26@gmail.com)


import numpy as np
import pandas as pd


def load_data(filepath):
    return pd.read_csv(filepath)


def init_population():
    pass


def calc_fitness():
    pass


def selection():
    pass


def crossover():
    pass


def mutation():
    pass


if __name__ == "__main__":
    n = 10
    
    df = load_data("drivers.csv")
    
    init_population()
    
    for i in range(n):
        calc_fitness()
        selection()
        crossover()
        mutation()
        
        print(f"GEN {i:02d}")