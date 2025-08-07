import logging

def calculate_reward(action: int, ground_truth: int, is_correct: bool) -> float:
    """
    Calculates the reward for a given action based on the ground truth.

    Args:
        action (int): The action taken by the agent (0: Ignore, 1: Quarantine, 2: Block).
        ground_truth (int): The actual nature of the alert (0: False Positive, 1: Real Threat).
        is_correct (bool): A pre-calculated boolean indicating if the action was correct.

    Returns:
        float: The calculated reward value.
    """
    if is_correct:
        if ground_truth == 1:
            # True Positive: Agent correctly took action on a real threat.
            reward = 10.0
            logging.debug("Reward: True Positive (+10.0)")
        else:
            # True Negative: Agent correctly ignored a false positive.
            reward = 2.0
            logging.debug("Reward: True Negative (+2.0)")
    else:
        if ground_truth == 1:
            # False Negative: Agent incorrectly ignored a real threat.
            reward = -20.0
            logging.debug("Reward: False Negative (-20.0)")
        else:
            # False Positive: Agent incorrectly took action on a false positive.
            # This is disruptive, so it's penalized, but less than missing a real threat.
            reward = -5.0
            logging.debug("Reward: False Positive (-5.0)")

    return reward


def alternative_reward_function(action: int, ground_truth: int, is_correct: bool) -> float:
    """
    An alternative reward function with a different penalty/reward structure.
    This function could be used to train an agent that is more cautious.
    """
    if is_correct:
        # Higher reward for being correct, regardless of type
        reward = 5.0
    else:
        # Higher penalty for any mistake
        reward = -10.0

    return reward

if __name__ == '__main__':
    # --- Example Usage ---
    print("--- Demonstrating `calculate_reward` function ---")

    # Scenario 1: True Positive (Real Threat, Correct Action)
    r1 = calculate_reward(action=1, ground_truth=1, is_correct=True)
    print(f"Scenario: True Positive -> Reward: {r1}")

    # Scenario 2: False Negative (Real Threat, Incorrect Action)
    r2 = calculate_reward(action=0, ground_truth=1, is_correct=False)
    print(f"Scenario: False Negative -> Reward: {r2}")

    # Scenario 3: True Negative (False Positive, Correct Action)
    r3 = calculate_reward(action=0, ground_truth=0, is_correct=True)
    print(f"Scenario: True Negative -> Reward: {r3}")

    # Scenario 4: False Positive (False Positive, Incorrect Action)
    r4 = calculate_reward(action=2, ground_truth=0, is_correct=False)
    print(f"Scenario: False Positive -> Reward: {r4}")
