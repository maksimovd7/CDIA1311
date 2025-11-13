import math
import random
from typing import List, Tuple

def calculate_tour_cost(tour: List[int], distances: List[List[float]]) -> float:
    """Вычислить длину маршрута (замкнутый цикл)"""
    cost = 0
    n = len(tour)
    for i in range(n):
        cost += distances[tour[i]][tour[(i + 1) % n]]
    return cost

def simulated_annealing_tsp(
    distances: List[List[float]],
    initial_temp: float = 100.0,
    cooling_rate: float = 0.95,
    iterations_per_temp: int = 1000
) -> Tuple[List[int], float, dict]:
    """
    Имитация отжига для задачи коммивояжёра.

    Args:
        distances: матрица расстояний между городами
        initial_temp: начальная температура
        cooling_rate: коэффициент охлаждения
        iterations_per_temp: итераций на температуре

    Returns:
        маршрут, стоимость маршрута, улучшения по температурам
    """
    n = len(distances)
    