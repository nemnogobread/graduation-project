import tkinter as tk
from tkinter import ttk, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

from main_2_nodes_request import make_signal_measurements
from real_time_distance_calculation import calculate_distance
from triangulate_position import one_axe_triangulate, two_axe_triangilate
from config_manager import load_config, save_config, get_default_config


def calculate_attenuation_rate(signal_amplitude_0, signal_amplitude_1, distance_0, distance_1):
    h = 21 * 1e-3
    n = abs(signal_amplitude_0 - signal_amplitude_1) / (10 * h * math.log10(distance_0/distance_1))
    return abs(n)


class PositioningInterface:
    def __init__(self, root):
        self.root = root
        self.load_settings()

        self.root.title("Система позиционирования")
        self.root.geometry("900x800")

        self.current_anchor = ""
        self.current_distance = 0.0
        self.mobile_device_position = [0.0, 0.0]

        # Создаем основные фреймы
        self.create_graph_frame()
        self.create_calibration_frame()
        self.create_console_frame()


    def load_settings(self):
        config = load_config() or get_default_config()

        self.anchor1 = config['anchor1']
        self.anchor2 = config['anchor2']
        self.mobile_device = config['mobile_device']
        self.start_signal = config['start_signal']
        self.anchor_position = config['anchor_position']
        self.base_distance = config['base_distance']
        self.base_amplitude = config['base_amplitude']
        self.calibration_amplitude = config['calibration_amplitude']
        self.calibration_distance = config['calibration_distance']
        self.distance = config['distance']
        self.n_rate = config['n_rate']


    def save_settings(self):
        config = {
            "anchor1": self.anchor1,
            "anchor2": self.anchor2,
            "mobile_device": self.mobile_device,
            "start_signal": self.start_signal,
            "anchor_position": self.anchor_position,
            "base_distance": self.base_distance,
            "base_amplitude": self.base_amplitude,
            "calibration_amplitude": self.calibration_amplitude,
            "calibration_distance": self.calibration_distance,
            "distance": self.distance,
            "n_rate": self.n_rate
        }
        save_config(config)


    def create_graph_frame(self):
        """Фрейм для отображения графика"""
        graph_frame = ttk.LabelFrame(self.root, text="Система координат", padding=10)
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Создаем график (может быть 1D или 2D)
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Кнопка определения координат
        btn_frame = ttk.Frame(graph_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            btn_frame, 
            text="Определение координат", 
            command=self.calculate_position
        ).pack(side=tk.LEFT, padx=5)
        
    def create_calibration_frame(self):
        """Фрейм для калибровки"""
        calib_frame = ttk.LabelFrame(self.root, text="Калибровка узла", padding=10)
        calib_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Поле для имени узла
        ttk.Label(calib_frame, text="Имя узла (COM порт):").grid(row=0, column=0, sticky=tk.W)
        self.anchor_entry = ttk.Entry(calib_frame)
        self.anchor_entry.grid(row=0, column=1, sticky=tk.EW, padx=5)
        
        # Поле для расстояния
        ttk.Label(calib_frame, text="Расстояние (м):").grid(row=1, column=0, sticky=tk.W)
        self.distance_entry = ttk.Entry(calib_frame)
        self.distance_entry.grid(row=1, column=1, sticky=tk.EW, padx=5)
        
        # Кнопка сохранения параметров
        ttk.Button(
            calib_frame, 
            text="Сохранить параметры", 
            command=self.save_calibration
        ).grid(row=2, column=0, columnspan=2, pady=5)
        
        # Кнопки калибровки
        btn_calib_frame = ttk.Frame(calib_frame)
        btn_calib_frame.grid(row=3, column=0, columnspan=2, sticky=tk.EW)
        
        ttk.Button(
            btn_calib_frame, 
            text="1. Базовая амплитуда", 
            command=self.calculate_base_amplitude
        ).pack(side=tk.LEFT, padx=2, expand=True)
        
        ttk.Button(
            btn_calib_frame, 
            text="2. Калибровочная амплитуда", 
            command=self.calculate_calib_amplitude
        ).pack(side=tk.LEFT, padx=2, expand=True)
        
        ttk.Button(
            btn_calib_frame, 
            text="3. Коэффициент затухания", 
            command=self.calculate_attenuation
        ).pack(side=tk.LEFT, padx=2, expand=True)
        
    def create_console_frame(self):
        """Фрейм для консоли вывода"""
        console_frame = ttk.LabelFrame(self.root, text="Системная информация", padding=10)
        console_frame.pack(fill=tk.BOTH, padx=5, pady=5)
        
        self.console = scrolledtext.ScrolledText(
            console_frame, 
            wrap=tk.WORD, 
            height=8,
            state='disabled'
        )
        self.console.pack(fill=tk.BOTH, expand=True)
        

    # Методы для обработчиков
    def save_calibration(self):
        """Сохранение параметров калибровки"""
        self.current_anchor = self.anchor_entry.get()
        try:
            self.current_distance = float(self.distance_entry.get())
            self.log_message(f"Параметры сохранены: узел {self.current_anchor}, расстояние {self.current_distance} м")
        except ValueError:
            self.log_message("Ошибка: расстояние должно быть числом", "error")
    

    def calculate_position(self):
        for anchor in self.distance:
            self.distance[anchor] = calculate_distance(anchor, self.mobile_device, self.base_distance[anchor], self.base_amplitude[anchor], self.n_rate[anchor], self.start_signal[anchor])
        if len(self.anchor_position[self.anchor1]) == 1:
            self.mobile_device_position = one_axe_triangulate(self.anchor_position, self.distance)
            self.log_message(f"Координата {self.mobile_device}: {self.mobile_device_position[0]:.2f}")
            self.update_graph(self.mobile_device_position)
        else:
            self.mobile_device_position = two_axe_triangilate(self.anchor_position, self.distance)
            self.log_message(f"Координата {self.mobile_device}: {self.mobile_device_position['position'][0]:.2f}, {self.mobile_device_position['position'][1]:.2f}")
            self.update_graph(self.mobile_device_position['position'])
        

    def calculate_base_amplitude(self):
        """Базовая амплитуда"""
        self.base_amplitude[self.current_anchor] = make_signal_measurements(self.mobile_device, self.start_signal.get(self.current_anchor))
        self.base_distance[self.current_anchor] = self.current_distance
        self.log_message(f"Базовая амлитуда {self.current_anchor}: {self.base_amplitude[self.current_anchor]:.2f} для расстояния {self.base_distance[self.current_anchor]} м")
        self.save_settings()

    def calculate_calib_amplitude(self):
        """Калибровочная амплитуда"""
        self.calibration_amplitude[self.current_anchor] = make_signal_measurements(self.mobile_device, self.start_signal[self.current_anchor])
        self.calibration_distance[self.current_anchor] = self.current_distance
        self.log_message(f"Калибровочная амлитуда {self.current_anchor}: {self.calibration_amplitude[self.current_anchor]:.2f} для расстояния {self.calibration_distance[self.current_anchor]} м")
        self.save_settings()


    def calculate_attenuation(self):
        """Коэффициент затухания"""
        self.n_rate[self.current_anchor] = calculate_attenuation_rate(self.base_amplitude[self.current_anchor], self.calibration_amplitude[self.current_anchor],
                                                            self.base_distance[self.current_anchor], self.calibration_distance[self.current_anchor])
        self.log_message(f"Коэффициент затухания {self.current_anchor}: {self.n_rate[self.current_anchor]:.2f}")
        self.save_settings()


    def log_message(self, message, level="info"):
        """Вывод сообщения в консоль"""
        self.console.configure(state='normal')
        
        # Цвета для разных уровней сообщений
        if level == "error":
            tag = "red"
            self.console.tag_config(tag, foreground="red")
        elif level == "warning":
            tag = "orange"
            self.console.tag_config(tag, foreground="orange")
        else:
            tag = "black"
        
        self.console.insert(tk.END, message + "\n", tag)
        self.console.configure(state='disabled')
        self.console.see(tk.END)
        

    def update_graph(self, mobile_device_position):
        self.ax.clear()
        
        # Определяем размерность (1D или 2D)
        first_anchor = next(iter(self.anchor_position.values()))
        is_2d = (len(first_anchor) == 2)
        
        # Рисуем якоря
        for com, pos in self.anchor_position.items():
            if is_2d:
                self.ax.scatter(pos[0], pos[1], c='green', marker='s', s=200, label=f'Якорь {com}')
            else:
                self.ax.scatter(pos[0], 0, c='green', marker='s', s=200, label=f'Якорь {com}')
        
        # Рисуем мобильное устройство
        if is_2d:
            self.ax.scatter(mobile_device_position[0], mobile_device_position[1], 
                        c='red', s=100, label='Устройство')
        else:
            self.ax.scatter(mobile_device_position[0], 0, 
                        c='red', s=100, label='Устройство')
        
        # Настройки графика
        if is_2d:
            self.ax.set_xlabel('X координата')
            self.ax.set_ylabel('Y координата')
            
            # Автомасштабирование с запасом 10%
            all_x = [pos[0] for pos in self.anchor_position.values()] + [mobile_device_position[0]]
            all_y = [pos[1] for pos in self.anchor_position.values()] + [mobile_device_position[1]]
            
            x_padding = (max(all_x) - min(all_x)) * 0.1
            y_padding = (max(all_y) - min(all_y)) * 0.1
            
            self.ax.set_xlim(min(all_x) - x_padding, max(all_x) + x_padding)
            self.ax.set_ylim(min(all_y) - y_padding, max(all_y) + y_padding)
        else:
            self.ax.set_xlabel('Координата')
            self.ax.set_ylabel('')
            self.ax.set_yticks([])
            
            all_x = [pos[0] for pos in self.anchor_position.values()] + [mobile_device_position[0]]
            x_padding = (max(all_x) - min(all_x)) * 0.1
            self.ax.set_xlim(min(all_x) - x_padding, max(all_x) + x_padding)
            self.ax.set_ylim(-0.5, 0.5)
        
        self.ax.grid(True, linestyle='--', alpha=0.5)
        self.ax.legend()
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = PositioningInterface(root)
    root.mainloop()