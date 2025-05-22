"""
Utility Functions Module
"""

import os
import sys
from .optimizer import solve_model, print_solution
from .visualization import draw_network
from .network import WastewaterNetwork

def solve_and_visualize(network=None, save_path=None, display=True):
    """Solve the wastewater network problem and visualize the solution."""
    if network is None:
        network = WastewaterNetwork.create_example_network()
    
    print("Solving the wastewater network model...")
    solution = solve_model(network)
    
    print("\n" + "="*60)
    print("SOLUTION SUMMARY")
    print("="*60)
    print_solution(solution)
    print("="*60 + "\n")
    
    if display:
        print("Generating visualization...")
        if save_path:
            os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
            draw_network(network, solution, save_path=save_path)
            print(f"Visualization saved to: {save_path}")
        
        draw_network(network, solution)
    
    return solution

def run_example():
    """Run an example that solves and visualizes the wastewater network."""
    fig_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "docs", "fig")
    os.makedirs(fig_dir, exist_ok=True)
    
    save_path = os.path.join(fig_dir, "wastewater_solution.png")
    solve_and_visualize(save_path=save_path)
    
    return 0

if __name__ == "__main__":
    sys.exit(run_example()) 