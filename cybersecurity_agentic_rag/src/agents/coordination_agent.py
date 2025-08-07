import logging
fromcybersecurity_agentic_rag.src.agents.cyber_defense_agent import CyberDefenseAgent
fromcybersecurity_agentic_rag.src.agents.knowledge_agent import KnowledgeAgent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CoordinationAgent:
    """
    The Coordination Agent acts as the orchestrator of the multi-agent system.
    It manages the workflow between the Cyber Defense Agent and the Knowledge Agent
    to ensure a comprehensive and context-aware response to security events.
    """

    def __init__(self, defense_agent: CyberDefenseAgent, knowledge_agent: KnowledgeAgent):
        """
        Initializes the Coordination Agent.

        Args:
            defense_agent: An instance of the CyberDefenseAgent.
            knowledge_agent: An instance of the KnowledgeAgent.
        """
        self.defense_agent = defense_agent
        self.knowledge_agent = knowledge_agent
        logging.info("Coordination Agent initialized.")

    def handle_security_event(self, event_data):
        """
        Manages the end-to-end process of handling a security event.

        Args:
            event_data (dict): A dictionary containing the details of the security event.

        Returns:
            dict: A dictionary containing the final response plan and all intermediate artifacts.
        """
        logging.info(f"New security event received: {event_data.get('id', 'N/A')}")

        # 1. Initial analysis by the Cyber Defense Agent
        initial_analysis = self.defense_agent.analyze_alert(event_data)
        logging.info("Initial analysis complete.")

        # 2. Knowledge enrichment by the Knowledge Agent
        report_text = f"{event_data['description']} {initial_analysis['analysis']}"
        extracted_entities = self.knowledge_agent.extract_entities_from_report(report_text)

        enriched_knowledge = {}
        for entity in extracted_entities:
            query = f"find related entities to '{entity}'"
            enriched_knowledge[entity] = self.knowledge_agent.query_knowledge_graph(query)

        logging.info("Knowledge enrichment complete.")

        # 3. Generate a final, context-aware response plan
        final_analysis_report = {
            "analysis": initial_analysis["analysis"],
            "enriched_knowledge": enriched_knowledge,
        }

        logging.info("Generating final response plan with enriched context.")
        final_response_plan = self.defense_agent.propose_response_plan(final_analysis_report)

        return {
            "event_id": event_data.get('id'),
            "initial_analysis": initial_analysis,
            "enriched_knowledge": enriched_knowledge,
            "final_response_plan": final_response_plan,
        }

if __name__ == '__main__':
    # This is a mock-up for demonstration purposes.
    # In a real system, these would be fully implemented components.
    class MockRetrievalEngine:
        def retrieve(self, query, top_k):
            from langchain_core.documents import Document
            return [Document(page_content="Context about similar past incidents...")]

    class MockGenerationEngine:
        def generate(self, prompt):
            if "Analyze" in prompt:
                return "Analysis: High-severity threat detected, likely related to phishing."
            if "response plan" in prompt:
                return "Final Plan: 1. Isolate machine. 2. Block C2 IP. 3. Reset user credentials."

    class MockKnowledgeGraph:
        def __init__(self):
            self.graph = {'CVE-2023-9999': [('exploited_by', 'FIN7')]}
        def add_triple(self, e1, rel, e2): pass
        def find_related_nodes(self, entity):
            return self.graph.get(entity, [])

    # Setup mock components and agents
    mock_retriever = MockRetrievalEngine()
    mock_generator = MockGenerationEngine()
    mock_kg = MockKnowledgeGraph()

    defense_agent = CyberDefenseAgent(mock_retriever, mock_generator)
    knowledge_agent = KnowledgeAgent(mock_kg)

    coordination_agent = CoordinationAgent(defense_agent, knowledge_agent)

    # Define a sample security event
    sample_event = {
        "id": "EVENT-002",
        "description": "User reported a suspicious email with a link exploiting CVE-2023-9999.",
        "timestamp": "2025-08-07T11:00:00Z"
    }

    # Handle the event
    final_output = coordination_agent.handle_security_event(sample_event)

    print("\n--- Coordination Agent Final Output ---")
    import json
    print(json.dumps(final_output, indent=2))
