import tkinter as tk
from tkinter import filedialog, messagebox
from graph_utils import save_graph

# Example data (replace with actual data as needed)
def get_example_graph_data():
    # Simulate a disk scheduling example
    x_values = [0, 1, 1, 2, 2, 3, 3, 4]
    y_values = [0, 55, 55, 158, 158, 39, 39, 98]
    datapoints = [0, 55, 158, 39, 98]
    return x_values, y_values, datapoints

def save_graph_via_gui(x_values, y_values, datapoints):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.asksaveasfilename(
        defaultextension='.png',
        filetypes=[('PNG Image', '*.png')],
        title='Save Disk Scheduling Graph'
    )
    if file_path:
        label = f"Graph is being made for data points: {datapoints}"
        save_graph(x_values, y_values, file_path, label=label)
        messagebox.showinfo("Success", f"Graph saved as: {file_path}")
    root.destroy()

class DiskSchedulerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Disk Scheduling Graph Saver")
        self.geometry("500x200")
        self.resizable(False, False)
        
        # Example data
        self.x_values, self.y_values, self.datapoints = get_example_graph_data()
        
        # Label
        label_text = f"Graph is being made for data points: {self.datapoints}"
        self.label = tk.Label(self, text=label_text, wraplength=480, fg='blue')
        self.label.pack(pady=20)
        
        # Save Button
        self.save_button = tk.Button(self, text="Save Graph", command=self.save_graph)
        self.save_button.pack(pady=10)
    
    def save_graph(self):
        save_graph_via_gui(self.x_values, self.y_values, self.datapoints)

if __name__ == "__main__":
    app = DiskSchedulerGUI()
    app.mainloop()
