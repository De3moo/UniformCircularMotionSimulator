import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def run(data_sim):
    # Create the main Tkinter window
    root = tk.Tk()
    root.title("Effect of Variables on Centripetal Force")
    root.geometry("1200x800")  # Set the window size

    # Configure the window layout
    root.rowconfigure(0, weight=2)  # Top part for the graphs
    root.rowconfigure(1, weight=1)  # Bottom part for the table
    root.columnconfigure(0, weight=1)

    # Function to plot graphs based on selected variable
    def plot_graph(variable):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        x = []  # Variable values
        acceleration = []  # Centripetal acceleration values
        force = []  # Centripetal force values

        for row in data_sim:
            if variable == "Mass":
                x.append(row[4])  # Mass
            elif variable == "Radius":
                x.append(row[1])  # Radius
            elif variable == "Velocity":
                x.append(row[5])  # Tangential Velocity
            acceleration.append(row[6])  # Centripetal acceleration
            force.append(row[7])  # Centripetal force

        # Plot Centripetal Acceleration
        ax1.plot(x, acceleration, label="Centripetal Acceleration", color="blue")
        ax1.set_xlabel(variable)
        ax1.set_ylabel("Centripetal Acceleration (m/s^2)")
        ax1.set_title(f"Effect of {variable} on Centripetal Acceleration")
        ax1.legend()

        # Plot Centripetal Force
        ax2.plot(x, force, label="Centripetal Force", color="red")
        ax2.set_xlabel(variable)
        ax2.set_ylabel("Centripetal Force (N)")
        ax2.set_title(f"Effect of {variable} on Centripetal Force")
        ax2.legend()

        # Adjust layout
        fig.tight_layout()

        # Clear previous graphs and display the new ones
        for widget in graph_frame.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        canvas.draw()

    # Top Half: Frame for Graphs
    graph_frame = tk.Frame(root)
    graph_frame.grid(row=0, column=0, sticky="nsew")

    # Buttons to select variable to plot
    button_frame = tk.Frame(root)
    button_frame.grid(row=0, column=1, sticky="nsew", padx=10)

    tk.Button(button_frame, text="Mass", command=lambda: plot_graph("Mass")).pack(pady=5)
    tk.Button(button_frame, text="Radius", command=lambda: plot_graph("Radius")).pack(pady=5)
    tk.Button(button_frame, text="Velocity", command=lambda: plot_graph("Velocity")).pack(pady=5)
    
    # Lower Half: Treeview Table
    columns = [
        "Simulation", "Radius (m)", "Angle (rad)", "Angular Velocity (rad/s)", 
        "Mass (kg)", "Tangential Velocity (m/s)", "Centripetal Acceleration (m/s^2)", 
        "Centripetal Force (N)", "Period (s)", "Frequency (Hz)"
    ]
    tree = ttk.Treeview(root, columns=columns, show="headings")

    # Set up table headings
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, stretch=True)

    def populate():
        # Populate the table with simulated data
        for row in data_sim:
            tree.insert("", tk.END, values=row)

    # Place the Treeview widget in the lower half of the window
    tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    populate()

    root.mainloop()
