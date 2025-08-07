import logging
import time
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_classification_metrics(y_true: list, y_pred: list, average='binary') -> dict:
    """
    Calculates a set of classification metrics.

    Args:
        y_true (list): A list of true labels.
        y_pred (list): A list of predicted labels.
        average (str): The averaging strategy for multi-class classification.
                       'binary' is for binary classification.
                       'micro', 'macro', 'weighted' for multi-class.

    Returns:
        dict: A dictionary containing precision, recall, F1-score, and accuracy.
    """
    if len(y_true) != len(y_pred):
        raise ValueError("Input lists must have the same length.")
    if not y_true:
        logging.warning("Input lists are empty. Returning zero for all metrics.")
        return {'precision': 0, 'recall': 0, 'f1_score': 0, 'accuracy': 0}

    try:
        precision = precision_score(y_true, y_pred, average=average, zero_division=0)
        recall = recall_score(y_true, y_pred, average=average, zero_division=0)
        f1 = f1_score(y_true, y_pred, average=average, zero_division=0)
        accuracy = accuracy_score(y_true, y_pred)

        metrics = {
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'accuracy': accuracy
        }
        logging.info(f"Calculated metrics: {metrics}")
        return metrics
    except Exception as e:
        logging.error(f"Could not calculate metrics: {e}")
        return {'precision': 0, 'recall': 0, 'f1_score': 0, 'accuracy': 0}

class ResponseTimer:
    """
    A context manager to easily time blocks of code.
    """
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.elapsed_time = None

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.perf_counter()
        self.elapsed_time = self.end_time - self.start_time
        logging.info(f"Response time: {self.elapsed_time:.4f} seconds")

if __name__ == '__main__':
    # --- Example Usage ---

    # 1. Classification Metrics
    print("--- Classification Metrics Example ---")
    true_labels = [1, 0, 1, 1, 0, 1, 0, 0, 1]
    pred_labels = [1, 1, 1, 0, 0, 1, 0, 1, 1]

    print(f"True labels: {true_labels}")
    print(f"Pred labels: {pred_labels}")

    metrics = calculate_classification_metrics(true_labels, pred_labels)
    print(f"Calculated Metrics: {metrics}")

    # 2. Response Time Measurement
    print("\n--- Response Time Example ---")
    with ResponseTimer() as timer:
        print("Simulating a task that takes some time...")
        # Simulate work
        time.sleep(0.5)
        print("Task finished.")

    print(f"The task took {timer.elapsed_time:.4f} seconds.")
