"""
Punto de entrada principal para el proyecto Edit Distance.

Ejecuta benchmarks, genera gráficas y guarda resultados.

Uso:
    python main.py              # Ejecutar todo (benchmarks + gráficas)
    python main.py --bench      # Solo benchmarks
    python main.py --plot       # Solo gráficas (requiere CSV previo)
    python main.py --quick      # Benchmarks rápidos (solo grupos A-D)
"""

import argparse
import csv
import sys
from pathlib import Path

from src.inputs import get_test_inputs
from src.benchmark import run_benchmarks, save_results_csv
from src.plotting import plot_all

RESULTS_DIR = Path("results")
CSV_PATH = RESULTS_DIR / "benchmark_results.csv"


def load_results_csv(filepath: Path) -> list[dict]:
    """Carga resultados de benchmark desde CSV."""
    results = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["m"] = int(row["m"])
            row["n"] = int(row["n"])
            row["id"] = int(row["id"])
            row["time_dp"] = float(row["time_dp"]) if row["time_dp"] else None
            row["time_dac"] = float(row["time_dac"]) if row["time_dac"] else None
            row["result_dp"] = int(row["result_dp"]) if row["result_dp"] else None
            row["result_dac"] = (
                int(row["result_dac"]) if row["result_dac"] else None
            )
            row["dac_timeout"] = row["dac_timeout"] == "True"
            results.append(row)
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Edit Distance: DaC vs DP - Análisis empírico"
    )
    parser.add_argument("--bench", action="store_true",
                        help="Solo ejecutar benchmarks")
    parser.add_argument("--plot", action="store_true",
                        help="Solo generar gráficas (requiere CSV previo)")
    parser.add_argument("--quick", action="store_true",
                        help="Benchmarks rápidos (solo grupos A-D, sin E)")
    args = parser.parse_args()

    run_bench = not args.plot
    run_plot = not args.bench

    if run_bench:
        print("=" * 60)
        print("  Edit Distance: Benchmarks DaC vs DP")
        print("=" * 60)

        inputs = get_test_inputs()
        if args.quick:
            inputs = [i for i in inputs if i["group"] != "E"]
            print(f"  Modo rápido: {len(inputs)} entradas (sin grupo E)")
        else:
            print(f"  Total de entradas: {len(inputs)}")

        print()
        results = run_benchmarks(inputs)
        save_results_csv(results, CSV_PATH)

        # Resumen
        print()
        print("=" * 60)
        print("  Resumen")
        print("=" * 60)
        dac_ok = [r for r in results if not r["dac_timeout"]]
        print(f"  DaC ejecutado exitosamente: {len(dac_ok)}/{len(results)}")
        print(f"  DP ejecutado: {len(results)}/{len(results)}")

        # Verificar consistencia
        mismatches = [
            r for r in results
            if not r["dac_timeout"]
            and r["result_dac"] is not None
            and r["result_dac"] != r["result_dp"]
        ]
        if mismatches:
            print(f"  ADVERTENCIA: {len(mismatches)} resultados inconsistentes!")
            for r in mismatches:
                print(f"    #{r['id']}: DaC={r['result_dac']} DP={r['result_dp']}")
        else:
            print("  Consistencia: Todos los resultados DaC == DP")

    if run_plot:
        if not CSV_PATH.exists():
            print(f"Error: No se encontró {CSV_PATH}. Ejecute --bench primero.")
            sys.exit(1)

        print()
        print("=" * 60)
        print("  Generando gráficas")
        print("=" * 60)
        results = load_results_csv(CSV_PATH)
        plot_all(results, RESULTS_DIR)

    print()
    print("Listo.")


if __name__ == "__main__":
    main()
