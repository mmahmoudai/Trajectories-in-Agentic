import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class KnowledgeAgent:
    """
    The Knowledge Agent is responsible for managing and interacting with the
    cybersecurity knowledge graph. It provides other agents with access to
    structured knowledge and updates the graph with new information.
    """

    def __init__(self, knowledge_graph):
        """
        Initializes the Knowledge Agent.

        Args:
            knowledge_graph: An instance of the KnowledgeGraph class.
        """
        self.knowledge_graph = knowledge_graph
        logging.info("Knowledge Agent initialized.")

    def query_knowledge_graph(self, query):
        """
        Queries the knowledge graph to find relationships and entities.

        Args:
            query (str): A natural language or structured query.

        Returns:
            list: A list of results from the knowledge graph.
        """
        logging.info(f"Querying knowledge graph with: '{query}'")
        # In a real implementation, this would involve parsing the query
        # and translating it into a graph query language (e.g., Cypher, SPARQL).
        # Here, we'll simulate a search for related nodes.

        # Example: "find related entities to 'CVE-2023-12345'"
        try:
            entity = query.split("'")[1] # Simple parsing
            results = self.knowledge_graph.find_related_nodes(entity)
            logging.info(f"Found {len(results)} related entities for '{entity}'.")
            return results
        except IndexError:
            logging.warning("Could not parse entity from query.")
            return []

    def add_information(self, entity1, relationship, entity2):
        """
        Adds a new piece of information (a triple) to the knowledge graph.

        Args:
            entity1 (str): The source entity.
            relationship (str): The relationship between the entities.
            entity2 (str): The target entity.
        """
        logging.info(f"Adding information to knowledge graph: {entity1} -> {relationship} -> {entity2}")
        self.knowledge_graph.add_triple(entity1, relationship, entity2)
        logging.info("Knowledge graph updated.")

    def extract_entities_from_report(self, report_text):
        """
        Extracts cybersecurity entities (e.g., IPs, CVEs, file hashes) from a text report.

        Args:
            report_text (str): The text of the security report.

        Returns:
            list: A list of extracted entities.
        """
        # This would typically use a sophisticated NER model.
        # For this example, we'll use a simple regex-based approach.
        import re

        cve_pattern = r'CVE-\d{4}-\d{4,7}'
        ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'

        cves = re.findall(cve_pattern, report_text)
        ips = re.findall(ip_pattern, report_text)

        entities = cves + ips
        logging.info(f"Extracted {len(entities)} entities from report.")
        return entities

if __name__ == '__main__':
    # Mock-up for demonstration
    class MockKnowledgeGraph:
        def __init__(self):
            self.graph = {}
        def add_triple(self, e1, rel, e2):
            if e1 not in self.graph:
                self.graph[e1] = []
            self.graph[e1].append((rel, e2))
            print(f"MockKG: Added '{e1} -[{rel}]-> {e2}'")
        def find_related_nodes(self, entity):
            print(f"MockKG: Searching for nodes related to '{entity}'")
            return self.graph.get(entity, [])

    # Example Usage
    mock_kg = MockKnowledgeGraph()
    knowledge_agent = KnowledgeAgent(knowledge_graph=mock_kg)

    # Add some information
    knowledge_agent.add_information('CVE-2023-12345', 'exploited_by', 'APT41')
    knowledge_agent.add_information('APT41', 'uses_tool', 'Cobalt Strike')
    knowledge_agent.add_information('192.168.1.100', 'associated_with', 'APT41')

    # Query the knowledge
    results = knowledge_agent.query_knowledge_graph("find related entities to 'APT41'")
    print("\n--- Query Results for 'APT41' ---")
    print(results)

    # Extract entities from a sample report
    sample_report = """
    Incident Report IR-2023-08-07:
    We detected suspicious activity from IP 192.168.1.100, which is linked to
    a known campaign exploiting CVE-2023-12345. The threat actor, likely APT41,
    used a variant of Cobalt Strike.
    """
    entities = knowledge_agent.extract_entities_from_report(sample_report)
    print("\n--- Extracted Entities ---")
    print(entities)
