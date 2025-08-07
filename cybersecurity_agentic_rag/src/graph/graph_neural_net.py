import logging
import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from torch_geometric.data import Data

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GCN(torch.nn.Module):
    """
    A simple Graph Convolutional Network (GCN) for node classification.
    This model can be used to classify entities in the knowledge graph,
    for example, to identify malicious IPs or tools.
    """
    def __init__(self, num_node_features, num_classes):
        super(GCN, self).__init__()
        self.conv1 = GCNConv(num_node_features, 16)
        self.conv2 = GCNConv(16, num_classes)
        logging.info(f"GCN model initialized with {num_node_features} features and {num_classes} classes.")

    def forward(self, data):
        x, edge_index = data.x, data.edge_index

        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, training=self.training)
        x = self.conv2(x, edge_index)

        return F.log_softmax(x, dim=1)

def train_gnn(model, data, epochs=10):
    """
    A placeholder function demonstrating the GNN training loop.
    In a real scenario, this would be a complete training pipeline.
    """
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)
    model.train()

    logging.info("Starting GNN training (demonstration).")
    for epoch in range(epochs):
        optimizer.zero_grad()
        out = model(data)
        # Assuming a 'y' attribute in data for labels
        loss = F.nll_loss(out[data.train_mask], data.y[data.train_mask])
        loss.backward()
        optimizer.step()
        logging.info(f"Epoch {epoch+1:02d}, Loss: {loss.item():.4f}")
    logging.info("GNN training (demonstration) finished.")

def predict(model, data):
    """
    Uses the trained GNN model to make predictions.
    """
    model.eval()
    _, pred = model(data).max(dim=1)
    return pred

if __name__ == '__main__':
    # This is a demonstration of how the GNN would be used.
    # It requires a graph with node features and labels.

    # Example: Classify nodes in a graph as 'Benign' (0) or 'Malicious' (1)
    num_nodes = 4
    num_features = 8
    num_classes = 2

    # Create a sample graph data object
    # Node features (e.g., embeddings from a text description)
    x = torch.randn(num_nodes, num_features)

    # Edges in the graph
    edge_index = torch.tensor([[0, 1, 1, 2, 2, 3],
                               [1, 0, 2, 1, 3, 2]], dtype=torch.long)

    # Labels (e.g., 0 for benign, 1 for malicious)
    y = torch.tensor([0, 0, 1, 1], dtype=torch.long)

    # Create a PyG Data object
    graph_data = Data(x=x, edge_index=edge_index, y=y)

    # Define which nodes to use for training
    graph_data.train_mask = torch.tensor([True, True, True, True], dtype=torch.bool)

    # Initialize the GCN model
    model = GCN(num_node_features=num_features, num_classes=num_classes)
    print("GCN Model Structure:")
    print(model)

    # Demonstrate the training loop
    print("\n--- GNN Training (Demonstration) ---")
    train_gnn(model, graph_data, epochs=2) # Running for only 2 epochs for demonstration

    # Demonstrate prediction
    print("\n--- GNN Prediction (Demonstration) ---")
    predictions = predict(model, graph_data)
    print(f"Node predictions: {predictions.numpy()}")
    print(f"Actual labels:    {y.numpy()}")

    correct = (predictions == y).sum()
    accuracy = int(correct) / len(y)
    print(f"Accuracy: {accuracy:.2f}")
