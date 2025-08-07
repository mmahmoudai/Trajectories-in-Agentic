import logging
import networkx as nx
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class KnowledgeGraph:
    """
    Manages the cybersecurity knowledge graph using NetworkX. This class provides
    functionality to build, manipulate, and query the graph of security entities.
    """

    def __init__(self):
        """Initializes the Knowledge Graph."""
        self.graph = nx.MultiDiGraph()
        logging.info("Knowledge Graph initialized.")

    def add_triple(self, entity1, relationship, entity2):
        """
        Adds a directed relationship (a triple) to the knowledge graph.

        Args:
            entity1 (str): The source entity (node).
            relationship (str): The type of relationship (edge label).
            entity2 (str): The target entity (node).
        """
        self.graph.add_node(entity1)
        self.graph.add_node(entity2)
        self.graph.add_edge(entity1, entity2, label=relationship)
        logging.debug(f"Added triple: {entity1} -[{relationship}]-> {entity2}")

    def find_related_nodes(self, entity, depth=1):
        """
        Finds all nodes connected to a given entity up to a certain depth.

        Args:
            entity (str): The entity to start the search from.
            depth (int): The search depth.

        Returns:
            list: A list of tuples, where each tuple is a relationship (source, relation, target).
        """
        if entity not in self.graph:
            logging.warning(f"Entity '{entity}' not found in the knowledge graph.")
            return []

        related_nodes = []
        # Use breadth-first search to find neighbors
        for source, target, data in self.graph.edges(entity, data=True):
            related_nodes.append((source, data['label'], target))

        # For a simple 1-depth search, this is sufficient.
        # A deeper search would require a recursive or iterative BFS/DFS implementation.
        return related_nodes

    def get_subgraph_for_entities(self, entities):
        """
        Extracts a subgraph containing only the specified entities and their relationships.

        Args:
            entities (list): A list of entity names.

        Returns:
            networkx.Graph: A subgraph containing the specified entities.
        """
        return self.graph.subgraph([node for node in entities if node in self.graph])

    def visualize_graph(self, subgraph=None, filename="knowledge_graph.png"):
        """
        Visualizes the knowledge graph (or a subgraph) and saves it to a file.

        Args:
            subgraph (networkx.Graph, optional): The subgraph to visualize. If None, visualizes the whole graph.
            filename (str): The path to save the visualization image.
        """
        plt.figure(figsize=(12, 12))

        graph_to_draw = subgraph if subgraph is not None else self.graph

        if not graph_to_draw.nodes():
            logging.warning("Graph is empty, nothing to visualize.")
            plt.close()
            return

        pos = nx.spring_layout(graph_to_draw, k=0.9)
        nx.draw(graph_to_draw, pos, with_labels=True, node_size=2500, node_color="skyblue", font_size=10, font_weight="bold")
        edge_labels = nx.get_edge_attributes(graph_to_draw, 'label')
        nx.draw_networkx_edge_labels(graph_to_draw, pos, edge_labels=edge_labels, font_color='red')

        plt.title("Cybersecurity Knowledge Graph")
        plt.savefig(filename)
        plt.close()
        logging.info(f"Graph visualization saved to {filename}")

if __name__ == '__main__':
    # Example Usage
    kg = KnowledgeGraph()

    # Add cybersecurity threat intelligence data
    kg.add_triple('APT28', 'uses_tool', 'X-Agent')
    kg.add_triple('X-Agent', 'is_type', 'Malware')
    kg.add_triple('APT28', 'targets_sector', 'Government')
    kg.add_triple('CVE-2023-23397', 'exploited_by', 'APT28')
    kg.add_triple('CVE-2023-23397', 'is_type', 'Vulnerability')

    # Find nodes related to 'APT28'
    related = kg.find_related_nodes('APT28')
    print("\n--- Relationships for 'APT28' ---")
    for r in related:
        print(f"{r[0]} -[{r[1]}]-> {r[2]}")

    # Visualize the entire graph
    kg.visualize_graph(filename="full_kg.png")

    # Visualize a subgraph
    subgraph = kg.get_subgraph_for_entities(['APT28', 'CVE-2023-23397', 'X-Agent'])
    kg.visualize_graph(subgraph=subgraph, filename="subgraph_kg.png")

    print("\nGraph visualizations saved to 'full_kg.png' and 'subgraph_kg.png'")
