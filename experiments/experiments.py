import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import tsp_parser as tp
import nearest_neighbor as nn
import simulated_annealing as sa
import genetic_algorithm as ga
import two_opt
import time
import csv
import random
import numpy as np

ROOT_DIR = os.path.join(os.path.dirname(__file__), "..")

def run_experiments(tsp_file, num_runs=10):
    coords = tp.parse_tsp(tsp_file)
    distance = tp.distance_calc(coords)
    n = len(coords)
    results = []

    print("Running Nearest Neighbor...")
    start_time = time.time()
    best_nn_cost = float('inf')
    best_nn_route = None
    for s in range(n):
        cost, route = nn.nearest_neighbor(distance, s)
        if cost < best_nn_cost:
            best_nn_cost = cost
            best_nn_route = route
    nn_time = time.time() - start_time

    results.append({
        "algorithm": "Nearest Neighbor",
        "best": round(best_nn_cost, 2),
        "worst": round(best_nn_cost, 2),
        "average": round(best_nn_cost, 2),
        "std": 0.0,
        "avg_time": round(nn_time, 4)
    })
    print(f"  Result: {best_nn_cost:.2f}  ({nn_time:.4f}s)")

    print("Running NN + 2-Opt...")
    start_time = time.time()
    opt_cost, opt_route = two_opt.two_opt(best_nn_route, distance)
    opt_time = time.time() - start_time
    total_nn_opt_time = nn_time + opt_time  # include NN time in total

    results.append({
        "algorithm": "NN + 2-Opt",
        "best": round(opt_cost, 2),
        "worst": round(opt_cost, 2),
        "average": round(opt_cost, 2),
        "std": 0.0,
        "avg_time": round(total_nn_opt_time, 4)
    })
    print(f"  Result: {opt_cost:.2f}  ({total_nn_opt_time:.4f}s)")

    print(f"Running Simulated Annealing ({num_runs} runs)...")
    sa_costs = []
    sa_times = []
    for i in range(num_runs):
        start = random.randint(0, n - 1)
        _, init_route = nn.nearest_neighbor(distance, start)

        start_time = time.time()
        cost, route = sa.simulated_annealing(distance, init_route)
        elapsed = time.time() - start_time

        sa_costs.append(cost)
        sa_times.append(elapsed)
        print(f"  Run {i+1}/{num_runs}: {cost:.2f}")

    results.append({
        "algorithm": "Simulated Annealing",
        "best": round(min(sa_costs), 2),
        "worst": round(max(sa_costs), 2),
        "average": round(np.mean(sa_costs), 2),
        "std": round(np.std(sa_costs), 2),
        "avg_time": round(np.mean(sa_times), 4)
    })

    print(f"Running SA + 2-Opt ({num_runs} runs)...")
    sa_opt_costs = []
    sa_opt_times = []
    for i in range(num_runs):
        start = random.randint(0, n - 1)
        _, init_route = nn.nearest_neighbor(distance, start)

        start_time = time.time()
        _, sa_route = sa.simulated_annealing(distance, init_route)
        cost, _ = two_opt.two_opt(sa_route, distance)
        elapsed = time.time() - start_time

        sa_opt_costs.append(cost)
        sa_opt_times.append(elapsed)
        print(f"  Run {i+1}/{num_runs}: {cost:.2f}")

    results.append({
        "algorithm": "SA + 2-Opt",
        "best": round(min(sa_opt_costs), 2),
        "worst": round(max(sa_opt_costs), 2),
        "average": round(np.mean(sa_opt_costs), 2),
        "std": round(np.std(sa_opt_costs), 2),
        "avg_time": round(np.mean(sa_opt_times), 4)
    })

    print(f"Running Genetic Algorithm ({num_runs} runs)...")
    ga_costs = []
    ga_times = []
    for i in range(num_runs):
        start_time = time.time()
        cost, route = ga.genetic_algorithm(distance)
        elapsed = time.time() - start_time

        ga_costs.append(cost)
        ga_times.append(elapsed)
        print(f"  Run {i+1}/{num_runs}: {cost:.2f}")

    results.append({
        "algorithm": "Genetic Algorithm",
        "best": round(min(ga_costs), 2),
        "worst": round(max(ga_costs), 2),
        "average": round(np.mean(ga_costs), 2),
        "std": round(np.std(ga_costs), 2),
        "avg_time": round(np.mean(ga_times), 4)
    })

    print(f"Running GA + 2-Opt ({num_runs} runs)...")
    ga_opt_costs = []
    ga_opt_times = []
    for i in range(num_runs):
        start_time = time.time()
        _, ga_route = ga.genetic_algorithm(distance)
        cost, _ = two_opt.two_opt(ga_route, distance)
        elapsed = time.time() - start_time

        ga_opt_costs.append(cost)
        ga_opt_times.append(elapsed)
        print(f"  Run {i+1}/{num_runs}: {cost:.2f}")

    results.append({
        "algorithm": "GA + 2-Opt",
        "best": round(min(ga_opt_costs), 2),
        "worst": round(max(ga_opt_costs), 2),
        "average": round(np.mean(ga_opt_costs), 2),
        "std": round(np.std(ga_opt_costs), 2),
        "avg_time": round(np.mean(ga_opt_times), 4)
    })

    return results


def save_to_csv(results, filename):
    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["algorithm", "best", "worst", "average", "std", "avg_time"])
        writer.writeheader()
        writer.writerows(results)
    print(f"\nResults saved to: {filename}")


def print_table(results, optimal=426.0):
    print("\n" + "=" * 85)
    print(f"{'Algorithm':<22} {'Best':>8} {'Average':>10} {'Worst':>9} {'Std':>7} {'Time(s)':>9} {'Gap%':>8}")
    print("-" * 85)
    for r in results:
        gap = ((r["average"] - optimal) / optimal) * 100
        print(f"{r['algorithm']:<22} {r['best']:>8.2f} {r['average']:>10.2f} {r['worst']:>9.2f} {r['std']:>7.2f} {r['avg_time']:>9.4f} {gap:>7.1f}%")
    print("=" * 85)
    print(f"Optimal solution: {optimal}")


if __name__ == "__main__":
    print("TSP Heuristic Algorithm Experiments")
    print("Dataset: eil51")

    data_path = os.path.join(ROOT_DIR, "data", "eil51.tsp")
    csv_path = os.path.join(os.path.dirname(__file__), "eil51_results.csv")

    results = run_experiments(data_path, num_runs=10)
    save_to_csv(results, csv_path)
    print_table(results, optimal=426.0)
