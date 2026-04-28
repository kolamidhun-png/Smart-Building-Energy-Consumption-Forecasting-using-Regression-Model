import ttkbootstrap as ttk
import tkinter as tk
from algorithm_info import AlgorithmInfoPage
from simulation import SimulationPage

class HomePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Header with enhanced styling
        header = ttk.Frame(self)
        header.pack(fill=tk.X, pady=20)
        
        title = ttk.Label(
            header, 
            text="Disk Scheduling Algorithm Visualizer", 
            font=('Helvetica', 28, 'bold'),
            bootstyle="inverse-primary"
        )
        title.pack()
        
        # Introduction with enhanced styling
        intro_frame = ttk.Frame(self)
        intro_frame.pack(fill=tk.X, padx=50, pady=20)
        
        # Welcome text with custom color
        welcome_text = ttk.Label(
            intro_frame,
            text="Welcome to the Disk Scheduling Algorithm Visualizer!",
            font=('Helvetica', 16, 'bold'),
            bootstyle="info"
        )
        welcome_text.pack(pady=(0, 15))
        
        # Features with bullet points and colors
        features_frame = ttk.Frame(intro_frame)
        features_frame.pack(fill=tk.X)
        
        features = [
            ("📊 Detailed Algorithm Explanations", "primary"),
            ("🎮 Interactive Visualizations", "success"),
            ("🔄 3D Head Movement Simulations", "info"),
            ("📈 Performance Comparisons", "warning")
        ]
        
        for text, style in features:
            feature = ttk.Label(
                features_frame,
                text=text,
                font=('Helvetica', 12),
                bootstyle=style
            )
            feature.pack(anchor=tk.W, pady=5)
        
        # Algorithm Cards with enhanced styling
        card_frame = ttk.Frame(self)
        card_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        algorithms = [
            ("FCFS", "First-Come First-Served", "#3498db", "primary"),
            ("SSTF", "Shortest Seek Time First", "#2ecc71", "success"),
            ("SCAN", "Elevator Algorithm", "#e74c3c", "danger"),
            ("C-SCAN", "Circular SCAN", "#9b59b6", "info"),
            ("LOOK", "Optimized Elevator", "#f39c12", "warning"),
            ("C-LOOK", "Circular LOOK", "#1abc9c", "secondary")
        ]
        
        for i, (name, desc, color, style) in enumerate(algorithms):
            card = ttk.Frame(card_frame, bootstyle="light", padding=15)
            card.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="nsew")
            
            title = ttk.Label(
                card,
                text=name,
                font=('Helvetica', 16, 'bold'),
                bootstyle=f"inverse-{style}"
            )
            title.pack(fill=tk.X, pady=5)
            
            desc_label = ttk.Label(
                card,
                text=desc,
                wraplength=200,
                font=('Helvetica', 11),
                bootstyle=style
            )
            desc_label.pack(fill=tk.X, pady=5)
            
            btn = ttk.Button(
                card,
                text="Learn More",
                command=lambda n=name: self.show_algorithm_info(n),
                bootstyle=style,
                width=15
            )
            btn.pack(pady=5)
        
        # Navigation buttons with enhanced styling
        nav_frame = ttk.Frame(self)
        nav_frame.pack(fill=tk.X, pady=20)
        
        sim_btn = ttk.Button(
            nav_frame,
            text="Go to Simulation",
            command=lambda: controller.show_frame(SimulationPage),
            bootstyle="success",
            width=20
        )
        sim_btn.pack(side=tk.RIGHT, padx=20)
        
        # Configure grid weights
        for i in range(3):
            card_frame.columnconfigure(i, weight=1)
        for i in range(2):
            card_frame.rowconfigure(i, weight=1)
    
    def show_algorithm_info(self, algorithm):
        self.controller.frames[AlgorithmInfoPage].set_algorithm(algorithm)
        self.controller.show_frame(AlgorithmInfoPage)
