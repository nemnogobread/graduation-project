import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import random
from real_time_distance_calculation_by_two_anchors import calculate_distance
from main_2_nodes_request import make_measurements

anchor1 = 'COM5'
anchor2 = 'COM6'
mobile_device = 'COM3'
pos_anchor1 = 0
pos_anchor2 = 5.0
base_distance_to_anchor1 = -1
base_amplitude_to_anchor1 = -1
n_anchor_1 = -1
base_distance_to_anchor2 = -1
base_amplitude_to_anchor2 = -1
n_anchor_2 = -1
calibration_made = False

def calculate_attenuation_rate(signal_amplitude_0, signal_amplitude_1, distance_0, distance_1):
    n = abs(signal_amplitude_0 - signal_amplitude_1) / (10 * h * math.log10(distance_0/distance_1))
    return abs(n)

class PositioningApp:
    def __init__(self, root, anchor1_pos=0, anchor2_pos=10):
        self.root = root
        self.root.title("Positioning System")

        # Координаты якорей
        self.anchor1_pos = anchor1_pos
        self.anchor2_pos = anchor2_pos

        # Создаем основную рамку
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Кнопки управления
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=10)

        self.btn_script1 = ttk.Button(self.button_frame, text="Измерить текущее положение устройства", command=self.real_time_measurement)
        self.btn_script1.pack(side=tk.LEFT, padx=5)

        self.btn_script2 = ttk.Button(self.button_frame, text="Изобратить на графике общую картину", command=self.show_multiple_measurements)
        self.btn_script2.pack(side=tk.LEFT, padx=5)

        self.btn_script3 = ttk.Button(self.button_frame, text="Make calibration", command=self.run_script3)
        self.btn_script3.pack(side=tk.LEFT, padx=5)

        # Область для графика
        self.figure, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.main_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Инициализация графика
        self.update_plot()

        # Панель состояния
        self.status_var = tk.StringVar(value="Готов к работе")
        status_bar = ttk.Label(self.main_frame, textvariable=self.status_var,
                               relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, padx=5, pady=5)

        # Лог-панель
        self.log_area = ScrolledText(self.main_frame, height=5, wrap=tk.WORD)
        self.log_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log_area.configure(state='disabled')


    def real_time_measurement(self):
        """Запуск скрипта 1: определение текущей позиции устройства"""

        # Без калибровки расстояние нельзя измерить
        if not calibration_made:
            self.update_ui(
                status=f"Необходима калибровка!",
            )
            return

        device_pos = calculate_distance(anchor1, anchor2, mobile_device, pos_anchor1, pos_anchor2,
                                        base_distance_to_anchor1, base_amplitude_to_anchor1, n_anchor_1,
                                        base_distance_to_anchor2, base_amplitude_to_anchor2, n_anchor_2)

        # Обновляем график с новой позицией
        self.update_plot(device_pos=device_pos)

        # Выводим координату в консоль
        print(f"Текущая координата устройства: {device_pos:.2f}")


    def show_multiple_measurements(self):
        """Запуск скрипта 2: сравнение измеренных и истинных координат"""
        # Здесь должен быть ваш реальный скрипт 2
        # Для примера создаем случайные данные
        num_points = 10
        true_positions = np.linspace(self.anchor1_pos, self.anchor2_pos, num_points)
        measured_positions = true_positions + np.random.normal(0, 0.5, num_points)

        # Обновляем график с наборами координат
        self.update_plot(true_positions=true_positions, measured_positions=measured_positions)

        # Выводим данные в консоль
        print("Истинные координаты:", true_positions)
        print("Измеренные координаты:", measured_positions)

    def calibrate_two_anchors(self): # TODO

        base_amplitude_to_anchor1 = make_measurements()
        n_anchor1 = calculate_attenuation_rate(base_amplitude_to_anchor1, calibration_amplitude_to_anchor1,
                                               base_distance_to_anchor1, calibration_distance_to_anchor1)


    def update_plot(self, device_pos=None, true_positions=None, measured_positions=None):
        """Обновление графика"""
        self.ax.clear()

        # Рисуем ось между якорями
        self.ax.set_xlim(self.anchor1_pos - 1, self.anchor2_pos + 1)
        self.ax.set_ylim(-0.1, 0.5)
        self.ax.axhline(0, color='black', linewidth=0.5)

        # Отмечаем якоря
        self.ax.plot(self.anchor1_pos, 0, 'ro', markersize=10, label='Якорь 1')
        self.ax.plot(self.anchor2_pos, 0, 'ro', markersize=10, label='Якорь 2')

        # Если есть текущая позиция устройства, отмечаем ее
        if device_pos is not None:
            self.ax.plot(device_pos, 0, 'bo', markersize=8, label='Устройство')
            self.ax.annotate(f'{device_pos:.2f}', (device_pos, 0.05), textcoords="offset points", xytext=(0, 5),
                             ha='center')

        # Если есть наборы координат, рисуем их
        if true_positions is not None and measured_positions is not None:
            self.ax.plot(true_positions, np.zeros_like(true_positions), 'g^', markersize=6, label='Истинные')
            self.ax.plot(measured_positions, np.zeros_like(measured_positions), 'mv', markersize=6, label='Измеренные')

            # Добавляем линии ошибок
            for t, m in zip(true_positions, measured_positions):
                self.ax.plot([t, m], [0, 0], 'r--', linewidth=0.5, alpha=0.3)

        self.ax.set_title("Позиционирование устройства между якорями")
        self.ax.set_xlabel("Координата по оси X")
        self.ax.legend(loc='upper right')
        self.ax.grid(True, linestyle='--', alpha=0.5)

        # Убираем ось Y
        self.ax.set_yticks([])

        self.canvas.draw()

    def update_ui(self, status=None, log=None):
        """Обновляет интерфейс"""
        if status:
            self.status_var.set(status)
        if log:
            self.log_area.configure(state='normal')
            self.log_area.insert(tk.END, log + "\n")
            self.log_area.configure(state='disabled')
            self.log_area.see(tk.END)
        self.root.update_idletasks()


if __name__ == "__main__":
    root = tk.Tk()
    app = PositioningApp(root, anchor1_pos=0, anchor2_pos=5)
    root.mainloop()