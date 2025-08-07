import pytest
from cybersecurity_agentic_rag.src.graph.knowledge_graph import KnowledgeGraph

@pytest.fixture
def empty_kg():
    """Provides an empty KnowledgeGraph instance for testing."""
    return KnowledgeGraph()

@pytest.fixture
def populated_kg():
    """Provides a KnowledgeGraph instance with some data."""
    kg = KnowledgeGraph()
    kg.add_triple('APT28', 'uses_tool', 'X-Agent')
    kg.add_triple('APT28', 'targets_sector', 'Government')
    return kg

def test_add_triple(empty_kg):
    """
    Tests if a triple is added correctly to the knowledge graph.
    """
    assert empty_kg.graph.number_of_nodes() == 0
    assert empty_kg.graph.number_of_edges() == 0

    empty_kg.add_triple('CVE-123', 'has_patch', 'Patch-XYZ')

    assert empty_kg.graph.number_of_nodes() == 2
    assert empty_kg.graph.number_of_edges() == 1
    assert 'CVE-123' in empty_kg.graph
    assert 'Patch-XYZ' in empty_kg.graph
    assert empty_kg.graph.has_edge('CVE-123', 'Patch-XYZ')
    edge_data = empty_kg.graph.get_edge_data('CVE-123', 'Patch-XYZ')
    # In a MultiDiGraph, there can be multiple edges, so we check the first one (key 0)
    assert edge_data[0]['label'] == 'has_patch'

def test_find_related_nodes(populated_kg):
    """
    Tests the find_related_nodes functionality.
    """
    # Test for a node that exists
    related_nodes = populated_kg.find_related_nodes('APT28')
    assert len(related_nodes) == 2

    # Extract just the target nodes for easier checking
    target_nodes = {triple[2] for triple in related_nodes}
    assert 'X-Agent' in target_nodes
    assert 'Government' in target_nodes

    # Test for a node that does not exist
    related_nodes_nonexistent = populated_kg.find_related_nodes('Nonexistent-Node')
    assert len(related_nodes_nonexistent) == 0

def test_subgraph_extraction(populated_kg):
    """
    Tests if a subgraph is extracted correctly.
    """
    entities = ['APT28', 'X-Agent', 'Nonexistent-Node']
    subgraph = populated_kg.get_subgraph_for_entities(entities)

    assert subgraph.number_of_nodes() == 2
    assert subgraph.number_of_edges() == 1
    assert 'APT28' in subgraph
    assert 'X-Agent' in subgraph
    assert 'Nonexistent-Node' not in subgraph
    assert subgraph.has_edge('APT28', 'X-Agent')
    assert not subgraph.has_edge('APT28', 'Government') # This node was not in the entity list
