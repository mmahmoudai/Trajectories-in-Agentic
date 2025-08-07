import logging
import pandas as pd
from cybersecurity_agentic_rag.src.utils.evaluation_metrics import calculate_classification_metrics

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Mock functions simulating different system configurations ---

def run_full_system(dataset):
    """Simulates running the full, integrated system."""
    logging.info("Running full system...")
    # In reality, this would be the complex orchestration from main.py
    # Mocked predictions for demonstration
    return [1, 0, 1, 1, 0]

def run_system_without_graph(dataset):
    """Simulates the system without knowledge graph enrichment."""
    logging.info("Running system without Knowledge Graph...")
    # The CoordinationAgent would skip the knowledge enrichment step.
    # Performance is expected to be slightly worse.
    return [1, 1, 1, 1, 0]

def run_system_without_rl(dataset):
    """Simulates the system with a simple rule-based action model instead of RL."""
    logging.info("Running system without Reinforcement Learning...")
    # The action selection would be based on fixed rules, e.g., "always quarantine if severity > 0.8"
    # This might be less adaptive and perform worse on nuanced cases.
    return [1, 0, 0, 1, 0]

def run_system_without_agentic_coordination(dataset):
    """Simulates a simple, non-agentic RAG pipeline."""
    logging.info("Running system without Agentic Coordination (simple RAG)...")
    # This is equivalent to a baseline RAG system.
    return [0, 1, 0, 1, 1]


def run_ablation_studies(dataset_path):
    """
    Runs a series of ablation studies to evaluate the contribution of each component.
    """
    logging.info("--- Starting Ablation Studies ---")

    # Mock dataset
    mock_data = {
        'query': ["q1", "q2", "q3", "q4", "q5"],
        'true_label': [1, 0, 1, 1, 1] # 1=Action needed, 0=No action
    }
    eval_dataset = pd.DataFrame(mock_data)
    true_labels = eval_dataset['true_label'].tolist()
    logging.info(f"Loaded dataset with {len(eval_dataset)} samples.")

    # --- Run evaluations for each configuration ---
    study_results = {}

    # Full System
    preds_full = run_full_system(eval_dataset)
    study_results['Full System'] = calculate_classification_metrics(true_labels, preds_full)

    # Ablation 1: No Knowledge Graph
    preds_no_graph = run_system_without_graph(eval_dataset)
    study_results['No Knowledge Graph'] = calculate_classification_metrics(true_labels, preds_no_graph)

    # Ablation 2: No Reinforcement Learning
    preds_no_rl = run_system_without_rl(eval_dataset)
    study_results['No RL-based Policy'] = calculate_classification_metrics(true_labels, preds_no_rl)

    # Ablation 3: No Agentic Coordination
    preds_no_agents = run_system_without_agentic_coordination(eval_dataset)
    study_results['No Agentic Logic (Baseline RAG)'] = calculate_classification_metrics(true_labels, preds_no_agents)

    # --- Format and display results ---
    results_df = pd.DataFrame.from_dict(study_results, orient='index')
    results_df = results_df.reset_index().rename(columns={'index': 'Configuration'})

    print("\n--- Ablation Study Results ---")
    print(results_df[['Configuration', 'f1_score', 'precision', 'recall', 'accuracy']])

    results_df.to_csv("experiments/ablation_study_results.csv", index=False)
    logging.info("Ablation study results saved to experiments/ablation_study_results.csv")
    logging.info("\n--- Ablation Studies Finished ---")

if __name__ == '__main__':
    mock_dataset_filepath = "data/processed/evaluation_dataset.csv"
    run_ablation_studies(mock_dataset_filepath)
