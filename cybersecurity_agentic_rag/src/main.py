import logging
import json
from langchain_core.documents import Document

# Import all the components of our system
from agents.coordination_agent import CoordinationAgent
from agents.cyber_defense_agent import CyberDefenseAgent
from agents.knowledge_agent import KnowledgeAgent
from rag.retrieval_engine import RetrievalEngine
from rag.generation_engine import GenerationEngine
from graph.knowledge_graph import KnowledgeGraph

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_system_components():
    """
    Initializes and wires together all the components of the agentic RAG system.
    In a real application, this would involve loading trained models, connecting to
    databases, etc. Here, we use mock components for demonstration.
    """
    logger.info("--- Setting up System Components ---")

    # 1. RAG Components
    # Create a small set of documents for the retrieval engine's knowledge base
    sample_docs = [
        Document(page_content="CVE-2023-3456 is a critical remote code execution vulnerability."),
        Document(page_content="The threat actor 'ShadowNet' often uses phishing emails as an initial access vector."),
        Document(page_content="IP address 123.123.123.123 is a known command-and-control server for ShadowNet."),
    ]
    retrieval_engine = RetrievalEngine(documents=sample_docs)
    generation_engine = GenerationEngine() # Uses a mock LLM by default

    # 2. Graph Component
    knowledge_graph = KnowledgeGraph()
    knowledge_graph.add_triple('ShadowNet', 'uses_technique', 'Phishing')
    knowledge_graph.add_triple('123.123.123.123', 'is_c2_server_for', 'ShadowNet')
    knowledge_graph.add_triple('CVE-2023-3456', 'is_exploited_by', 'ShadowNet')

    # 3. Agent Components
    knowledge_agent = KnowledgeAgent(knowledge_graph=knowledge_graph)
    cyber_defense_agent = CyberDefenseAgent(
        retrieval_engine=retrieval_engine,
        generation_engine=generation_engine
    )
    coordination_agent = CoordinationAgent(
        defense_agent=cyber_defense_agent,
        knowledge_agent=knowledge_agent
    )

    logger.info("--- System Components are Ready ---")
    return coordination_agent

def main():
    """
    Main function to run a demonstration of the cybersecurity agentic system.
    """
    # Initialize the entire system
    coordinator = setup_system_components()

    # Define a sample security event to be processed
    security_event = {
        "id": "EVENT-003",
        "type": "Malware Detection",
        "description": "A process attempted to connect to a known malicious IP address (123.123.123.123). This may be related to CVE-2023-3456.",
        "source": "Endpoint Detection and Response (EDR) System",
        "timestamp": "2025-08-07T14:00:00Z"
    }

    logger.info(f"\n--- Handling New Security Event: {security_event['id']} ---")

    # The Coordination Agent orchestrates the entire response
    final_output = coordinator.handle_security_event(security_event)

    logger.info("\n--- Final Output from Coordination Agent ---")
    # Use json.dumps for pretty printing the output dictionary
    print(json.dumps(final_output, indent=2))

if __name__ == '__main__':
    main()
