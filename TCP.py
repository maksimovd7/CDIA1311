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
    # Случайный стартовый маршрут
    current_tour = list(range(n))
    random.shuffle(current_tour)
    current_cost = calculate_tour_cost(current_tour, distances)
    best_tour = current_tour[:]
    best_cost = current_cost
    temperature = initial_temp
    improvements_by_temperature = {}

    while temperature > 1e-2:
        improvements = 0
        for _ in range(iterations_per_temp):
            # 2-opt обмен
            neighbor_tour = current_tour[:]
            i, j = sorted(random.sample(range(n), 2))
            neighbor_tour[i:j+1] = reversed(neighbor_tour[i:j+1])
            neighbor_cost = calculate_tour_cost(neighbor_tour, distances)
            delta = neighbor_cost - current_cost
            if delta < 0 or random.random() < math.exp(-delta / temperature):
                current_tour = neighbor_tour
                current_cost = neighbor_cost
                if current_cost < best_cost:
                    best_tour = current_tour[:]
                    best_cost = current_cost
                    improvements += 1
        improvements_by_temperature[round(temperature, 2)] = improvements
        temperature *= cooling_rate
    return best_tour, best_cost, improvements_by_temperature

def input_distance_matrix(n: int) -> List[List[float]]:
    """Ручной ввод матрицы расстояний"""
    print(f"Введите матрицу расстояний для {n} городов, по строкам (через пробел, {n} чисел в строке):")
    distances = []
    for i in range(n):
        row = list(map(float, input(f"Строка {i+1}: ").strip().split()))
        if len(row) != n:
            print(f"Ошибка: Введите ровно {n} чисел в строке!")
            return input_distance_matrix(n)
        distances.append(row)
    return distances

if __name__ == "__main__":
    n = 8  # Количество городов фиксировано по задаче
    distances = input_distance_matrix(n)
    initial_temp = 100.0      # Начальная температура
    cooling_rate = 0.95       # Коэффициент охлаждения
    iterations_per_temp = 1000

    tour, cost, improvements = simulated_annealing_tsp(
        distances,
        initial_temp=initial_temp,
        cooling_rate=cooling_rate,
        iterations_per_temp=iterations_per_temp
    )
    print("Лучший маршрут:", ' -> '.join(str(c) for c in tour))
    print("Стоимость маршрута:", cost)
    print("\nКоличество улучшений на разных температурах:")
    for temp, count in improvements.items():
        print(f"Температура {temp}: улучшений {count}")

    
