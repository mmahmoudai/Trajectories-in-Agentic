import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CyberDefenseAgent:
    """
    The Cyber Defense Agent is responsible for actively monitoring for threats,
    analyzing them, and proposing appropriate responses. It is the frontline
    of the agentic cyber defense system.
    """

    def __init__(self, retrieval_engine, generation_engine):
        """
        Initializes the Cyber Defense Agent.

        Args:
            retrieval_engine: An instance of the retrieval engine to fetch relevant information.
            generation_engine: An instance of the generation engine to produce reports and responses.
        """
        self.retrieval_engine = retrieval_engine
        self.generation_engine = generation_engine
        logging.info("Cyber Defense Agent initialized.")

    def analyze_alert(self, alert_data):
        """
        Analyzes a given security alert to determine its nature and severity.

        Args:
            alert_data (dict): A dictionary containing details of the security alert.

        Returns:
            dict: An analysis report including threat level and key indicators.
        """
        logging.info(f"Analyzing security alert: {alert_data.get('id', 'N/A')}")

        # 1. Retrieve relevant context from knowledge sources
        query = f"Analysis of security alert: {alert_data.get('description', '')}"
        retrieved_docs = self.retrieval_engine.retrieve(query, top_k=5)

        # 2. Generate a structured analysis using the generation engine
        prompt = f"""
        Analyze the following security alert based on the provided context.

        Alert: {alert_data}

        Context from knowledge base:
        {''.join([doc.page_content for doc in retrieved_docs])}

        Provide a structured analysis covering:
        - Threat Category (e.g., Malware, Phishing, Intrusion)
        - Severity Level (e.g., Critical, High, Medium, Low)
        - Key Indicators of Compromise (IOCs)
        - Recommended immediate actions
        """

        analysis_report = self.generation_engine.generate(prompt)

        logging.info(f"Generated analysis for alert {alert_data.get('id', 'N/A')}")
        return {"analysis": analysis_report, "retrieved_docs": retrieved_docs}

    def propose_response_plan(self, analysis_report):
        """
        Proposes a response plan based on the analysis of a threat.

        Args:
            analysis_report (dict): The output from the analyze_alert method.

        Returns:
            str: A textual description of the proposed response plan.
        """
        logging.info("Generating a response plan.")

        prompt = f"""
        Based on the following security analysis, create a detailed, step-by-step response plan.
        The plan should be actionable and clear for a security operations team.

        Analysis:
        {analysis_report.get('analysis', 'No analysis provided.')}

        Propose a response plan with sections for:
        1. Containment
        2. Eradication
        3. Recovery
        4. Post-Incident Activities
        """

        response_plan = self.generation_engine.generate(prompt)
        logging.info("Response plan generated.")
        return response_plan

if __name__ == '__main__':
    # This is a mock-up for demonstration purposes.
    # In a real system, these would be fully implemented components.
    class MockRetrievalEngine:
        def retrieve(self, query, top_k):
            from langchain_core.documents import Document
            print(f"MockRetrievalEngine: Retrieving top {top_k} for '{query[:30]}...'")
            return [Document(page_content="Context about similar past incidents...")]

    class MockGenerationEngine:
        def generate(self, prompt):
            print(f"MockGenerationEngine: Generating for prompt '{prompt[:50]}...'")
            return "Generated response based on the prompt."

    # Example Usage
    mock_retriever = MockRetrievalEngine()
    mock_generator = MockGenerationEngine()

    defense_agent = CyberDefenseAgent(retrieval_engine=mock_retriever, generation_engine=mock_generator)

    sample_alert = {
        "id": "ALERT-001",
        "type": "Suspicious Login",
        "description": "Multiple failed login attempts from IP 192.168.1.100 followed by a successful login.",
        "timestamp": "2025-08-07T10:00:00Z"
    }

    analysis = defense_agent.analyze_alert(sample_alert)
    print("\n--- Analysis Report ---")
    print(analysis['analysis'])

    response = defense_agent.propose_response_plan(analysis)
    print("\n--- Proposed Response Plan ---")
    print(response)
