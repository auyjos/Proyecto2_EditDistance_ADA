"""
Generador de entradas de prueba para Edit Distance.

Produce 35 entradas organizadas en 5 grupos:
  A (1-5):   Casos triviales y base
  B (6-10):  Cadenas pequeñas similares
  C (11-15): Cadenas pequeñas muy diferentes (peor caso DaC)
  D (16-25): Tamaños crecientes para medir DaC (exponencial)
  E (26-35): Tamaños crecientes solo para DP (polinomial)
"""

import random

SEED = 42
ALPHABET = "abcd"  # Alfabeto pequeño para maximizar diferencias


def generate_random_string(length: int, rng: random.Random) -> str:
    """Genera cadena aleatoria sobre un alfabeto pequeño."""
    return "".join(rng.choice(ALPHABET) for _ in range(length))


def get_test_inputs() -> list[dict]:
    """
    Retorna lista de 35 entradas de prueba.

    Cada entrada es un diccionario con:
        id, group, x, y, m, n, expected (None si no se conoce), description
    """
    rng = random.Random(SEED)
    inputs = []

    def add(id_: int, group: str, x: str, y: str,
            expected: int | None, desc: str):
        inputs.append({
            "id": id_,
            "group": group,
            "x": x,
            "y": y,
            "m": len(x),
            "n": len(y),
            "expected": expected,
            "description": desc,
        })

    # --- Grupo A: Casos triviales y base ---
    add(1,  "A", "",      "",      0, "Ambas vacías")
    add(2,  "A", "",      "abc",   3, "Fuente vacía")
    add(3,  "A", "xyz",   "",      3, "Destino vacío")
    add(4,  "A", "a",     "a",     0, "Un carácter igual")
    add(5,  "A", "a",     "b",     1, "Un carácter diferente")

    # --- Grupo B: Cadenas pequeñas similares ---
    add(6,  "B", "abc",    "abc",    0, "Idénticas")
    add(7,  "B", "abc",    "abd",    1, "Un reemplazo")
    add(8,  "B", "abc",    "abcd",   1, "Una inserción")
    add(9,  "B", "abcd",   "abc",    1, "Una eliminación")
    add(10, "B", "kitten", "sitting", 3, "Ejemplo clásico")

    # --- Grupo C: Cadenas pequeñas muy diferentes (peor caso DaC) ---
    add(11, "C", "abc",    "xyz",    3, "Completamente diferentes")
    add(12, "C", "abcde",  "vwxyz",  5, "Todas diferentes")
    add(13, "C", "aaaa",   "bbbb",   4, "Todas diferentes, repetidas")
    add(14, "C", "abcdef", "fedcba", 6, "Invertida")
    add(15, "C", "aabbcc", "xxyyzz", 6, "Todas diferentes, pares")

    # --- Grupo D: Tamaños crecientes para DaC ---
    for i, size in enumerate(range(4, 14), start=16):
        x = generate_random_string(size, rng)
        y = generate_random_string(size, rng)
        add(i, "D", x, y, None, f"Random m=n={size} (DaC benchmark)")

    # --- Grupo E: Tamaños crecientes solo para DP ---
    dp_sizes = [50, 100, 200, 500, 1000, 2000, 5000]
    for i, size in enumerate(dp_sizes, start=26):
        x = generate_random_string(size, rng)
        y = generate_random_string(size, rng)
        add(i, "E", x, y, None, f"Random m=n={size} (DP benchmark)")

    # Casos asimétricos
    add(33, "E",
        generate_random_string(100, rng),
        generate_random_string(500, rng),
        None, "Asimétrico m=100, n=500")
    add(34, "E",
        generate_random_string(10, rng),
        generate_random_string(1000, rng),
        None, "Asimétrico m=10, n=1000")
    add(35, "E", "a" * 500, "b" * 500, 500,
        "Peor caso DP: todo diferente")

    return inputs


if __name__ == "__main__":
    for inp in get_test_inputs():
        x_preview = inp["x"][:20] + "..." if len(inp["x"]) > 20 else inp["x"]
        y_preview = inp["y"][:20] + "..." if len(inp["y"]) > 20 else inp["y"]
        print(f"#{inp['id']:2d} [{inp['group']}] "
              f"m={inp['m']:5d} n={inp['n']:5d} "
              f"x={x_preview!r:25s} y={y_preview!r:25s} "
              f"| {inp['description']}")
