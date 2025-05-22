"""
Visualization Module
"""

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os

def draw_network(network, solution=None, figsize=(12, 10), save_path=None):
    """Draw the wastewater network as a directed graph."""
    G = nx.DiGraph()
    
    # Define node positions
    pos = {
        1: (0, 8),    # Top left
        2: (2, 6),    # Middle top
        3: (4, 8),    # Top right
        4: (4, 4),    # Middle right
        5: (0, 0),    # Bottom left
        6: (2, 2),    # Middle bottom
        7: (4, 0),    # Bottom right
        8: (6, 3),    # Far right
        9: (8, 4)     # Supersink (treatment)
    }
    
    # Add nodes with attributes
    for node in network.nodes:
        inflow = network.inflows[node]
        G.add_node(node, inflow=inflow)
    
    # Add all arcs as thin gray lines initially
    for arc in network.arcs:
        G.add_edge(arc[0], arc[1], 
                  fixed_cost=network.fixed_costs[arc],
                  variable_cost=network.variable_costs[arc],
                  capacity=network.capacities[arc],
                  flow=0,
                  constructed=False)
    
    # Update arc attributes if a solution is provided
    if solution and solution['objective_value'] is not None:
        for arc in solution['constructed_arcs']:
            flow = solution['flows'].get(arc, 0)
            G.edges[arc]['flow'] = flow
            G.edges[arc]['constructed'] = True
    
    # Create figure
    plt.figure(figsize=figsize)
    
    # Draw the nodes
    node_colors = []
    node_sizes = []
    labels = {}
    
    for node in G.nodes():
        inflow = G.nodes[node]['inflow']
        
        # Node color based on type
        if node == 9:
            node_colors.append('lightblue')  # Treatment plant (sink)
        elif inflow > 0:
            node_colors.append('lightgreen')  # Supply node
        elif inflow < 0:
            node_colors.append('lightblue')  # Demand node
        else:
            node_colors.append('white')  # Transshipment node
        
        # Node size based on inflow/outflow
        if inflow != 0:
            node_sizes.append(1000 + 100 * abs(inflow))
        else:
            node_sizes.append(800)
        
        # Node labels
        if inflow != 0 and node != 9:
            labels[node] = f"{node}\n({inflow})"
        else:
            labels[node] = f"{node}"
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, 
                          edgecolors='black', linewidths=1)
    
    # Draw edges
    if solution and solution['objective_value'] is not None:
        # Draw constructed arcs (bold)
        constructed_edges = [(u, v) for u, v in G.edges() if G.edges[u, v]['constructed']]
        nx.draw_networkx_edges(G, pos, edgelist=constructed_edges, 
                              width=3, edge_color='blue', arrows=True, arrowsize=20)
        
        # Draw unused arcs (thin, gray)
        unused_edges = [(u, v) for u, v in G.edges() if not G.edges[u, v]['constructed']]
        nx.draw_networkx_edges(G, pos, edgelist=unused_edges, 
                              width=1, edge_color='gray', style='dashed', 
                              arrows=True, arrowsize=15, alpha=0.5)
    else:
        # Draw all edges the same if no solution is provided
        nx.draw_networkx_edges(G, pos, width=1.5, edge_color='gray', arrows=True, arrowsize=15)
    
    # Draw node labels
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=12, font_weight='bold')
    
    # Draw edge labels if solution is provided
    if solution and solution['objective_value'] is not None:
        edge_labels = {}
        for u, v in constructed_edges:
            flow = G.edges[u, v]['flow']
            if flow > 0.001:
                edge_labels[(u, v)] = f"{flow:.1f}"
        
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
    
    # Add title
    if solution and solution['objective_value'] is not None:
        plt.title(f"Wastewater Network Solution\nTotal Cost: ${solution['objective_value']:,.2f}", 
                 fontsize=14)
    else:
        plt.title("Wastewater Network", fontsize=14)
    
    plt.axis('off')
    plt.tight_layout()
    
    # Save or display the figure
    if save_path:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        # Only attempt to show the figure in an interactive environment
        try:
            plt.show()
        except:
            print("Warning: Unable to display the figure in a non-interactive environment.")
        finally:
            plt.close() 