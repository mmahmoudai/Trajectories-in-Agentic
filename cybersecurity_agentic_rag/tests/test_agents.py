import pytest
from unittest.mock import MagicMock
from cybersecurity_agentic_rag.src.agents.knowledge_agent import KnowledgeAgent
from cybersecurity_agentic_rag.src.agents.cyber_defense_agent import CyberDefenseAgent

# --- Tests for KnowledgeAgent ---

@pytest.fixture
def mock_knowledge_graph():
    """Provides a mock KnowledgeGraph object for testing."""
    mock_kg = MagicMock()
    mock_kg.find_related_nodes.return_value = [('APT41', 'uses_tool', 'Cobalt Strike')]
    return mock_kg

@pytest.fixture
def knowledge_agent(mock_knowledge_graph):
    """Provides a KnowledgeAgent initialized with a mock KG."""
    return KnowledgeAgent(knowledge_graph=mock_knowledge_graph)

def test_knowledge_agent_query(knowledge_agent, mock_knowledge_graph):
    """
    Tests if the KnowledgeAgent correctly calls the KG's query method.
    """
    query = "find related entities to 'APT41'"
    result = knowledge_agent.query_knowledge_graph(query)

    # Assert that the mock KG's method was called with the correct argument
    mock_knowledge_graph.find_related_nodes.assert_called_once_with('APT41')

    # Assert that the agent returns the value from the mock KG
    assert len(result) == 1
    assert result[0] == ('APT41', 'uses_tool', 'Cobalt Strike')

def test_knowledge_agent_add_information(knowledge_agent, mock_knowledge_graph):
    """
    Tests if the KnowledgeAgent correctly calls the KG's add method.
    """
    knowledge_agent.add_information('CVE-123', 'is_related_to', 'Malware-X')

    # Assert that the mock KG's method was called with the correct arguments
    mock_knowledge_graph.add_triple.assert_called_once_with('CVE-123', 'is_related_to', 'Malware-X')

# --- Tests for CyberDefenseAgent ---

@pytest.fixture
def mock_retrieval_engine():
    """Provides a mock RetrievalEngine."""
    mock_retriever = MagicMock()
    mock_retriever.retrieve.return_value = [MagicMock(page_content="mocked context")]
    return mock_retriever

@pytest.fixture
def mock_generation_engine():
    """Provides a mock GenerationEngine."""
    mock_generator = MagicMock()
    mock_generator.generate.return_value = "This is a generated analysis."
    return mock_generator

@pytest.fixture
def defense_agent(mock_retrieval_engine, mock_generation_engine):
    """Provides a CyberDefenseAgent with mock dependencies."""
    return CyberDefenseAgent(retrieval_engine=mock_retrieval_engine, generation_engine=mock_generation_engine)

def test_cyber_defense_agent_analyze_alert(defense_agent, mock_retrieval_engine, mock_generation_engine):
    """
    Tests the analyze_alert workflow of the CyberDefenseAgent.
    """
    alert_data = {'id': 'ALERT-TEST-1', 'description': 'A test alert.'}
    analysis = defense_agent.analyze_alert(alert_data)

    # Check if the retrieval engine was called
    mock_retrieval_engine.retrieve.assert_called_once()

    # Check if the generation engine was called
    mock_generation_engine.generate.assert_called_once()

    # Check if the output is as expected from the mock generator
    assert analysis['analysis'] == "This is a generated analysis."
