import logging
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FakeEmbeddings
from langchain_core.documents import Document

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RetrievalEngine:
    """
    The Retrieval Engine is responsible for fetching relevant information from a
    knowledge base (represented as a vector store) in response to a query.
    """

    def __init__(self, documents=None, embeddings=None):
        """
        Initializes the Retrieval Engine.

        Args:
            documents (list, optional): A list of Document objects to be indexed.
            embeddings (object, optional): An embedding model instance. Defaults to FakeEmbeddings.
        """
        logging.info("Initializing Retrieval Engine.")
        if embeddings is None:
            self.embeddings = FakeEmbeddings(size=768)
            logging.info("Using FakeEmbeddings for demonstration.")
        else:
            self.embeddings = embeddings

        if documents:
            self.vector_store = self._create_vector_store(documents)
            self.retriever = self.vector_store.as_retriever()
            logging.info("Vector store created and retriever is ready.")
        else:
            self.vector_store = None
            self.retriever = None
            logging.warning("No documents provided. Retrieval will not function.")

    def _create_vector_store(self, documents):
        """Creates a FAISS vector store from the given documents."""
        logging.info(f"Creating vector store from {len(documents)} documents.")
        try:
            vector_store = FAISS.from_documents(documents, self.embeddings)
            return vector_store
        except Exception as e:
            logging.error(f"Failed to create vector store: {e}")
            return None

    def add_documents(self, new_documents):
        """Adds new documents to the existing vector store."""
        if not self.vector_store:
            self.vector_store = self._create_vector_store(new_documents)
            self.retriever = self.vector_store.as_retriever()
            logging.info("New vector store created with provided documents.")
        else:
            logging.info(f"Adding {len(new_documents)} new documents to the vector store.")
            self.vector_store.add_documents(new_documents)
            self.retriever = self.vector_store.as_retriever()
            logging.info("Vector store updated.")


    def retrieve(self, query, top_k=5):
        """
        Retrieves the top_k most relevant documents for a given query.

        Args:
            query (str): The query string.
            top_k (int): The number of documents to retrieve.

        Returns:
            list: A list of relevant Document objects.
        """
        if not self.retriever:
            logging.error("Retriever is not initialized. Cannot retrieve.")
            return []

        logging.info(f"Retrieving top {top_k} documents for query: '{query[:50]}...'")
        try:
            self.retriever.search_kwargs = {'k': top_k}
            results = self.retriever.invoke(query)
            logging.info(f"Found {len(results)} relevant documents.")
            return results
        except Exception as e:
            logging.error(f"An error occurred during retrieval: {e}")
            return []

if __name__ == '__main__':
    # Example Usage
    sample_docs = [
        Document(page_content="MITRE ATT&CK technique T1548 involves privilege escalation."),
        Document(page_content="CVE-2021-44228, also known as Log4Shell, is a critical vulnerability in Apache Log4j."),
        Document(page_content="Phishing attacks often use deceptive emails to steal credentials."),
        Document(page_content="A common indicator of compromise (IOC) is a suspicious IP address."),
        Document(page_content="The cyber threat actor APT28 is also known as Fancy Bear."),
    ]

    retrieval_engine = RetrievalEngine(documents=sample_docs)

    # Perform a retrieval
    query = "information about vulnerabilities"
    retrieved_docs = retrieval_engine.retrieve(query, top_k=2)

    print(f"\n--- Retrieval Results for query: '{query}' ---")
    for doc in retrieved_docs:
        print(f"- {doc.page_content}")

    # Add more documents
    new_docs = [
        Document(page_content="Ransomware encrypts files and demands a payment for decryption."),
        Document(page_content="Zero-day vulnerabilities are flaws that are unknown to the vendor.")
    ]
    retrieval_engine.add_documents(new_docs)

    query2 = "what is ransomware?"
    retrieved_docs2 = retrieval_engine.retrieve(query2, top_k=1)

    print(f"\n--- Retrieval Results for query: '{query2}' ---")
    for doc in retrieved_docs2:
        print(f"- {doc.page_content}")
