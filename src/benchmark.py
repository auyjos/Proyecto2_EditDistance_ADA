"""
Módulo de benchmarking para Edit Distance.

Mide tiempos de ejecución de ambos algoritmos (DaC y DP)
sobre las entradas de prueba, con timeout para DaC.
"""

import csv
import time
import signal
import sys
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, TimeoutError as FuturesTimeout

from src.dac import solve_dac
from src.dp import edit_distance_dp

# Timeout en segundos para DaC (evitar bloqueo en entradas grandes)
DAC_TIMEOUT = 60.0

# Número de repeticiones para entradas pequeñas (promediar ruido)
MIN_REPEATS = 3
SMALL_THRESHOLD = 10  # m+n <= este valor se repite varias veces


def _run_dac(x: str, y: str) -> int:
    """Ejecuta DaC en un proceso separado (para poder aplicar timeout)."""
    return solve_dac(x, y)


def measure_time(func, *args, repeats: int = 1) -> float:
    """
    Mide el tiempo de ejecución de func(*args).
    Retorna el tiempo promedio en segundos.
    """
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        result = func(*args)
        end = time.perf_counter()
        times.append(end - start)
    return sum(times) / len(times), result


def benchmark_single(inp: dict, dac_timeout: float = DAC_TIMEOUT) -> dict:
    """
    Ejecuta benchmark para una sola entrada.

    Retorna diccionario con:
        id, m, n, group, description,
        result_dac, time_dac,
        result_dp, time_dp,
        dac_timeout (bool)
    """
    x, y = inp["x"], inp["y"]
    m, n = inp["m"], inp["n"]
    repeats = MIN_REPEATS if (m + n) <= SMALL_THRESHOLD else 1

    # --- DP (siempre se ejecuta) ---
    time_dp, result_dp = measure_time(edit_distance_dp, x, y, repeats=repeats)

    # --- DaC (con timeout) ---
    result_dac = None
    time_dac = None
    dac_timed_out = False

    # Solo intentar DaC si el tamaño es razonable
    max_size = max(m, n)
    if max_size <= 15:
        try:
            with ProcessPoolExecutor(max_workers=1) as executor:
                future = executor.submit(_run_dac, x, y)
                try:
                    result_dac = future.result(timeout=dac_timeout)
                except FuturesTimeout:
                    dac_timed_out = True
                    future.cancel()

            if not dac_timed_out:
                time_dac, result_dac = measure_time(
                    solve_dac, x, y, repeats=repeats
                )
        except Exception:
            dac_timed_out = True
    else:
        dac_timed_out = True

    return {
        "id": inp["id"],
        "group": inp["group"],
        "m": m,
        "n": n,
        "description": inp["description"],
        "result_dp": result_dp,
        "time_dp": time_dp,
        "result_dac": result_dac,
        "time_dac": time_dac,
        "dac_timeout": dac_timed_out,
    }


def run_benchmarks(inputs: list[dict],
                   dac_timeout: float = DAC_TIMEOUT,
                   verbose: bool = True) -> list[dict]:
    """
    Ejecuta benchmarks para todas las entradas.
    Retorna lista de resultados.
    """
    results = []
    for inp in inputs:
        if verbose:
            print(f"  Benchmark #{inp['id']:2d} "
                  f"[{inp['group']}] m={inp['m']:5d} n={inp['n']:5d} "
                  f"- {inp['description']}...", end="", flush=True)

        result = benchmark_single(inp, dac_timeout=dac_timeout)
        results.append(result)

        if verbose:
            dp_ms = result["time_dp"] * 1000
            if result["dac_timeout"]:
                print(f"  DP={dp_ms:.3f}ms  DaC=TIMEOUT/SKIP")
            else:
                dac_ms = result["time_dac"] * 1000
                print(f"  DP={dp_ms:.3f}ms  DaC={dac_ms:.3f}ms")

    return results


def save_results_csv(results: list[dict], filepath: str | Path):
    """Guarda los resultados del benchmark en un archivo CSV."""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "id", "group", "m", "n", "description",
        "result_dp", "time_dp",
        "result_dac", "time_dac",
        "dac_timeout",
    ]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"Resultados guardados en: {filepath}")
