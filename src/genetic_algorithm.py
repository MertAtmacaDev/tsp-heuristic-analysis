import tsp_parser as tp
import nearest_neighbor as nn
import random

def total_distance(route, distance):
    total = 0
    for i in range(len(route) - 1):
        total += distance[route[i]][route[i + 1]]
    total += distance[route[-1]][route[0]]
    return total

def create_population(pop_size, num_cities, distance):
    population = []

    best_nn_cost = float('inf')
    best_nn_route = None
    for start in range(num_cities):
        cost, route = nn.nearest_neighbor(distance, start)
        if cost < best_nn_cost:
            best_nn_cost = cost
            best_nn_route = route
    #seeding the initial population with the best nn solution to speed up convergence
    population.append(best_nn_route)

    cities = list(range(num_cities))
    for _ in range(pop_size - 1):
        route = cities[:]
        random.shuffle(route)
        population.append(route)

    return population

def tournament_selection(population, distance, tournament_size=5):
    tournament = random.sample(population, tournament_size)
    tournament.sort(key=lambda route: total_distance(route, distance))
    return tournament[0]

def crossover(parent1, parent2):
    size = len(parent1)
    start = random.randint(0, size - 2)
    end = random.randint(start + 1, size - 1)

    child = [None] * size
    child[start:end + 1] = parent1[start:end + 1]

    #maintaining order crossover by filling the remaining positions from parent2
    inherited = set(child[start:end + 1])
    fill_order = [city for city in parent2 if city not in inherited]

    fill_index = 0
    for i in range(size):
        if child[i] is None:
            child[i] = fill_order[fill_index]
            fill_index += 1

    return child

def mutate(route, mutation_rate=0.02):
    route = route[:]
    for i in range(len(route)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(route) - 1)
            route[i], route[j] = route[j], route[i]
    return route

def genetic_algorithm(distance, pop_size=100, generations=500,
                      mutation_rate=0.02, elite_size=5):
    num_cities = len(distance)
    population = create_population(pop_size, num_cities, distance)

    best_route = None
    best_cost = float('inf')

    for gen in range(generations):
        population.sort(key=lambda route: total_distance(route, distance))

        current_cost = total_distance(population[0], distance)
        if current_cost < best_cost:
            best_cost = current_cost
            best_route = population[0][:]

        new_population = []

        for i in range(elite_size):
            new_population.append(population[i])

        while len(new_population) < pop_size:
            parent1 = tournament_selection(population, distance)
            parent2 = tournament_selection(population, distance)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            new_population.append(child)

        population = new_population

        if (gen + 1) % 100 == 0:
            print(f"generation {gen + 1}/{generations} - best: {best_cost:.2f}")

    return best_cost, best_route


if __name__ == "__main__":
    coords = tp.parse_tsp("data/eil51.tsp")
    distance = tp.distance_calc(coords)

    best_nn = float('inf')
    for s in range(len(coords)):
        cost, _ = nn.nearest_neighbor(distance, s)
        if cost < best_nn:
            best_nn = cost
    print(f"Nearest Neighbor best score: {best_nn:.2f}")

    ga_cost, ga_route = genetic_algorithm(distance)
    print(f"\nGenetic Algorithm: {ga_cost:.2f}")
    print(f"different: %{((best_nn - ga_cost) / best_nn) * 100:.1f}")