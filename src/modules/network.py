"""
Wastewater Network Module
"""

class WastewaterNetwork:
    """A class representing a wastewater network with nodes, arcs, and flow data."""
    
    def __init__(self):
        """Initialize an empty wastewater network."""
        self.nodes = set()
        self.arcs = set()
        self.inflows = {}
        self.fixed_costs = {}
        self.variable_costs = {}
        self.capacities = {}
    
    def add_node(self, node_id, inflow=0):
        """Add a node to the network."""
        self.nodes.add(node_id)
        self.inflows[node_id] = inflow
    
    def add_arc(self, from_node, to_node, fixed_cost, variable_cost, capacity=1000):
        """Add an arc to the network."""
        arc = (from_node, to_node)
        self.arcs.add(arc)
        self.fixed_costs[arc] = fixed_cost
        self.variable_costs[arc] = variable_cost
        self.capacities[arc] = capacity
    
    def get_outgoing_arcs(self, node):
        """Get all arcs leaving a node."""
        return [(i, j) for (i, j) in self.arcs if i == node]
    
    def get_incoming_arcs(self, node):
        """Get all arcs entering a node."""
        return [(i, j) for (i, j) in self.arcs if j == node]
    
    @classmethod
    def create_example_network(cls):
        """Create the example wastewater network from the problem statement."""
        network = cls()
        
        # Add nodes with their inflows
        network.add_node(1, 27)
        network.add_node(2, 3)
        network.add_node(3, 14)
        network.add_node(4, 36)
        network.add_node(5, 21)
        network.add_node(6, 8)
        network.add_node(7, 13)
        network.add_node(8, 0)
        network.add_node(9, -122)  # Supersink with outflow equal to total inflow
        
        # Add arcs with their costs and capacities
        network.add_arc(1, 2, 240, 21, 100)
        network.add_arc(1, 3, 350, 30, 100)
        network.add_arc(2, 3, 200, 22, 100)
        network.add_arc(2, 4, 750, 58, 100)
        network.add_arc(3, 4, 610, 43, 100)
        network.add_arc(3, 9, 3800, 1, 100)
        network.add_arc(4, 3, 1840, 49, 100)
        network.add_arc(4, 8, 780, 63, 100)
        network.add_arc(5, 6, 620, 44, 100)
        network.add_arc(5, 7, 800, 51, 100)
        network.add_arc(6, 7, 500, 56, 100)
        network.add_arc(6, 8, 630, 94, 100)
        network.add_arc(7, 4, 1120, 82, 100)
        network.add_arc(7, 9, 3800, 1, 100)
        network.add_arc(8, 9, 2500, 2, 100)
        
        return network 