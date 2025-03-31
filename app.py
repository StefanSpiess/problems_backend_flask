from flask import Flask, jsonify, request, abort

from problem_solution import ProblemSolution
from market_demand import MarketDemand

app = Flask(__name__)

# ProblemSolution endpoints (already defined)
@app.route('/problem_solutions', methods=['GET'])
def list_solutions():
    all_problem_solutions = ProblemSolution.load_all()
    all_solutions = []
    for data in all_problem_solutions:
        ps = ProblemSolution.from_dict(data)
        serialized = ps.to_full_dict()
        all_solutions.append(serialized)
    return jsonify(all_solutions)

@app.route('/problem_solutions', methods=['POST'])
def create_solution():
    data = request.json
    required_fields = ['name', 'problem_id', 'market_demand_id', 'solution_space_id', 'solution_maturity_id']
    if not all(field in data for field in required_fields):
        abort(400, description="Missing required fields")
    solution = ProblemSolution(**data)
    solution.save()
    return jsonify(solution.to_dict()), 201

@app.route('/problem_solutions/<int:solution_id>', methods=['GET'])
def solution_details(solution_id):
    sol = ProblemSolution.find_by_id(solution_id)
    if not sol:
        abort(404)
    return jsonify(sol.to_full_dict())

# 👉 New endpoints for MarketDemand objects!

@app.route('/market_demands', methods=['GET'])
def get_market_demands():
    market_demands = MarketDemand.load_all()
    return jsonify(market_demands)

@app.route('/market_demands', methods=['POST'])
def create_market_demand():
    data = request.json
    demand = MarketDemand(**data)
    demand.save()
    return jsonify(demand.to_dict()), 201

@app.route('/market_demands/<int:demand_id>', methods=['GET'])
def get_market_demand(demand_id):
    demand = MarketDemand.find_by_id(demand_id)
    if not demand:
        abort(404, description="MarketDemand not found")
    return jsonify(demand.to_dict())