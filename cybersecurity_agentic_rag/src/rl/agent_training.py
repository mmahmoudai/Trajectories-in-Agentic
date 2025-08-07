import logging
import os
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
fromcybersecurity_agentic_rag.src.rl.environment import CybersecurityEnv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def train_agent(env, total_timesteps=10000, model_save_path="models/ppo_cybersecurity"):
    """
    Trains a PPO agent on the CybersecurityEnv.

    Args:
        env: The reinforcement learning environment.
        total_timesteps (int): The total number of steps to train for.
        model_save_path (str): The path to save the trained model.
    """
    logging.info(f"Starting training for {total_timesteps} timesteps.")

    # Use PPO, a popular and versatile RL algorithm
    # 'MlpPolicy' means the agent will use a Multi-Layer Perceptron network
    model = PPO("MlpPolicy", env, verbose=0)

    # The learn() method starts the training process
    model.learn(total_timesteps=total_timesteps)

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)

    # Save the trained model
    model.save(model_save_path)
    logging.info(f"Model saved to {model_save_path}.zip")

    return model

def evaluate_agent(env, model, num_episodes=10):
    """
    Evaluates the trained agent's performance.
    """
    logging.info(f"Evaluating agent for {num_episodes} episodes.")

    for episode in range(num_episodes):
        obs, _ = env.reset()
        done = False
        total_reward = 0

        while not done:
            action, _states = model.predict(obs, deterministic=True)
            obs, reward, done, truncated, info = env.step(action)
            total_reward += reward
            if done or truncated:
                break

        logging.info(f"Episode {episode + 1}: Total Reward = {total_reward:.2f}")

if __name__ == '__main__':
    # --- Training and Evaluation Pipeline ---

    # 1. Create the environment
    # make_vec_env is a helper function to create vectorized environments,
    # which can speed up training. Here we use just one environment.
    vec_env = make_vec_env(CybersecurityEnv, n_envs=1)

    # 2. Train the agent
    # Note: 1000 timesteps is very short and only for demonstration.
    # A real training run would require many more steps.
    model_path = "cybersecurity_agentic_rag/models/ppo_cyber_agent"
    trained_model = train_agent(vec_env, total_timesteps=1000, model_save_path=model_path)

    # 3. Evaluate the trained agent
    print("\n--- Evaluating the trained agent ---")
    # It's good practice to evaluate on a separate environment instance
    eval_env = CybersecurityEnv()
    evaluate_agent(eval_env, trained_model, num_episodes=5)
    eval_env.close()

    # 4. Load a saved model and make predictions
    print("\n--- Loading saved model for prediction ---")
    if os.path.exists(f"{model_path}.zip"):
        loaded_model = PPO.load(model_path)

        obs, _ = eval_env.reset()
        print(f"Sample observation: {obs}")

        action, _ = loaded_model.predict(obs)
        print(f"Predicted action for the observation: {action}")
    else:
        print("Model file not found. Skipping loading example.")

    vec_env.close()
