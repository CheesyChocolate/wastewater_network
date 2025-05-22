"""
Command-line Interface Module
"""

import argparse
import os
import sys

from .optimizer import solve_model, print_solution
from .visualization import draw_network
from .network import WastewaterNetwork

def main():
    """Main entry point for the wastewater network solver."""
    parser = argparse.ArgumentParser(description="Solve the wastewater network design problem")
    
    parser.add_argument("--visualize", action="store_true", 
                       help="Visualize the network and solution")
    parser.add_argument("--save", type=str, default=None, metavar="FILENAME",
                       help="Save the visualization to a file")
    parser.add_argument("--time-limit", type=int, default=None, metavar="SECONDS",
                       help="Time limit for the solver in seconds")
    
    args = parser.parse_args()
    
    print("Creating the wastewater network model...")
    network = WastewaterNetwork.create_example_network()
    
    print("Solving the model...")
    solution = solve_model(network, time_limit=args.time_limit)
    
    print("\n" + "="*60)
    print("SOLUTION SUMMARY")
    print("="*60)
    print_solution(solution)
    print("="*60 + "\n")
    
    if args.visualize:
        print("Generating visualization...")
        
        save_path = args.save
        if not save_path and args.visualize:
            fig_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "docs", "fig")
            os.makedirs(fig_dir, exist_ok=True)
            save_path = os.path.join(fig_dir, "wastewater_solution_cli.png")
            
        draw_network(network, solution, save_path=save_path)
        
        if save_path:
            print(f"Visualization saved to: {save_path}")
        else:
            print("Close the plot window to exit.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 