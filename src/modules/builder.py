"""
Network Builder Module

This module provides functionality to create custom wastewater networks.
"""

from .network import WastewaterNetwork

def create_custom_network():
    """
    Create a custom network with user-specified nodes and arcs.
    
    Returns:
    --------
    WastewaterNetwork
        A custom network object
    """
    network = WastewaterNetwork()
    
    # Get nodes from user
    print("Enter nodes (enter blank line to finish):")
    print("Format: node_id inflow")
    print("Example: 1 10")
    
    while True:
        line = input("> ")
        if not line.strip():
            break
            
        try:
            parts = line.strip().split()
            node_id = int(parts[0])
            inflow = float(parts[1])
            network.add_node(node_id, inflow)
            print(f"Added node {node_id} with inflow {inflow}")
        except (ValueError, IndexError):
            print("Invalid format. Please use: node_id inflow")
    
    # Get arcs from user
    print("\nEnter arcs (enter blank line to finish):")
    print("Format: from_node to_node fixed_cost variable_cost [capacity]")
    print("Example: 1 2 100 10 50")
    
    while True:
        line = input("> ")
        if not line.strip():
            break
            
        try:
            parts = line.strip().split()
            from_node = int(parts[0])
            to_node = int(parts[1])
            fixed_cost = float(parts[2])
            variable_cost = float(parts[3])
            
            if len(parts) > 4:
                capacity = float(parts[4])
                network.add_arc(from_node, to_node, fixed_cost, variable_cost, capacity)
            else:
                network.add_arc(from_node, to_node, fixed_cost, variable_cost)
                
            print(f"Added arc ({from_node}, {to_node}) with fixed cost {fixed_cost} and variable cost {variable_cost}")
        except (ValueError, IndexError):
            print("Invalid format. Please use: from_node to_node fixed_cost variable_cost [capacity]")
    
    # Verify the network
    if not network.nodes:
        print("Warning: No nodes were added to the network.")
    
    if not network.arcs:
        print("Warning: No arcs were added to the network.")
    
    # Check flow balance
    total_inflow = sum(flow for flow in network.inflows.values() if flow > 0)
    total_outflow = abs(sum(flow for flow in network.inflows.values() if flow < 0))
    
    if abs(total_inflow - total_outflow) > 1e-6:
        print(f"Warning: Network is not balanced. Total inflow: {total_inflow}, Total outflow: {total_outflow}")
    
    return network

def create_grid_network(rows, cols, flow_per_node=10, sink_node_id=None):
    """
    Create a grid-structured wastewater network.
    
    Parameters:
    -----------
    rows : int
        Number of rows in the grid
    cols : int
        Number of columns in the grid
    flow_per_node : float
        Inflow at each non-sink node
    sink_node_id : int, optional
        ID of the sink node (if None, uses the last node)
        
    Returns:
    --------
    WastewaterNetwork
        A grid-structured network
    """
    network = WastewaterNetwork()
    
    # Create nodes
    total_nodes = rows * cols
    
    if sink_node_id is None:
        sink_node_id = total_nodes + 1
    
    # Add all non-sink nodes with positive inflow
    for i in range(1, total_nodes + 1):
        if i != sink_node_id:
            network.add_node(i, flow_per_node)
    
    # Add sink node with negative inflow (equal to total inflow)
    total_inflow = flow_per_node * (total_nodes if sink_node_id > total_nodes else total_nodes - 1)
    network.add_node(sink_node_id, -total_inflow)
    
    # Add horizontal arcs
    for row in range(rows):
        for col in range(cols - 1):
            node1 = row * cols + col + 1
            node2 = row * cols + col + 2
            
            # Add arcs in both directions
            network.add_arc(node1, node2, 100, 10)
            network.add_arc(node2, node1, 100, 10)
    
    # Add vertical arcs
    for row in range(rows - 1):
        for col in range(cols):
            node1 = row * cols + col + 1
            node2 = (row + 1) * cols + col + 1
            
            # Add arcs in both directions
            network.add_arc(node1, node2, 100, 10)
            network.add_arc(node2, node1, 100, 10)
    
    # Add arcs to sink if sink is outside the grid
    if sink_node_id > total_nodes:
        for i in range(1, total_nodes + 1):
            network.add_arc(i, sink_node_id, 500, 5)
    
    return network 