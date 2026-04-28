import ttkbootstrap as ttk
import tkinter as tk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.animation import FuncAnimation
import time
import threading
from matplotlib import cm
from graph_utils import save_graph

class SimulationPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Header with back button
        header = ttk.Frame(self)
        header.pack(fill=tk.X, pady=10)
        
        back_btn = ttk.Button(header, text="\u2190 Back", 
                            command=lambda: controller.show_frame(controller.frames.keys().__iter__().__next__()),
                            bootstyle="light-outline")
        back_btn.pack(side=tk.LEFT, padx=10)
        
        title = ttk.Label(header, text="Disk Scheduling Simulation", 
                         font=('Helvetica', 18))
        title.pack(side=tk.LEFT, expand=True)
        
        # Main content
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - controls
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Input controls
        input_frame = ttk.Labelframe(control_frame, text="Input Parameters", padding=10)
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_frame, text="Head Position:").grid(row=0, column=0, sticky=tk.W)
        self.head_entry = ttk.Entry(input_frame)
        self.head_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(input_frame, text="Request Sequence:").grid(row=1, column=0, sticky=tk.W)
        self.request_entry = ttk.Entry(input_frame)
        self.request_entry.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(input_frame, text="Disk Size:").grid(row=2, column=0, sticky=tk.W)
        self.disk_size_entry = ttk.Entry(input_frame)
        self.disk_size_entry.insert(0, "200")
        self.disk_size_entry.grid(row=2, column=1, padx=5, pady=2)
        
        # Algorithm selection
        algo_frame = ttk.Labelframe(control_frame, text="Algorithms", padding=10)
        algo_frame.pack(fill=tk.X, pady=5)
        
        self.algo_var = tk.StringVar()
        algorithms = ["FCFS", "SSTF", "SCAN", "C-SCAN", "LOOK", "C-LOOK"]
        for i, algo in enumerate(algorithms):
            ttk.Radiobutton(algo_frame, text=algo, variable=self.algo_var, 
                          value=algo, command=self.algorithm_selected).grid(row=i//2, column=i%2, sticky=tk.W)
        
        # Action buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Run All", command=self.run_all_algorithms, 
                  bootstyle="success").pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Visualize", command=self.visualize_algorithm, 
                  bootstyle="info").pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="3D Simulation", command=self.start_3d_simulation, 
                  bootstyle="warning").pack(side=tk.LEFT, padx=2)
        
        # Results display
        results_frame = ttk.Labelframe(control_frame, text="Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.results_text = tk.Text(results_frame, height=10, width=40)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Right panel - visualization
        viz_frame = ttk.Frame(main_frame)
        viz_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create figure for visualization
        self.figure = plt.Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Save Graph Button
        self.save_graph_button = ttk.Button(viz_frame, text="Save Graph", command=self.save_current_graph, bootstyle="primary-outline")
        self.save_graph_button.pack(pady=5)
        
        # Speed control
        speed_frame = ttk.Frame(control_frame)
        speed_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(speed_frame, text="Speed:").pack(side=tk.LEFT)
        self.speed_slider = ttk.Scale(speed_frame, from_=100, to=2000, 
                                    command=self.update_speed)
        self.speed_slider.set(500)
        self.speed_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Animation control buttons
        anim_frame = ttk.Frame(control_frame)
        anim_frame.pack(fill=tk.X, pady=5)
        
        self.start_btn = ttk.Button(anim_frame, text="Start", command=self.start_animation,
                                  bootstyle="success-outline")
        self.start_btn.pack(side=tk.LEFT, padx=2)
        
        self.pause_btn = ttk.Button(anim_frame, text="Pause", command=self.pause_animation,
                                  bootstyle="warning-outline", state=tk.DISABLED)
        self.pause_btn.pack(side=tk.LEFT, padx=2)
        
        self.reset_btn = ttk.Button(anim_frame, text="Reset", command=self.reset_animation,
                                  bootstyle="danger-outline")
        self.reset_btn.pack(side=tk.LEFT, padx=2)
        
        # Initialize animation variables
        self.animation = None
        self.animation_running = False
        self.current_step = 0

    def setup_visualization(self):
        self.figure.clf()
        self.ax = self.figure.add_subplot(111)
        self.canvas.draw()
    
    def run_all_algorithms(self):
        try:
            head = int(self.head_entry.get())
            requests = list(map(int, self.request_entry.get().split()))
            disk_size = int(self.disk_size_entry.get())
            
            if head < 0 or head >= disk_size or any(r < 0 or r >= disk_size for r in requests):
                messagebox.showerror("Error", "Invalid request or head position")
                return
            
            self.controller.algorithms = {
                "FCFS": self.fcfs(requests, head),
                "SSTF": self.sstf(requests, head),
                "SCAN": self.scan(requests, head, disk_size),
                "C-SCAN": self.c_scan(requests, head, disk_size),
                "LOOK": self.look(requests, head),
                "C-LOOK": self.c_look(requests, head),
            }
            
            self.display_results()
            self.plot_comparison_charts()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")
    
    def display_results(self):
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        for name, (seq, seek_time) in self.controller.algorithms.items():
            self.results_text.insert(tk.END, f"{name}:\n")
            self.results_text.insert(tk.END, f"Seek Time: {seek_time}\n")
            self.results_text.insert(tk.END, f"Sequence: {seq}\n\n")
        self.results_text.config(state=tk.DISABLED)
    
    def plot_comparison_charts(self):
        self.figure.clf()
        
        # Bar chart
        ax1 = self.figure.add_subplot(121)
        names = list(self.controller.algorithms.keys())
        seek_times = [val[1] for val in self.controller.algorithms.values()]
        colors = plt.cm.viridis(np.linspace(0, 1, len(names)))
        bars = ax1.bar(names, seek_times, color=colors)
        ax1.set_title("Seek Time Comparison")
        ax1.set_ylabel("Seek Time")
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom')
        
        # Pie chart
        ax2 = self.figure.add_subplot(122)
        ax2.pie(seek_times, labels=names, autopct='%1.1f%%', 
               colors=colors, startangle=90)
        ax2.set_title("Seek Time Distribution")
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def algorithm_selected(self):
        self.controller.current_algorithm = self.algo_var.get()
    
    def visualize_algorithm(self):
        if not self.controller.current_algorithm or not self.controller.algorithms:
            messagebox.showerror("Error", "Please run algorithms and select one to visualize")
            return
        
        seq, _ = self.controller.algorithms[self.controller.current_algorithm]
        
        self.figure.clf()
        self.ax = self.figure.add_subplot(111)
        self.line, = self.ax.plot([], [], 'ro-', markersize=8)
        
        self.ax.set_xlim(0, len(seq)-1)
        self.ax.set_ylim(0, max(seq)+20)
        self.ax.set_title(f"{self.controller.current_algorithm} Head Movement")
        self.ax.set_xlabel("Step")
        self.ax.set_ylabel("Track Position")
        self.ax.grid(True)
        
        self.sequence = seq
        self.current_step = 0
        
        self.canvas.draw()
    
    def start_animation(self):
        if not hasattr(self, 'sequence'):
            return
            
        if self.animation_running:
            return
            
        self.animation_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.NORMAL)
        
        def animation_loop():
            while self.animation_running and self.current_step < len(self.sequence):
                x_data = list(range(self.current_step+1))
                y_data = self.sequence[:self.current_step+1]
                
                self.line.set_data(x_data, y_data)
                self.canvas.draw()
                
                self.current_step += 1
                time.sleep(self.controller.simulation_speed / 1000)
            
            self.animation_running = False
            self.start_btn.config(state=tk.NORMAL)
            self.pause_btn.config(state=tk.DISABLED)
        
        threading.Thread(target=animation_loop, daemon=True).start()
    
    def pause_animation(self):
        self.animation_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
    
    def reset_animation(self):
        self.pause_animation()
        self.current_step = 0
        if hasattr(self, 'sequence'):
            self.line.set_data([], [])
            self.canvas.draw()
    
    def start_3d_simulation(self):
        if not self.controller.algorithms:
            messagebox.showerror("Error", "Please run algorithms first")
            return
        
        # Create a new window for 3D simulation
        sim_window = ttk.Toplevel(self.controller.root)
        sim_window.title("3D Disk Scheduling Simulation")
        sim_window.geometry("800x600")
        
        # Create figure for 3D visualization
        fig = plt.Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111, projection='3d')
        
        # Prepare data for 3D visualization
        colors = plt.cm.viridis(np.linspace(0, 1, len(self.controller.algorithms)))
        
        max_steps = max(len(seq) for seq, _ in self.controller.algorithms.values())
        
        for i, (name, (seq, _)) in enumerate(self.controller.algorithms.items()):
            x = np.arange(len(seq))
            y = np.array(seq)
            z = np.full_like(x, i)
            
            ax.plot(x, y, z, 'o-', label=name, color=colors[i], markersize=5)
        
        ax.set_xlabel('Time Step')
        ax.set_ylabel('Track Position')
        ax.set_zlabel('Algorithm')
        ax.set_title('3D Algorithm Comparison')
        ax.legend()
        
        # Add to Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=sim_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add controls
        control_frame = ttk.Frame(sim_window)
        control_frame.pack(fill=tk.X)
        
        ttk.Button(control_frame, text="Animate", 
                  command=lambda: self.animate_3d_view(ax, canvas)).pack(side=tk.LEFT)
        
        ttk.Button(control_frame, text="Rotate View", 
                  command=lambda: self.rotate_3d_view(ax, canvas)).pack(side=tk.LEFT)
    
    def animate_3d_view(self, ax, canvas):
        if hasattr(self, 'view_animation_running') and self.view_animation_running:
            return
            
        self.view_animation_running = True
        
        def animation_worker():
            for angle in range(0, 360, 2):
                if not hasattr(self, 'view_animation_running') or not self.view_animation_running:
                    break
                ax.view_init(elev=20, azim=angle)
                canvas.draw()
                time.sleep(0.05)
            self.view_animation_running = False
        
        threading.Thread(target=animation_worker, daemon=True).start()
    
    def rotate_3d_view(self, ax, canvas):
        ax.view_init(elev=30, azim=45)
        canvas.draw()
    
    def update_speed(self, val):
        self.controller.simulation_speed = int(float(val))
    
    # Disk scheduling algorithms (same as before)
    def fcfs(self, requests, head):
        seek_sequence = [head] + requests
        seek_time = sum(abs(seek_sequence[i] - seek_sequence[i-1]) for i in range(1, len(seek_sequence)))
        return seek_sequence, seek_time

    def sstf(self, requests, head):
        requests = requests.copy()
        seek_sequence = [head]
        total_seek_time = 0
        while requests:
            closest = min(requests, key=lambda x: abs(x - head))
            total_seek_time += abs(head - closest)
            head = closest
            seek_sequence.append(head)
            requests.remove(closest)
        return seek_sequence, total_seek_time

    def scan(self, requests, head, disk_size=200):
        requests = sorted(requests)
        left = [r for r in requests if r < head]
        right = [r for r in requests if r >= head]

        seek_sequence = [head] + right + [disk_size-1] + left[::-1] if left else [head] + right
        seek_time = (max(right) - head if right else 0) + disk_size-1 - min(left) if left else 0
        return seek_sequence, seek_time

    def c_scan(self, requests, head, disk_size=200):
        requests = sorted(requests)
        right = [r for r in requests if r >= head]
        left = [r for r in requests if r < head]

        seek_sequence = [head] + right + [disk_size-1, 0] + left if left else [head] + right
        seek_time = (max(right) - head if right else 0) + (disk_size-1) + (max(left) if left else 0)
        return seek_sequence, seek_time

    def look(self, requests, head):
        requests = sorted(requests)
        left = [r for r in requests if r < head]
        right = [r for r in requests if r >= head]

        seek_sequence = [head] + right + left[::-1] if left else [head] + right
        seek_time = (max(right) - head if right else 0) + (max(right) - min(left) if left else 0)
        return seek_sequence, seek_time

    def c_look(self, requests, head):
        requests = sorted(requests)
        right = [r for r in requests if r >= head]
        left = [r for r in requests if r < head]

        seek_sequence = [head] + right + left if left else [head] + right
        seek_time = (max(right) - head if right else 0) + (max(left) - min(left) if left else 0)
        return seek_sequence, seek_time

    def save_current_graph(self):
        # Try to get the current algorithm's sequence for labeling
        algo = getattr(self.controller, 'current_algorithm', None)
        algos = getattr(self.controller, 'algorithms', None)
        if not algo or not algos or algo not in algos:
            messagebox.showerror("Error", "No algorithm sequence available to save.")
            return
        seq, _ = algos[algo]
        datapoints_label = f"Graph is being made for data points: {seq}"
        # Get the current plot data from the axes
        if not hasattr(self, 'ax') or not self.ax.lines:
            messagebox.showerror("Error", "No graph to save.")
            return
        line = self.ax.lines[0]
        x_values = line.get_xdata()
        y_values = line.get_ydata()
        file_path = filedialog.asksaveasfilename(
            defaultextension='.png',
            filetypes=[('PNG Image', '*.png')],
            title='Save Disk Scheduling Graph'
        )
        if file_path:
            save_graph(x_values, y_values, file_path, label=datapoints_label)
            messagebox.showinfo("Success", f"Graph saved as: {file_path}") 
