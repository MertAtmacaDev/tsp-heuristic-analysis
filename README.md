# TSP Heuristic Algorithm Performance Analysis

A comparative performance analysis of heuristic algorithms for the Travelling Salesman Problem (TSP), developed as a term project for the Algorithm Analysis and Design course at Manisa Celal Bayar University.

## Algorithms

- **Nearest Neighbor (NN)** — Greedy constructive heuristic
- **Simulated Annealing (SA)** — Metaheuristic with geometric cooling schedule
- **Genetic Algorithm (GA)** — Evolutionary approach with Order Crossover (OX)
- **2-Opt** — Local search improvement heuristic
- **Hybrid variants** — NN+2-Opt, SA+2-Opt, GA+2-Opt

## Dataset

[eil51](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/) from TSPLIB — 51 cities, known optimal solution: **426**

## Results (eil51)

| Algorithm | Best | Avg | Worst | Std | Gap% |
|-----------|------|-----|-------|-----|------|
| NN | 482 | 482.00 | 482 | 0.00 | 13.1% |
| NN + 2-Opt | 437 | 437.00 | 437 | 0.00 | 2.6% |
| SA | 439 | 447.90 | 456 | 5.41 | 5.1% |
| SA + 2-Opt | 433 | 446.90 | 462 | 7.93 | 4.9% |
| GA | 459 | 465.00 | 467 | 2.79 | 9.2% |
| GA + 2-Opt | 433 | 441.40 | 443 | 3.04 | 3.6% |

## Project Structure

```
├── data/                  # TSPLIB dataset (eil51.tsp)
├── src/                   # Algorithm implementations
│   ├── tsp_parser.py
│   ├── nearest_neighbor.py
│   ├── simulated_annealing.py
│   ├── genetic_algorithm.py
│   └── two_opt.py
├── experiments/           # Experiment runner and visualization
│   ├── experiments.py
│   └── visualize.py
├── figures/               # Generated charts (PNG)
├── paper/                 # LaTeX source and PDF
│   ├── main.tex
│   ├── references.bib
│   └── figures/           # Generated charts (PDF)
└── requirements.txt
```

## Usage

```bash
pip install -r requirements.txt

# Run experiments (10 runs per stochastic algorithm)
python experiments/experiments.py

# Generate figures
python experiments/visualize.py
```

## Paper

The full report is available in IEEE conference format: [`paper/main.tex`](paper/main.tex)
