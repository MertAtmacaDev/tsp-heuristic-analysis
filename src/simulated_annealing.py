import tsp_parser as tp
import nearest_neighbor as nn
import random
import math

def total_distance(route, distance):
    total = 0
    for i in range(len(route) - 1):
        total += distance[route[i]][route[i + 1]]
    total += distance[route[-1]][route[0]]
    return total

def two_opt_swap(route, i, j):
    new_route = route[:i] + route[i:j + 1][::-1] + route[j + 1:]
    return new_route

def simulated_annealing(distance, initial_route,
                        initial_temp=1000,
                        cooling_rate=0.9995,
                        min_temp=1e-8,
                        max_iter=100000):
    n = len(initial_route)
    current_route = list(initial_route)
    current_cost = total_distance(current_route, distance)

    best_route = list(current_route)
    best_cost = current_cost

    temp = initial_temp
    iteration = 0

    while temp > min_temp and iteration < max_iter:
        i = random.randint(0, n - 2)
        j = random.randint(i + 1, n - 1)

        new_route = two_opt_swap(current_route, i, j)
        new_cost = total_distance(new_route, distance)

        delta = new_cost - current_cost
        # Always accept better solutions sometimes worse ones depending on temperature
        if delta < 0 or random.random() < math.exp(-delta / temp):
            current_route = new_route
            current_cost = new_cost

            if current_cost < best_cost:
                best_cost = current_cost
                best_route = list(current_route)

        temp *= cooling_rate
        iteration += 1

    return best_cost, best_route


if __name__ == "__main__":
    coords = tp.parse_tsp("data/eil51.tsp")
    distance = tp.distance_calc(coords)

    start = random.randint(0, len(coords) - 1)
    nn_cost, nn_route = nn.nearest_neighbor(distance, start)
    print(f"Nearest Neighbor: {nn_cost:.2f}")

    sa_cost, sa_route = simulated_annealing(distance, nn_route)
    print(f"Simulated Annealing: {sa_cost:.2f}")
    print(f"different: %{((nn_cost - sa_cost) / nn_cost) * 100:.1f}")