import matplotlib.pyplot as plt
import requests

def simulate_user_interactions():
    actions = [('workout', 10), ('nutrition', 10), ('workout', 5), ('nutrition', 5)]
    state_history = []

    for action, value in actions:
        if action == 'workout':
            response = requests.post('http://localhost:5000/workout', json={'intensity': value})
        elif action == 'nutrition':
            response = requests.post('http://localhost:5000/nutrition', json={'quality': value})
        state = response.json()
        state_history.append(state)
    
    return state_history

def plot_state_history(state_history):
    fitness = [state['fitness_level'] for state in state_history]
    nutrition = [state['nutrition_score'] for state in state_history]
    recovery = [state['recovery_score'] for state in state_history]
    
    plt.figure(figsize=(12, 6))
    plt.plot(fitness, label='Fitness Level')
    plt.plot(nutrition, label='Nutrition Score')
    plt.plot(recovery, label='Recovery Score')
    plt.xlabel('Interaction')
    plt.ylabel('Score')
    plt.legend()
    plt.show()

state_history = simulate_user_interactions()
plot_state_history(state_history)
