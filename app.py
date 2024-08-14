from flask import Flask, request, jsonify
from fitness_simulator import FitnessSimulator
import json

app = Flask(__name__)
simulator = FitnessSimulator()

@app.route('/workout', methods=['POST'])
def workout():
    intensity = request.json.get('intensity')
    simulator.apply_workout(intensity)
    simulator.update_state()
    return jsonify(simulator.get_state())

@app.route('/nutrition', methods=['POST'])
def nutrition():
    quality = request.json.get('quality')
    simulator.apply_nutrition(quality)
    simulator.update_state()
    return jsonify(simulator.get_state())

@app.route('/state', methods=['GET'])
def get_state():
    return jsonify(simulator.get_state())

if __name__ == '__main__':
    app.run(debug=True)
