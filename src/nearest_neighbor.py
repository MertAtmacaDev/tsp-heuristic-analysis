import tsp_parser as tp
import random

def nearest_neighbor(distance, start_city):
    sorted_city = [start_city]
    visited = {start_city} #using a set instead of list for o(1) lookups instead of o(n)
    total_distance = 0

    for i in range(len(distance)-1):

        current_city = sorted_city[-1]
        min_distance = float('inf')

        for j in range(len(distance)):
            if j in visited:
                continue

            current_distance = distance[current_city][j]
            if min_distance > current_distance:
                min_distance = current_distance
                nearest_city = j
            
        total_distance += min_distance
        sorted_city.append(nearest_city)
        visited.add(nearest_city)

    # closing the loop by returning back to the starting city
    total_distance += distance[sorted_city[-1]][sorted_city[0]]
    return total_distance, sorted_city

if __name__ == "__main__":
    coords = tp.parse_tsp("data/eil51.tsp")
    start_city = random.randint(0,50)
    total_distance, sorted_city = nearest_neighbor(tp.distance_calc(coords), start_city)

    print(total_distance)