import json
import os

def save_iteration_state(states, algorithm_name):
    filename = f"save_file/{algorithm_name}_state.json"
    os.makedirs('save_file', exist_ok=True)
    
    data = {
        'states': [{
            'cube': state['cube'],
            'value': state['value'],
            'iteration': state['iteration'],
            'temperature': state.get('temperature', None)  # Untuk simulated annealing
        } for state in states]
    }
    
    with open(filename, 'w') as f:
        json.dump(data, f)
    
    return filename

def load_iteration_state(filename):
    with open(filename, 'r') as f:
        return json.load(f)