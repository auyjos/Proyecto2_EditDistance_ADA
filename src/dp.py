"""
Edit Distance - Programación Dinámica (Bottom-Up con tabulación).

Complejidad temporal: O(m * n).
Complejidad espacial: O(m * n) para la tabla completa.
"""


def edit_distance_dp(x: str, y: str) -> int:
    """
    Calcula la distancia de edición entre x e y usando
    programación dinámica bottom-up (tabulación).

    dp[i][j] = distancia de edición entre x[0..i-1] e y[0..j-1].

    Recurrencia:
        dp[i][0] = i  (eliminar todos los caracteres de x)
        dp[0][j] = j  (insertar todos los caracteres de y)

        Si x[i-1] == y[j-1]:
            dp[i][j] = dp[i-1][j-1]
        Si no:
            dp[i][j] = 1 + min(dp[i-1][j],      # Delete
                                dp[i][j-1],      # Insert
                                dp[i-1][j-1])    # Replace

    Parámetros:
        x: cadena fuente
        y: cadena destino

    Retorna:
        Mínimo número de operaciones para transformar x en y.
    """
    m = len(x)
    n = len(y)

    # Crear tabla de (m+1) x (n+1)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Casos base
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Llenar la tabla fila por fila
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # Delete
                    dp[i][j - 1],      # Insert
                    dp[i - 1][j - 1],  # Replace
                )

    return dp[m][n]


def edit_distance_dp_optimized(x: str, y: str) -> int:
    """
    Versión optimizada en espacio: O(min(m, n)).
    Usa solo dos filas en lugar de la tabla completa.
    """
    # Asegurar que n <= m para usar menos espacio
    if len(x) < len(y):
        x, y = y, x

    m = len(x)
    n = len(y)

    prev = list(range(n + 1))
    curr = [0] * (n + 1)

    for i in range(1, m + 1):
        curr[0] = i
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(prev[j], curr[j - 1], prev[j - 1])
        prev, curr = curr, prev

    return prev[n]


def reconstruct_operations(x: str, y: str) -> list[str]:
    """
    Reconstruye la secuencia de operaciones óptimas
    haciendo backtracking sobre la tabla DP.

    Retorna lista de operaciones en orden.
    """
    m = len(x)
    n = len(y)

    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],
                    dp[i][j - 1],
                    dp[i - 1][j - 1],
                )

    # Backtracking
    ops = []
    i, j = m, n
    while i > 0 and j > 0:
        if x[i - 1] == y[j - 1]:
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i - 1][j - 1] + 1:
            ops.append(f"Replace x[{i-1}]='{x[i-1]}' with '{y[j-1]}'")
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i - 1][j] + 1:
            ops.append(f"Delete x[{i-1}]='{x[i-1]}'")
            i -= 1
        else:
            ops.append(f"Insert '{y[j-1]}' at position {i}")
            j -= 1

    while i > 0:
        ops.append(f"Delete x[{i-1}]='{x[i-1]}'")
        i -= 1
    while j > 0:
        ops.append(f"Insert '{y[j-1]}' at position 0")
        j -= 1

    return list(reversed(ops))
