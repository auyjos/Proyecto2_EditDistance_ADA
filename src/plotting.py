from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Backend no interactivo para guardar figuras
import matplotlib.pyplot as plt
import numpy as np


RESULTS_DIR = Path("results")


def plot_dac_times(results: list[dict], output_dir: Path = RESULTS_DIR):
    dac_data = [
        r for r in results
        if not r["dac_timeout"] and r["time_dac"] is not None
    ]
    if not dac_data:
        print("No hay datos de DaC para graficar.")
        return

    pairs = sorted((max(r["m"], r["n"]), r["time_dac"]) for r in dac_data)
    sizes = [p[0] for p in pairs]
    times = [p[1] for p in pairs]

    fig, ax = plt.subplots(figsize=(10, 6), layout="constrained")
    ax.scatter(sizes, times, color="tab:red", zorder=5, label="DaC (empírico)")
    ax.plot(sizes, times, color="tab:red", alpha=0.5, linestyle="--")

    # Curva teórica ajustada: c * 3^n
    if len(sizes) >= 3:
        sizes_arr = np.array(sizes, dtype=float)
        times_arr = np.array(times, dtype=float)
        positive = times_arr > 0
        if positive.sum() >= 2:
            log_times = np.log(times_arr[positive])
            log_theoretical = sizes_arr[positive] * np.log(3)
            c = np.exp(np.mean(log_times - log_theoretical))
            x_fit = np.linspace(min(sizes), max(sizes), 100)
            y_fit = c * 3 ** x_fit
            ax.plot(x_fit, y_fit, color="tab:orange", linestyle="-",
                    alpha=0.7, label=f"Teórico: c·3^n (c={c:.2e})")

    ax.set_yscale("log")
    ax.set_xlabel("Tamaño de entrada (n, con m=n)", fontsize=12)
    ax.set_ylabel("Tiempo (segundos) - escala log", fontsize=12)
    ax.set_title("Edit Distance - DaC: Tiempo vs Tamaño\n"
                 "(Crecimiento exponencial O(3^(m+n)))", fontsize=14)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    output_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_dir / "dac_times.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Gráfica DaC guardada en: {output_dir / 'dac_times.png'}")


def plot_dp_times(results: list[dict], output_dir: Path = RESULTS_DIR):
    dp_data = [r for r in results if r["time_dp"] is not None]
    if not dp_data:
        print("No hay datos de DP para graficar.")
        return

    pairs = sorted((max(r["m"], r["n"]), r["time_dp"]) for r in dp_data)
    sizes = [p[0] for p in pairs]
    times = [p[1] for p in pairs]

    fig, ax = plt.subplots(figsize=(10, 6), layout="constrained")
    ax.scatter(sizes, times, color="tab:blue", zorder=5, label="DP (empírico)")
    ax.plot(sizes, times, color="tab:blue", alpha=0.5, linestyle="--")

    # Curva teórica ajustada: c * n^2
    if len(sizes) >= 3:
        sizes_arr = np.array(sizes, dtype=float)
        times_arr = np.array(times, dtype=float)
        valid = (times_arr > 0) & (sizes_arr > 0)
        if valid.sum() >= 2:
            c = np.mean(times_arr[valid] / (sizes_arr[valid] ** 2))
            x_fit = np.linspace(min(sizes), max(sizes), 100)
            y_fit = c * x_fit ** 2
            ax.plot(x_fit, y_fit, color="tab:cyan", linestyle="-",
                    alpha=0.7, label=f"Teórico: c·n² (c={c:.2e})")

    ax.set_xlabel("Tamaño de entrada (n, con m=n)", fontsize=12)
    ax.set_ylabel("Tiempo (segundos)", fontsize=12)
    ax.set_title("Edit Distance - DP: Tiempo vs Tamaño\n"
                 "(Crecimiento polinomial O(m·n))", fontsize=14)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    output_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_dir / "dp_times.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Gráfica DP guardada en: {output_dir / 'dp_times.png'}")


def plot_comparison(results: list[dict], output_dir: Path = RESULTS_DIR):
    both = [
        r for r in results
        if not r["dac_timeout"]
        and r["time_dac"] is not None
        and r["time_dp"] is not None
    ]
    if not both:
        print("No hay datos comparativos para graficar.")
        return

    pairs = sorted(
        (max(r["m"], r["n"]), r["time_dac"], r["time_dp"]) for r in both
    )
    sizes = [p[0] for p in pairs]
    times_dac = [p[1] for p in pairs]
    times_dp = [p[2] for p in pairs]

    fig, ax = plt.subplots(figsize=(10, 6), layout="constrained")
    ax.scatter(sizes, times_dac, color="tab:red", zorder=5, label="DaC", s=60)
    ax.plot(sizes, times_dac, color="tab:red", alpha=0.5, linestyle="--")
    ax.scatter(sizes, times_dp, color="tab:blue", zorder=5, label="DP", s=60)
    ax.plot(sizes, times_dp, color="tab:blue", alpha=0.5, linestyle="--")

    ax.set_yscale("log")
    ax.set_xlabel("Tamaño de entrada (n, con m=n)", fontsize=12)
    ax.set_ylabel("Tiempo (segundos) - escala log", fontsize=12)
    ax.set_title("Edit Distance - Comparación DaC vs DP\n"
                 "(Exponencial vs Polinomial)", fontsize=14)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    output_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_dir / "comparison.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Gráfica comparativa guardada en: {output_dir / 'comparison.png'}")


def plot_all(results: list[dict], output_dir: Path = RESULTS_DIR):
    """Genera todas las gráficas."""
    plot_dac_times(results, output_dir)
    plot_dp_times(results, output_dir)
    plot_comparison(results, output_dir)
