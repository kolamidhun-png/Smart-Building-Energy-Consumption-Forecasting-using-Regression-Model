import matplotlib.pyplot as plt

def save_graph(x_values, y_values, filename, label=None):
    """
    Plots and saves the disk scheduling graph to the specified filename.
    Args:
        x_values (list): X-axis values (time units)
        y_values (list): Y-axis values (head positions)
        filename (str): Path to save the image file
        label (str, optional): Label to display on the graph
    """
    plt.figure(figsize=(10, 5))
    plt.plot(x_values, y_values, marker='o', linestyle='-', color='b')
    plt.title('Disk Scheduling Head Movement')
    plt.xlabel('Time Unit')
    plt.ylabel('Head Position')
    if label:
        plt.suptitle(label, fontsize=10, y=0.94, color='green')
    plt.grid(True)
    # Annotate each point
    for x, y in zip(x_values, y_values):
        plt.annotate(f'{y}', (x, y), textcoords="offset points", xytext=(0,8), ha='center', fontsize=9, color='red')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
