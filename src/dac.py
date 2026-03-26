"""
Edit Distance - Divide and Conquer (Recursión pura, sin memoización).

Complejidad temporal: O(3^(m+n)) en el peor caso.
Complejidad espacial: O(m+n) por la pila de recursión.
"""


def edit_distance_dac(x: str, y: str, m: int, n: int) -> int:
    """
    Calcula la distancia de edición entre x[0..m-1] e y[0..n-1]
    usando recursión pura (Divide and Conquer).

    Parámetros:
        x: cadena fuente
        y: cadena destino
        m: longitud del prefijo de x a considerar
        n: longitud del prefijo de y a considerar

    Retorna:
        Mínimo número de operaciones (insert, delete, replace) para
        transformar x[0..m-1] en y[0..n-1].
    """
    # Casos base
    if m == 0:
        return n
    if n == 0:
        return m

    # Si los últimos caracteres coinciden, no hay costo
    if x[m - 1] == y[n - 1]:
        return edit_distance_dac(x, y, m - 1, n - 1)

    # Los últimos caracteres difieren: tomar el mínimo de las 3 operaciones
    insert_op = edit_distance_dac(x, y, m, n - 1)
    delete_op = edit_distance_dac(x, y, m - 1, n)
    replace_op = edit_distance_dac(x, y, m - 1, n - 1)

    return 1 + min(insert_op, delete_op, replace_op)


def solve_dac(x: str, y: str) -> int:
    """Wrapper conveniente para edit_distance_dac."""
    return edit_distance_dac(x, y, len(x), len(y))
