# Edit Distance: Análisis Empírico DaC vs DP

## Definición del Problema

**Edit Distance** (Distancia de Edición) es el número mínimo de operaciones elementales (inserción, eliminación o reemplazo de un carácter) necesarias para transformar una cadena `x` en otra cadena `y`.

### Ejemplo
- Transformar `"kitten"` en `"sitting"`:
  - `kitten` → `sitten` (replace k→s)
  - `sitten` → `sittin` (replace e→i)
  - `sittin` → `sitting` (insert g)
  - **Distancia: 3**


### Instalación
```bash
pip install -r requirements.txt
```

### Ejecutar benchmarks y generar gráficas
```bash
python main.py
```

## 2. Estructura del Proyecto

```
.
├── main.py                  # Punto de entrada (argumentos: --bench, --plot, --quick)
├── requirements.txt         # Dependencias
├── src/
│   ├── dac.py              # Algoritmo DaC recursivo
│   ├── dp.py               # Algoritmo DP + optimizado
│   ├── inputs.py           # Generador de 35 entradas de prueba
│   ├── benchmark.py        # Medición de tiempos con timeout
│   └── plotting.py         # Generación de gráficas
├── tests/
│   └── test_algorithms.py  # Tests unitarios
└── results/                # Salida (CSV + PNG)
```


## 3. Algoritmos Implementados

### 3.1 Divide and Conquer (DaC)
**Justificación:** El problema cumple la propiedad de subproblemas superpuestos. Se divide en 3 subproblemas según si caracteres coinciden o no.

```
T(m,n) = 3·T(m-1,n-1) + O(1)  [cuando caracteres difieren]
T(0,n) = n  y  T(m,0) = m
```

**Complejidad Teórica:** O(3^(m+n)) - **Exponencial**





