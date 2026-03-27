def edit_distance_dac(x: str, y: str, m: int, n: int) -> int:
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
    return edit_distance_dac(x, y, len(x), len(y))
