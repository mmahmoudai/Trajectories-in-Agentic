import logging
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_community.llms.fake import FakeListLLM

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GenerationEngine:
    """
    The Generation Engine is responsible for generating coherent and contextually
    relevant text based on a given prompt and retrieved information.
    """

    def __init__(self, llm=None):
        """
        Initializes the Generation Engine.

        Args:
            llm (object, optional): A language model instance that follows the LangChain interface.
                                    Defaults to a FakeListLLM for demonstration.
        """
        logging.info("Initializing Generation Engine.")
        if llm is None:
            # Responses for the fake LLM to cycle through
            responses = [
                "Based on the context, the primary threat is a sophisticated phishing campaign.",
                "The recommended action is to isolate the affected systems and block the malicious domain.",
                "This activity is consistent with the tactics, techniques, and procedures (TTPs) of the threat actor FIN7.",
                "A full report has been generated and sent to the security operations center.",
            ]
            self.llm = FakeListLLM(responses=responses)
            logging.info("Using FakeListLLM for demonstration.")
        else:
            self.llm = llm

        # A generic prompt template that can be adapted
        self.prompt_template = PromptTemplate(
            input_variables=['input_text'],
            template="You are a helpful cybersecurity analyst AI. Based on the following information, provide a concise summary:\n\n{input_text}\n\nSummary:"
        )

        self.chain = RunnableSequence(self.prompt_template, self.llm)
        logging.info("Generation chain is ready.")

    def generate(self, input_text):
        """
        Generates text based on the provided input.

        Args:
            input_text (str): The input text or a formatted prompt.

        Returns:
            str: The generated text.
        """
        logging.info(f"Generating text for input: '{input_text[:80]}...'")
        try:
            response = self.chain.invoke({"input_text": input_text})
            logging.info("Text generation successful.")
            return response
        except Exception as e:
            logging.error(f"An error occurred during text generation: {e}")
            return "Error: Could not generate a response."

    def generate_with_custom_prompt(self, prompt_template, **kwargs):
        """
        Generates text using a custom prompt template.

        Args:
            prompt_template (PromptTemplate): A LangChain PromptTemplate object.
            **kwargs: The variables to be passed to the prompt template.

        Returns:
            str: The generated text.
        """
        logging.info("Generating text with a custom prompt.")
        try:
            custom_chain = RunnableSequence(prompt_template, self.llm)
            response = custom_chain.invoke(kwargs)
            logging.info("Custom prompt generation successful.")
            return response
        except Exception as e:
            logging.error(f"An error occurred during custom prompt generation: {e}")
            return "Error: Could not generate a response from custom prompt."


if __name__ == '__main__':
    # Example Usage
    generation_engine = GenerationEngine()

    # 1. Simple generation using the default prompt
    simple_input = "Context: A suspicious login was detected from an unrecognized IP address. Analysis: This matches known brute-force attack patterns."
    simple_output = generation_engine.generate(simple_input)

    print("\n--- Simple Generation Output ---")
    print(simple_output)

    # 2. Generation with a custom prompt for a specific task
    report_generation_template = PromptTemplate(
        input_variables=['alert_id', 'threat_info', 'ioc_list'],
        template="""
        Generate a formal incident report.
        Alert ID: {alert_id}
        Threat Information: {threat_info}
        Indicators of Compromise: {ioc_list}

        Report:
        """
    )

    custom_output = generation_engine.generate_with_custom_prompt(
        report_generation_template,
        alert_id="ALERT-007",
        threat_info="Potential data exfiltration attempt.",
        ioc_list="IP: 123.45.67.89, Domain: maliciousexfil.com"
    )

    print("\n--- Custom Prompt Generation Output ---")
    print(custom_output)
