def one_axe_triangulate(anchor_positions, distances): 
    
    if anchor_positions.keys() != distances.keys():
        raise ValueError("Ключи в position и distances не совпадают")
    
    # Извлекаем границы интервалов
    intervals = [
        (anchor_pos[0] - distances[anchor_name], anchor_pos[0] + distances[anchor_name])
        for anchor_name, anchor_pos in anchor_positions.items()
    ]
    
    # Находим пересечение всех интервалов
    lower_bound = max(interval[0] for interval in intervals)
    upper_bound = min(interval[1] for interval in intervals)
    
    # if lower_bound > upper_bound:
    #     raise ValueError("Нет пересечения интервалов - проверьте корректность расстояний")

    return [(lower_bound + upper_bound) / 2]


def two_axe_triangilate(anchor_positions, distances):
    """
    2D min-max локализация с использованием словарей
    
    Args:
        anchor_positions: {"COM5": [x1,y1], "COM6": [x2,y2], ...} - координаты маяков
        distances: {"COM5": d1, "COM6": d2, ...} - расстояния до устройства
    
    Returns:
        dict: {
            'position': [x, y],       # Центр ограничивающего прямоугольника
            'bounds': {                # Границы области
                'x_min': float,
                'x_max': float,
                'y_min': float,
                'y_max': float
            },
            'accuracy': [dx, dy]      # Погрешность по осям
        }
    
    Raises:
        ValueError: если нет пересечения или несоответствие ключей
    """
    # Проверка соответствия ключей
    if anchor_positions.keys() != distances.keys():
        raise ValueError("Ключи в anchor_positions и distances не совпадают")
    
    # Извлекаем границы для каждой оси
    x_bounds = []
    y_bounds = []
    
    for com, pos in anchor_positions.items():
        d = distances[com]
        x_bounds.append((pos[0] - d, pos[0] + d))  # min_x, max_x для текущего маяка
        y_bounds.append((pos[1] - d, pos[1] + d))  # min_y, max_y для текущего маяка
    
    # Находим пересечение всех прямоугольников
    x_min = max(b[0] for b in x_bounds)
    x_max = min(b[1] for b in x_bounds)
    y_min = max(b[0] for b in y_bounds)
    y_max = min(b[1] for b in y_bounds)
    
    # Проверка на существование решения
    if x_min > x_max or y_min > y_max:
        raise ValueError("Нет пересечения прямоугольников - проверьте входные данные")
    
    # Рассчитываем центр и погрешность
    center_x = (x_min + x_max) / 2
    center_y = (y_min + y_max) / 2
    accuracy_x = (x_max - x_min) / 2
    accuracy_y = (y_max - y_min) / 2
    
    return {
        'position': [center_x, center_y],
        'bounds': {
            'x_min': x_min,
            'x_max': x_max,
            'y_min': y_min,
            'y_max': y_max
        },
        'accuracy': [accuracy_x, accuracy_y]
    }