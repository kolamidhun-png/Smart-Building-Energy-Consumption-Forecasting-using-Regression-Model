from graph_utils import save_graph
import os
import matplotlib.pyplot as plt

class DiskScheduler:
    def __init__(self):
        # self is used to create instance variables
        self.current_position = 0
        self.requests = []
        self.movement_history = [(0, 0)]  # (time_unit, position) pairs
        self.animation_data = []  # Store detailed movement information
        self.graph_points = []  # Store points for graph plotting
    
    def add_request(self, request):
        if isinstance(request, int) and 0 <= request <= 199:  # Assuming disk positions from 0-199
            self.requests.append(request)
            return True
        return False
    
    def get_current_position(self):
        # self is used to access instance variables
        return self.current_position
    
    def move_head(self, new_position):
        # self is used to modify instance variables
        old_position = self.current_position
        self.current_position = new_position
        time_unit = len(self.movement_history)
        
        # Add the new position to movement history
        self.movement_history.append((time_unit, new_position))
        
        # Store detailed movement information for animation
        movement_info = {
            'from_position': old_position,
            'to_position': new_position,
            'time_unit': time_unit,
            'distance': abs(new_position - old_position)
        }
        self.animation_data.append(movement_info)
        
        # Store graph plotting points
        # Add both points to create a connected line
        self.graph_points.extend([
            {'x': time_unit - 1, 'y': old_position, 'type': 'start'},
            {'x': time_unit, 'y': new_position, 'type': 'end'}
        ])
    
    def get_datapoints(self):
        """Returns the movement history as datapoints for visualization"""
        return self.movement_history
    
    def get_graph_points(self):
        """Returns formatted points for graph plotting"""
        return {
            'x_values': [point['x'] for point in self.graph_points],
            'y_values': [point['y'] for point in self.graph_points],
            'points': self.graph_points
        }
    
    def display_animation_datapoints(self):
        """Displays detailed information about disk head movements for animation"""
        print("\n=== Disk Head Movement Animation Data ===")
        print("\nInitial Position:", self.movement_history[0][1])
        
        total_distance = 0
        print("\nDetailed Movement Sequence:")
        print("Time | From → To | Distance | Running Total")
        print("-" * 45)
        
        for data in self.animation_data:
            total_distance += data['distance']
            print(f"  {data['time_unit']:2d}  |  {data['from_position']:3d} → {data['to_position']:<3d} |    {data['distance']:<4d}   |     {total_distance:<4d}")
        
        print("\nAnimation Summary:")
        print(f"Total Movements: {len(self.animation_data)}")
        print(f"Total Distance Covered: {total_distance} cylinders")
        print(f"Average Seek Distance: {total_distance/len(self.animation_data):.2f} cylinders")
        
        print("\nGraph Plotting Points:")
        print("Time Unit (X) | Head Position (Y)")
        print("-" * 35)
        for point in self.graph_points:
            print(f"     {point['x']:3d}      |       {point['y']:3d}")

# Example demonstration
def demonstrate_disk_scheduling():
    print("=== Disk Scheduling Demonstration with Graph Points ===")
    
    # Create multiple examples with different patterns
    examples = [
        {
            'name': 'Sequential Access Pattern',
            'requests': [20, 45, 65, 85, 105, 125, 145, 165],
            'description': 'Shows steady movement across disk sectors'
        },
        {
            'name': 'Random Access Pattern',
            'requests': [55, 158, 39, 98, 183, 15, 70, 125],
            'description': 'Demonstrates scattered disk access'
        },
        {
            'name': 'Localized Access Pattern',
            'requests': [50, 45, 55, 48, 52, 43, 58, 47],
            'description': 'Shows head movement in a confined area'
        },
        {
            'name': 'Back and Forth Pattern',
            'requests': [25, 180, 30, 175, 35, 170, 40, 165],
            'description': 'Illustrates alternating head movement'
        }
    ]
    
    for example in examples:
        print(f"\n\n{'='*20} {example['name']} {'='*20}")
        print(f"Description: {example['description']}")
        scheduler = DiskScheduler()
        
        print(f"\nProcessing requests: {example['requests']}")
        # Add and process requests
        for req in example['requests']:
            scheduler.add_request(req)
            scheduler.move_head(req)
        
        # Display the animation data and graph points
        scheduler.display_animation_datapoints()
        
        # Show graph coordinates summary
        graph_data = scheduler.get_graph_points()
        print("\nGraph Coordinates Summary:")
        print("X-coordinates:", graph_data['x_values'])
        print("Y-coordinates:", graph_data['y_values'])
        
        # Print label for which data points the graph is being made
        datapoints_label = f"Graph is being made for data points: {[point[1] for point in scheduler.movement_history]}"
        print(f"\n{datapoints_label}")
        
        # Option to save the graph
        default_filename = f"{example['name'].replace(' ', '_').lower()}_graph.png"
        save_path = os.path.join(os.getcwd(), default_filename)
        save_graph(graph_data['x_values'], graph_data['y_values'], save_path, label=datapoints_label)
        print(f"Graph saved as: {save_path}")

        # Show the graph interactively with labels
        plt.figure(figsize=(10, 5))
        plt.plot(graph_data['x_values'], graph_data['y_values'], marker='o', linestyle='-', color='b')
        plt.title('Disk Scheduling Head Movement')
        plt.xlabel('Time Unit')
        plt.ylabel('Head Position')
        plt.suptitle(datapoints_label, fontsize=10, y=0.94, color='green')
        plt.grid(True)
        for x, y in zip(graph_data['x_values'], graph_data['y_values']):
            plt.annotate(f'{y}', (x, y), textcoords="offset points", xytext=(0,8), ha='center', fontsize=9, color='red')
        plt.tight_layout()
        plt.show()

# Run the demonstration with all patterns
demonstrate_disk_scheduling()
