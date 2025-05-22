"""
Optimizer Module
"""

import pulp
from .network import WastewaterNetwork

def create_model(network):
    """Create a PuLP model for the fixed-charge network flow problem."""
    model = pulp.LpProblem("WastewaterNetworkDesign", pulp.LpMinimize)
    
    # Flow variables
    x = {arc: pulp.LpVariable(f"x_{arc[0]}_{arc[1]}", lowBound=0) for arc in network.arcs}
    
    # Binary variables for arc construction
    y = {arc: pulp.LpVariable(f"y_{arc[0]}_{arc[1]}", cat=pulp.LpBinary) for arc in network.arcs}
    
    # Objective function
    model += pulp.lpSum(
        network.fixed_costs[arc] * y[arc] + network.variable_costs[arc] * x[arc]
        for arc in network.arcs
    )
    
    # Flow balance constraints
    for node in network.nodes:
        outflow = pulp.lpSum(x[arc] for arc in network.get_outgoing_arcs(node))
        inflow = pulp.lpSum(x[arc] for arc in network.get_incoming_arcs(node))
        model += outflow - inflow == network.inflows[node]
    
    # Capacity constraints
    for arc in network.arcs:
        model += x[arc] <= network.capacities[arc] * y[arc]
    
    return model, x, y

def solve_model(network, time_limit=None):
    """Solve the wastewater network design problem."""
    model, x, y = create_model(network)
    
    solver = pulp.PULP_CBC_CMD(timeLimit=time_limit) if time_limit else pulp.PULP_CBC_CMD()
    model.solve(solver)
    
    if model.status != pulp.LpStatusOptimal:
        return {
            "status": pulp.LpStatus[model.status],
            "objective_value": None,
            "constructed_arcs": [],
            "flows": {}
        }
    
    constructed_arcs = [(i, j) for (i, j) in network.arcs if y[(i, j)].value() > 0.5]
    flows = {(i, j): x[(i, j)].value() for (i, j) in network.arcs if x[(i, j)].value() > 0.001}
    
    return {
        "status": "Optimal",
        "objective_value": pulp.value(model.objective),
        "constructed_arcs": constructed_arcs,
        "flows": flows
    }

def print_solution(solution):
    """Print a solution in a readable format."""
    print(f"Solution status: {solution['status']}")
    
    if solution['objective_value'] is None:
        print("No feasible solution found.")
        return
    
    print(f"Total cost: ${solution['objective_value']:,.2f}")
    
    print("\nConstructed arcs:")
    for arc in sorted(solution['constructed_arcs']):
        print(f"  Arc {arc[0]} -> {arc[1]}")
    
    print("\nFlows:")
    for arc, flow in sorted(solution['flows'].items()):
        if flow > 0.001:  # Only print non-zero flows
            print(f"  Flow on {arc[0]} -> {arc[1]}: {flow:.2f}")
            
    print("\nTreatment plants:")
    for arc in solution['constructed_arcs']:
        if arc[1] == 9:  # Treatment plant (connection to supersink)
            print(f"  Plant at node {arc[0]} with capacity {solution['flows'].get(arc, 0):.2f}") 