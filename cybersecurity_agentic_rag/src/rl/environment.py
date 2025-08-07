import logging
import gymnasium as gym
from gymnasium import spaces
import numpy as np
fromcybersecurity_agentic_rag.src.rl.reward_functions import calculate_reward

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CybersecurityEnv(gym.Env):
    """
    A custom reinforcement learning environment for simulating cybersecurity defense scenarios.

    - Observation Space: Represents the state of the system, e.g., features of a security alert.
    - Action Space: Represents the possible actions a defense agent can take.
    """
    metadata = {'render_modes': ['human']}

    def __init__(self, reward_function=calculate_reward):
        super(CybersecurityEnv, self).__init__()

        self.reward_function = reward_function

        # Define the action space
        # Example actions: 0=Ignore, 1=Quarantine Host, 2=Block IP
        self.action_space = spaces.Discrete(3)

        # Define the observation space
        # Example observation: [alert_severity, asset_criticality, confidence_score]
        # All values are normalized between 0 and 1.
        self.observation_space = spaces.Box(low=0, high=1, shape=(3,), dtype=np.float32)

        # Internal state
        self._state = None
        self._episode_step = 0
        self.max_steps_per_episode = 10 # An episode ends after a fixed number of alerts

        logging.info("CybersecurityEnv initialized.")

    def _generate_mock_alert(self):
        """Generates a new, random security alert for the agent to process."""
        severity = np.random.rand()  # e.g., how severe the alert is rated
        criticality = np.random.rand() # e.g., how critical the affected asset is
        confidence = np.random.rand() # e.g., how confident the detection system is

        # The 'ground_truth' indicates if it's a real threat (1) or a false positive (0)
        # This is hidden from the agent but used for reward calculation.
        self._ground_truth = 1 if (severity > 0.7 and criticality > 0.5) else 0

        return np.array([severity, criticality, confidence], dtype=np.float32)

    def reset(self, seed=None, options=None):
        """Resets the environment to an initial state."""
        super().reset(seed=seed)
        self._state = self._generate_mock_alert()
        self._episode_step = 0
        logging.info("Environment reset.")
        return self._state, {} # Return observation and info dict

    def step(self, action):
        """
        Executes one time step within the environment.

        Args:
            action: The action taken by the agent.

        Returns:
            tuple: A tuple containing (observation, reward, terminated, truncated, info).
        """
        if self._state is None:
            raise RuntimeError("Cannot call step() before reset().")

        # Determine the outcome of the action
        # Action 0: Ignore
        # Action 1: Quarantine Host
        # Action 2: Block IP

        # This is a simplified logic for demonstration
        is_correct_action = (self._ground_truth == 1 and action in [1, 2]) or \
                              (self._ground_truth == 0 and action == 0)

        # Calculate reward
        reward = self.reward_function(action, self._ground_truth, is_correct_action)

        self._episode_step += 1
        terminated = self._episode_step >= self.max_steps_per_episode
        truncated = False # Not using time limits that truncate the episode in a different way

        # Get the next state (next alert)
        self._state = self._generate_mock_alert()

        info = {'ground_truth': self._ground_truth, 'correct_action': is_correct_action}

        logging.debug(f"Step {self._episode_step}: Action={action}, Reward={reward:.2f}, Terminated={terminated}")

        return self._state, reward, terminated, truncated, info

    def render(self, mode='human'):
        """Renders the environment state."""
        if mode == 'human':
            print(f"Step: {self._episode_step}, State (Alert): {self._state}, Ground Truth: {'Real Threat' if self._ground_truth else 'False Positive'}")

    def close(self):
        """Performs any necessary cleanup."""
        logging.info("CybersecurityEnv closed.")


if __name__ == '__main__':
    # Example of how to use the environment
    env = CybersecurityEnv()

    # Check the environment (optional, good practice)
    from stable_baselines3.common.env_checker import check_env
    try:
        check_env(env)
        print("Environment check passed!")
    except Exception as e:
        print(f"Environment check failed: {e}")


    obs, _ = env.reset()
    env.render()

    for i in range(5):
        action = env.action_space.sample() # Take a random action
        obs, reward, terminated, truncated, info = env.step(action)

        print(f"Action taken: {action}")
        env.render()
        print(f"Reward: {reward:.2f}, Info: {info}")

        if terminated:
            print("Episode finished.")
            obs, _ = env.reset()
            env.render()

    env.close()
