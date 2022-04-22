# genetic_team.py
# Artur Rodrigues (artur.rodrigues26@gmail.com)


import random
import itertools
import pandas as pd


def summary_team(team):
    drivers_points = 0
    for d in team["drivers"]:
        name = d["driver"]
        points = d["points"]
        price = d["price"]
        drivers_points += points
        
        print(f"{name:<15}: {points} points, {price} moneys")
    
    name = team["constructor"]["name"]
    points = team["constructor"]["points"]
    price = team["constructor"]["price"]
    constructor = f"{name:<15}: {points} points, {price} moneys"
    
    print(constructor)
    print("Total points:", drivers_points + points)


def init(target_team, pop_size, race=None):
    df_drivers = pd.read_csv("drivers.csv")
    df_constructors = pd.read_csv("constructors.csv")
    
    if race is None:
        df_drivers = df_drivers[["driver", "points", "price"]]
        df_constructors = df_constructors[["constructor", "points", "price"]]
    else:
        df_drivers = df_drivers[["driver", race, "price"]]
        df_drivers = df_drivers.rename(columns={race : "points"})
        
        df_constructors = df_constructors[["constructor", race, "price"]]
        df_constructors = df_constructors.rename(columns={race : "points"})
    
    team = df_constructors[df_constructors["constructor"] == target_team]
    
    pop = [
        {
            "drivers"     : df_drivers.sample(n=5).to_dict("records"),
            "constructor" : {
                "name"   : target_team,
                "price"  : float(team["price"]),
                "points" : float(team["points"]),
            },
            "score"       : 0,
        }
        for i in range(pop_size)
    ]
    
    return pop, df_drivers


def filter_teams(pop, budget):
    filtered_pop = []
    for p in pop:
        team_price = p["constructor"]["price"]
        drivers_price = sum([d["price"] for d in p["drivers"]])
        total_price = team_price + drivers_price
        
        unique_drivers = len(list(set([d["driver"] for d in p["drivers"]])))
        
        if total_price <= budget and unique_drivers == 5:
            filtered_pop.append(p)
    
    return filtered_pop

def fitness(pop):
    for p in pop:
        drivers_price = sum([d["price"] for d in p["drivers"]])
        drivers_points = sum([d["points"] for d in p["drivers"]])
        p["score"] = drivers_points
    
    return pop


def sort(pop):
    sort_score = lambda t : t["score"]
    pop = sorted(pop, key=sort_score, reverse=True)
    
    return pop


def selection(pop, pop_size):
    return pop[:pop_size]


def crossover(pop, cross_prob):
    new_teams = []
    for i in range(len(pop)):
        if random.uniform(0, 1) > cross_prob:
            continue
        
        samples = random.sample(pop, 2)
        cross_point = random.randint(1, 4)
        team = {
            "drivers"     : samples[0]["drivers"][:cross_point] + samples[1]["drivers"][cross_point:],
            "constructor" : samples[0]["constructor"],
            "score"       : 0,
        }
        
        new_teams.append(team)
    
    pop = pop + new_teams
    
    return pop


def mutation(pop, df_drivers, mut_prop):
    
    for p in pop:
        if random.uniform(0, 1) > mut_prop:
            continue 
        
        idx = random.randint(0, 4)
        del p["drivers"][idx]
        
        new_driver = df_drivers.sample().to_dict("records")[0]
        p["drivers"].append(new_driver)
        
    return pop


def genetic_algorithm(target_team, race, budget, pop_size, num_generations, verbose=True):
    pop, df_drivers = init(target_team, int(1.5*pop_size), race)
    pop = filter_teams(pop, budget)
    
    for i in range(num_generations):
        pop = crossover(pop, 0.50)
        pop = mutation(pop, df_drivers, 0.05)
        pop = filter_teams(pop, budget)
        pop = fitness(pop)
        pop = sort(pop)
        pop = selection(pop, pop_size)
        
        best_score = pop[0]["score"]
        
        if verbose:
            print(f"GEN {i+1:03d}: pop size = {len(pop):04d} | best score = {best_score:04d}")
    
    return pop[0]

if __name__ == "__main__":
    target_team = "ferrari"
    race = None
    budget = 100
    pop_size = 3000
    num_generations = 100
    
    best = genetic_algorithm(target_team, race, budget, pop_size, num_generations, verbose=False)
    summary_team(best)
    

