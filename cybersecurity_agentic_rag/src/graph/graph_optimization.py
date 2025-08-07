import logging
fromcybersecurity_agentic_rag.src.graph.knowledge_graph import KnowledgeGraph
fromcybersecurity_agentic_rag.src.graph.graph_neural_net import GCN, predict
import torch
from torch_geometric.data import Data

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GraphOptimization:
    """
    Provides methods to optimize and refine the knowledge graph. This includes
    inferring new relationships based on GNN predictions and pruning the graph
    to maintain relevance and quality.
    """

    def __init__(self, knowledge_graph: KnowledgeGraph, gnn_model: GCN):
        """
        Initializes the Graph Optimization engine.

        Args:
            knowledge_graph (KnowledgeGraph): The knowledge graph to be optimized.
            gnn_model (GCN): A trained GNN model for inference.
        """
        self.kg = knowledge_graph
        self.gnn = gnn_model
        logging.info("Graph Optimization engine initialized.")

    def infer_new_relationships(self, graph_data: Data, confidence_threshold=0.8):
        """
        Infers new relationships based on GNN predictions and adds them to the graph.

        For example, if two nodes are both classified as 'malicious' with high
        confidence, a new 'suspected_link' relationship could be inferred.

        Args:
            graph_data (Data): The PyG data object representing the graph.
            confidence_threshold (float): The confidence level required to add a new link.
        """
        logging.info("Starting relationship inference process.")

        self.gnn.eval()
        with torch.no_grad():
            log_softmax_out = self.gnn(graph_data)
            probabilities = torch.exp(log_softmax_out)

        predictions = probabilities.argmax(dim=1)

        # Example heuristic: Link nodes that are newly classified as malicious (class 1)
        malicious_nodes_indices = (predictions == 1).nonzero(as_tuple=True)[0]

        # This requires a mapping from tensor index back to node name
        node_names = list(self.kg.graph.nodes())

        new_triples_count = 0
        for i in range(len(malicious_nodes_indices)):
            for j in range(i + 1, len(malicious_nodes_indices)):
                node1_idx = malicious_nodes_indices[i]
                node2_idx = malicious_nodes_indices[j]

                # Check if confidence is high for both predictions
                if probabilities[node1_idx, 1] > confidence_threshold and \
                   probabilities[node2_idx, 1] > confidence_threshold:

                    node1_name = node_names[node1_idx]
                    node2_name = node_names[node2_idx]

                    # Add a new, inferred link if one doesn't already exist
                    if not self.kg.graph.has_edge(node1_name, node2_name):
                        self.kg.add_triple(node1_name, 'inferred_malicious_link', node2_name)
                        new_triples_count += 1

        logging.info(f"Inferred and added {new_triples_count} new relationships.")
        return new_triples_count

    def prune_graph(self, degree_threshold=1):
        """
        Prunes the graph by removing nodes with a degree below a certain threshold.

        Args:
            degree_threshold (int): The minimum degree a node must have to be kept.
        """
        logging.info(f"Pruning graph. Removing nodes with degree < {degree_threshold}.")

        initial_nodes = self.kg.graph.number_of_nodes()
        nodes_to_remove = [node for node, degree in dict(self.kg.graph.degree()).items() if degree < degree_threshold]

        self.kg.graph.remove_nodes_from(nodes_to_remove)

        final_nodes = self.kg.graph.number_of_nodes()
        logging.info(f"Removed {initial_nodes - final_nodes} nodes from the graph.")
        return initial_nodes - final_nodes

if __name__ == '__main__':
    # --- Mockups and Demonstration ---

    # 1. Create a Knowledge Graph
    kg = KnowledgeGraph()
    kg.add_triple('IP_1', 'communicates_with', 'Domain_A') # Benign
    kg.add_triple('IP_2', 'communicates_with', 'Domain_B') # Malicious
    kg.add_triple('IP_3', 'communicates_with', 'Domain_B') # Malicious
    kg.add_triple('IP_4', 'is_isolated', 'Orphan_Node')   # Low degree

    # 2. Create and "train" a GNN model
    node_names = list(kg.graph.nodes())
    num_nodes = len(node_names)
    # This mapping is crucial for connecting KG nodes to tensor indices
    name_to_idx = {name: i for i, name in enumerate(node_names)}

    # Create dummy features and labels
    x = torch.rand(num_nodes, 8)
    # Labels: 0=Benign, 1=Malicious
    y = torch.tensor([0, 0, 1, 1, 1, 1, 0]) # Based on node names

    # Create edge index from KG
    edge_list = [(name_to_idx[u], name_to_idx[v]) for u, v in kg.graph.edges()]
    edge_index = torch.tensor(edge_list, dtype=torch.long).t().contiguous()

    graph_data = Data(x=x, edge_index=edge_index, y=y)

    gnn_model = GCN(num_node_features=8, num_classes=2)
    # In a real scenario, the model would be loaded from a checkpoint after training
    gnn_model.eval()

    # 3. Initialize the optimization engine
    graph_optimizer = GraphOptimization(knowledge_graph=kg, gnn_model=gnn_model)

    print("--- Initial Graph ---")
    print("Nodes:", kg.graph.nodes())
    print("Edges:", kg.graph.edges(data=True))

    # 4. Infer new relationships
    print("\n--- Inferring Relationships ---")
    graph_optimizer.infer_new_relationships(graph_data)

    print("\n--- Graph After Inference ---")
    print("Nodes:", kg.graph.nodes())
    print("Edges:", kg.graph.edges(data=True))

    # 5. Prune the graph
    print("\n--- Pruning Graph ---")
    graph_optimizer.prune_graph(degree_threshold=2) # Remove nodes with only one connection

    print("\n--- Graph After Pruning ---")
    print("Nodes:", kg.graph.nodes())
    print("Edges:", kg.graph.edges(data=True))
