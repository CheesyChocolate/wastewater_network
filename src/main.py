#!/usr/bin/env python3
"""
Example script for the wastewater network solver.
"""

import os
import sys
import argparse

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.modules.network import WastewaterNetwork
from src.modules.optimizer import solve_model, print_solution
from src.modules.visualization import draw_network

def main():
    """Run the wastewater network solver."""
    parser = argparse.ArgumentParser(description="Solve and visualize the wastewater network problem")
    parser.add_argument("--display", action="store_true", help="Display the visualization")
    args = parser.parse_args()
    
    print("Creating the wastewater network model...")
    network = WastewaterNetwork.create_example_network()
    
    fig_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "fig")
    os.makedirs(fig_dir, exist_ok=True)
    
    print("Solving the model...")
    solution = solve_model(network)
    
    print("\n" + "="*60)
    print("SOLUTION SUMMARY")
    print("="*60)
    print_solution(solution)
    print("="*60 + "\n")
    
    print("Generating visualization...")
    output_file = os.path.join(fig_dir, "wastewater_solution.png")
    draw_network(network, solution, save_path=output_file)
    print(f"Visualization saved to: {output_file}")
    
    if args.display:
        print("Displaying visualization...")
        draw_network(network, solution)
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 