import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import tsp_parser as tp
import nearest_neighbor as nn
import simulated_annealing as sa
import genetic_algorithm as ga
import two_opt
import matplotlib.pyplot as plt
import numpy as np
import csv
import random

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
FIGURES_DIR = os.path.join(ROOT_DIR, "figures")
EXPERIMENTS_DIR = SCRIPT_DIR

os.makedirs(FIGURES_DIR, exist_ok=True)


def load_csv(filename):
    results = []
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["best"] = float(row["best"])
            row["worst"] = float(row["worst"])
            row["average"] = float(row["average"])
            row["std"] = float(row["std"])
            row["avg_time"] = float(row["avg_time"])
            results.append(row)
    return results

def plot_distance_comparison(results, optimal=426.0):
    algorithms = [r["algorithm"] for r in results]
    averages = [r["average"] for r in results]
    stds = [r["std"] for r in results]

    colors = ["#e74c3c", "#e67e22", "#3498db", "#2980b9", "#2ecc71", "#27ae60"]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(algorithms, averages, yerr=stds, capsize=5,
                  color=colors, edgecolor="black", linewidth=0.5)

    ax.axhline(y=optimal, color="red", linestyle="--", linewidth=1.5, label=f"Optimal ({optimal})")

    for bar, avg, std in zip(bars, averages, stds):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + std + 3,
                f"{avg:.1f}", ha="center", va="bottom", fontsize=9, fontweight="bold")

    ax.set_ylabel("Tour Distance", fontsize=12)
    ax.set_title("Average Tour Distance by Algorithm (eil51)", fontsize=14, fontweight="bold")
    ax.legend(fontsize=11)
    ax.set_ylim(400, max(averages) + 40)
    plt.xticks(rotation=20, ha="right", fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "distance_comparison.pdf"), dpi=300)
    plt.savefig(os.path.join(FIGURES_DIR, "distance_comparison.png"), dpi=300)
    plt.close()
    print("Saved: distance_comparison.pdf/png")

def plot_time_comparison(results):
    algorithms = [r["algorithm"] for r in results]
    times = [r["avg_time"] for r in results]

    colors = ["#e74c3c", "#e67e22", "#3498db", "#2980b9", "#2ecc71", "#27ae60"]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(algorithms, times, color=colors, edgecolor="black", linewidth=0.5)

    for bar, t in zip(bars, times):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                f"{t:.3f}s", ha="center", va="bottom", fontsize=9, fontweight="bold")

    ax.set_ylabel("Time (seconds)", fontsize=12)
    ax.set_title("Average Execution Time by Algorithm (eil51)", fontsize=14, fontweight="bold")
    plt.xticks(rotation=20, ha="right", fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "time_comparison.pdf"), dpi=300)
    plt.savefig(os.path.join(FIGURES_DIR, "time_comparison.png"), dpi=300)
    plt.close()
    print("Saved: time_comparison.pdf/png")


def plot_gap_comparison(results, optimal=426.0):
    algorithms = [r["algorithm"] for r in results]
    gaps = [((r["average"] - optimal) / optimal) * 100 for r in results]

    colors = ["#e74c3c", "#e67e22", "#3498db", "#2980b9", "#2ecc71", "#27ae60"]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(algorithms, gaps, color=colors, edgecolor="black", linewidth=0.5)

    for bar, g in zip(bars, gaps):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                f"{g:.1f}%", ha="center", va="bottom", fontsize=10, fontweight="bold")

    ax.set_ylabel("Gap from Optimal (%)", fontsize=12)
    ax.set_title("Optimality Gap by Algorithm (eil51)", fontsize=14, fontweight="bold")
    ax.axhline(y=0, color="green", linestyle="--", linewidth=1, alpha=0.7)
    plt.xticks(rotation=20, ha="right", fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "gap_comparison.pdf"), dpi=300)
    plt.savefig(os.path.join(FIGURES_DIR, "gap_comparison.png"), dpi=300)
    plt.close()
    print("Saved: gap_comparison.pdf/png")


def plot_route(ax, coords, route, title, color="blue"):
    """Plots a single TSP route on a given axes."""
    x = [coords[city][0] for city in route] + [coords[route[0]][0]]
    y = [coords[city][1] for city in route] + [coords[route[0]][1]]

    ax.plot(x, y, color=color, linewidth=1.2, alpha=0.8)
    ax.scatter([c[0] for c in coords], [c[1] for c in coords],
               c="red", s=30, zorder=5, edgecolors="black", linewidth=0.5)

    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_aspect("equal")


def plot_all_routes(coords, distance):
    routes = {}

    best_nn_cost = float('inf')
    best_nn_route = None
    for s in range(len(coords)):
        cost, route = nn.nearest_neighbor(distance, s)
        if cost < best_nn_cost:
            best_nn_cost = cost
            best_nn_route = route
    routes["Nearest Neighbor"] = (best_nn_route, best_nn_cost)

    opt_cost, opt_route = two_opt.two_opt(best_nn_route, distance)
    routes["NN + 2-Opt"] = (opt_route, opt_cost)

    start = random.randint(0, len(coords) - 1)
    _, init_route = nn.nearest_neighbor(distance, start)
    sa_cost, sa_route = sa.simulated_annealing(distance, init_route)
    routes["Simulated Annealing"] = (sa_route, sa_cost)

    sa_opt_cost, sa_opt_route = two_opt.two_opt(sa_route, distance)
    routes["SA + 2-Opt"] = (sa_opt_route, sa_opt_cost)

    ga_cost, ga_route = ga.genetic_algorithm(distance)
    routes["Genetic Algorithm"] = (ga_route, ga_cost)

    ga_opt_cost, ga_opt_route = two_opt.two_opt(ga_route, distance)
    routes["GA + 2-Opt"] = (ga_opt_route, ga_opt_cost)

    colors = ["#e74c3c", "#e67e22", "#3498db", "#2980b9", "#2ecc71", "#27ae60"]
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    axes = axes.flatten()

    for idx, (name, (route, cost)) in enumerate(routes.items()):
        title = f"{name}\nDistance: {cost:.2f}"
        plot_route(axes[idx], coords, route, title, color=colors[idx])

    plt.suptitle("TSP Route Comparison (eil51)", fontsize=15, fontweight="bold", y=1.01)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "route_comparison.pdf"), dpi=300, bbox_inches="tight")
    plt.savefig(os.path.join(FIGURES_DIR, "route_comparison.png"), dpi=300, bbox_inches="tight")
    plt.close()
    print("Saved: route_comparison.pdf/png")

def plot_best_avg_worst(results, optimal=426.0):
    algorithms = [r["algorithm"] for r in results]
    bests = [r["best"] for r in results]
    averages = [r["average"] for r in results]
    worsts = [r["worst"] for r in results]

    x = np.arange(len(algorithms))
    width = 0.25

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(x - width, bests, width, label="Best", color="#2ecc71", edgecolor="black", linewidth=0.5)
    ax.bar(x, averages, width, label="Average", color="#3498db", edgecolor="black", linewidth=0.5)
    ax.bar(x + width, worsts, width, label="Worst", color="#e74c3c", edgecolor="black", linewidth=0.5)

    ax.axhline(y=optimal, color="red", linestyle="--", linewidth=1.5, label=f"Optimal ({optimal})")

    ax.set_ylabel("Tour Distance", fontsize=12)
    ax.set_title("Best / Average / Worst Distance by Algorithm (eil51)", fontsize=14, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(algorithms, rotation=20, ha="right", fontsize=10)
    ax.legend(fontsize=10)
    ax.set_ylim(400, max(worsts) + 30)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "best_avg_worst.pdf"), dpi=300)
    plt.savefig(os.path.join(FIGURES_DIR, "best_avg_worst.png"), dpi=300)
    plt.close()
    print("Saved: best_avg_worst.pdf/png")

if __name__ == "__main__":
    print("Generating figures...")

    csv_path = os.path.join(EXPERIMENTS_DIR, "eil51_results.csv")
    results = load_csv(csv_path)

    plot_distance_comparison(results)
    plot_time_comparison(results)
    plot_gap_comparison(results)
    plot_best_avg_worst(results)

    print("\nGenerating route plots (running algorithms once)...")
    data_path = os.path.join(ROOT_DIR, "data", "eil51.tsp")
    coords = tp.parse_tsp(data_path)
    distance = tp.distance_calc(coords)
    plot_all_routes(coords, distance)

    print(f"\nAll figures saved to: {FIGURES_DIR}")