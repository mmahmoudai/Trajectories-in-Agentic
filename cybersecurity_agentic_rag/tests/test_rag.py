import pytest
from langchain_core.documents import Document
from cybersecurity_agentic_rag.src.rag.retrieval_engine import RetrievalEngine
from cybersecurity_agentic_rag.src.rag.generation_engine import GenerationEngine

@pytest.fixture
def sample_documents():
    """Provides a list of sample documents for testing."""
    return [
        Document(page_content="Ransomware is a type of malicious software."),
        Document(page_content="A zero-day vulnerability is a security flaw unknown to the vendor."),
        Document(page_content="Phishing attacks use social engineering to trick users."),
    ]

@pytest.fixture
def retrieval_engine(sample_documents):
    """Provides an initialized RetrievalEngine instance."""
    return RetrievalEngine(documents=sample_documents)

def test_retrieval_engine_initialization(retrieval_engine, sample_documents):
    """
    Tests if the RetrievalEngine is initialized correctly.
    """
    assert retrieval_engine.retriever is not None
    assert retrieval_engine.vector_store is not None
    # The FAISS index should have the same number of documents as the input
    assert retrieval_engine.vector_store.index.ntotal == len(sample_documents)

def test_retrieve_documents(retrieval_engine):
    """
    Tests if the retrieve method returns documents.
    This is a functional test, not a quality assessment.
    """
    query = "What is ransomware?"
    results = retrieval_engine.retrieve(query, top_k=1)

    assert isinstance(results, list)
    assert len(results) > 0
    assert isinstance(results[0], Document)
    # Because we use FakeEmbeddings, the results are deterministic.
    # The first document should be the most similar to the query in this mock setup.
    assert "Ransomware" in results[0].page_content

def test_add_documents(retrieval_engine):
    """
    Tests if new documents can be added to the retrieval engine.
    """
    initial_doc_count = retrieval_engine.vector_store.index.ntotal

    new_docs = [Document(page_content="A firewall is a network security device.")]
    retrieval_engine.add_documents(new_docs)

    assert retrieval_engine.vector_store.index.ntotal == initial_doc_count + 1

    # Test if the new document can be retrieved
    query = "firewall"
    results = retrieval_engine.retrieve(query, top_k=1)
    assert "firewall" in results[0].page_content

def test_generation_engine():
    """
    Tests the GenerationEngine with its default mock LLM.
    """
    gen_engine = GenerationEngine()

    prompt = "Describe the incident."
    response = gen_engine.generate(prompt)

    assert isinstance(response, str)
    assert len(response) > 0
    # The FakeListLLM cycles through responses, so the first one should be this.
    assert "phishing campaign" in response
