import tsp_parser as tp
import nearest_neighbor as nn
import time

def total_distance(route, distance):
    total = 0
    for i in range(len(route) - 1):
        total += distance[route[i]][route[i + 1]]
    total += distance[route[-1]][route[0]]
    return total

def two_opt(route, distance):
    route = route[:]
    n = len(route)
    improved = True

    while improved:
        improved = False
        for i in range(n - 1):
            for j in range(i + 2, n):
                if j == n - 1 and i == 0:
                    continue

                city_a = route[i]
                city_b = route[i + 1]
                city_c = route[j]
                city_d = route[(j + 1) % n]

                current_cost = distance[city_a][city_b] + distance[city_c][city_d]
                new_cost = distance[city_a][city_c] + distance[city_b][city_d]

                if new_cost < current_cost:
                    route[i + 1:j + 1] = route[i + 1:j + 1][::-1]
                    improved = True

    return total_distance(route, distance), route


if __name__ == "__main__":
    coords = tp.parse_tsp("eil51.tsp")
    distance = tp.distance_calc(coords)

    best_nn_cost = float('inf')
    best_nn_route = None
    for s in range(len(coords)):
        cost, route = nn.nearest_neighbor(distance, s)
        if cost < best_nn_cost:
            best_nn_cost = cost
            best_nn_route = route
    print(f"Nearest Neighbor: {best_nn_cost:.2f}")

    start_time = time.time()
    opt_cost, opt_route = two_opt(best_nn_route, distance)
    elapsed = time.time() - start_time
    print(f"NN + 2-Opt: {opt_cost:.2f}  ({elapsed:.3f}s)")
    print(f"different: %{((best_nn_cost - opt_cost) / best_nn_cost) * 100:.1f}")