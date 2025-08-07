import logging
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Note: Figure 1 (System Architecture) is a conceptual diagram and should be created
# using a dedicated diagramming tool like diagrams.net (formerly draw.io) or PowerPoint.

OUTPUT_DIR = "visualizations"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def plot_performance_comparison(results_df: pd.DataFrame, filename="figure_2_performance_comparison.png"):
    """
    Generates and saves a bar chart comparing the performance of different systems.
    This corresponds to Figure 2 in the paper.

    Args:
        results_df (pd.DataFrame): DataFrame with columns ['System', 'Precision', 'Recall', 'F1-Score', 'Accuracy'].
        filename (str): The filename to save the plot to.
    """
    filepath = os.path.join(OUTPUT_DIR, filename)

    melted_df = results_df.melt(id_vars='System', var_name='Metric', value_name='Score')

    plt.figure(figsize=(10, 6))
    ax = sns.barplot(data=melted_df, x='Metric', y='Score', hue='System', palette='viridis')

    plt.title('Performance Comparison: Agentic RAG vs. Baselines', fontsize=16)
    plt.ylabel('Score', fontsize=12)
    plt.xlabel('Metric', fontsize=12)
    plt.ylim(0, 1.05)
    plt.legend(title='System')

    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 9), textcoords='offset points')

    plt.tight_layout()
    plt.savefig(filepath, dpi=300)
    logging.info(f"Performance comparison plot saved to {filepath}")
    plt.close()

def plot_ablation_study(ablation_df: pd.DataFrame, filename="figure_3_ablation_study.png"):
    """
    Generates and saves a bar chart showing the results of an ablation study.
    This corresponds to Figure 3 in the paper.

    Args:
        ablation_df (pd.DataFrame): DataFrame with columns ['Configuration', 'f1_score'].
        filename (str): The filename to save the plot to.
    """
    filepath = os.path.join(OUTPUT_DIR, filename)

    plt.figure(figsize=(12, 7))
    sorted_df = ablation_df.sort_values('f1_score', ascending=False)
    ax = sns.barplot(data=sorted_df, x='f1_score', y='Configuration', palette='plasma')

    plt.title('Ablation Study: Impact of Components on F1-Score', fontsize=16)
    plt.xlabel('F1-Score', fontsize=12)
    plt.ylabel('System Configuration', fontsize=12)
    plt.xlim(0, 1.0)

    for p in ax.patches:
        width = p.get_width()
        plt.text(width + 0.01, p.get_y() + p.get_height() / 2, f'{width:.3f}', va='center')

    plt.tight_layout()
    plt.savefig(filepath, dpi=300)
    logging.info(f"Ablation study plot saved to {filepath}")
    plt.close()

def plot_confusion_matrix(y_true, y_pred, class_names, filename="figure_4_confusion_matrix.png"):
    """
    Generates and saves a confusion matrix visualization.
    """
    from sklearn.metrics import confusion_matrix
    filepath = os.path.join(OUTPUT_DIR, filename)

    cm = confusion_matrix(y_true, y_pred)

    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
    plt.title('Confusion Matrix', fontsize=16)
    plt.ylabel('True Label', fontsize=12)
    plt.xlabel('Predicted Label', fontsize=12)

    plt.tight_layout()
    plt.savefig(filepath, dpi=300)
    logging.info(f"Confusion matrix plot saved to {filepath}")
    plt.close()

def plot_training_rewards(log_dir, filename="figure_5_rl_training_rewards.png"):
    """
    Plots the training rewards from a Stable Baselines 3 log file.

    Args:
        log_dir (str): The directory containing the monitor.csv file.
        filename (str): The filename for the saved plot.
    """
    filepath = os.path.join(OUTPUT_DIR, filename)
    monitor_path = os.path.join(log_dir, "monitor.csv")

    if not os.path.exists(monitor_path):
        logging.warning(f"Monitor log not found at {monitor_path}. Cannot plot rewards.")
        return

    df = pd.read_csv(monitor_path, skiprows=1)

    plt.figure(figsize=(10, 6))
    plt.plot(df['l'], df['r'])
    plt.title('RL Agent Training Progress', fontsize=16)
    plt.xlabel('Episode', fontsize=12)
    plt.ylabel('Episode Reward', fontsize=12)

    plt.tight_layout()
    plt.savefig(filepath, dpi=300)
    logging.info(f"RL training rewards plot saved to {filepath}")
    plt.close()

if __name__ == '__main__':
    # --- Example Usage ---
    # This demonstrates how the functions would be called from an experiment script or notebook.

    # 1. Plot Performance Comparison
    baseline_data = {
        'System': ['Agentic RAG (Ours)', 'Baseline RAG', 'GNN Classifier'],
        'Precision': [0.91, 0.75, 0.88],
        'Recall': [0.93, 0.81, 0.82],
        'F1-Score': [0.92, 0.78, 0.85],
        'Accuracy': [0.94, 0.80, 0.87]
    }
    baseline_df = pd.DataFrame(baseline_data)
    plot_performance_comparison(baseline_df)

    # 2. Plot Ablation Study
    ablation_data = {
        'Configuration': ['Full System', 'No Knowledge Graph', 'No RL Policy', 'Baseline RAG'],
        'f1_score': [0.92, 0.84, 0.89, 0.78]
    }
    ablation_df = pd.DataFrame(ablation_data)
    plot_ablation_study(ablation_df)

    # 3. Plot Confusion Matrix
    true_labels = [1, 0, 1, 1, 0, 1, 0, 0, 1, 1]
    pred_labels = [1, 1, 1, 0, 0, 1, 0, 1, 1, 0]
    plot_confusion_matrix(true_labels, pred_labels, class_names=['Benign', 'Malicious'])

    print(f"All sample visualizations have been generated in the '{OUTPUT_DIR}' directory.")
