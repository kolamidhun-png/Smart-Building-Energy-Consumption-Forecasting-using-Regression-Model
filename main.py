import ttkbootstrap as ttk
from app import DiskSchedulingApp

if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    app = DiskSchedulingApp(root)
    root.mainloop()
