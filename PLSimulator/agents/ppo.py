from ray.rllib.agents import ppo

from PLSimulator.agents.agent import BaseAgent


class PPOAgent(BaseAgent):
    '''
        PPOAgent

        This agent uses a PPO model for training and controlling the agent
    '''

    def __init__(self):
        super().__init__()

        self.model = None
    
    def init_model(self, env):
        config = ppo.DEFAULT_CONFIG.copy()
        config["log_level"] = "WARN"
        config["num_workers"] = 1
        config["num_sgd_iter"] = 10
        config["sgd_minibatch_size"] = 250

        self.model = ppo.PPOTrainer(config, env)
    
    def train(self):
        return self.model.train()
    
    def step(self, state: list) -> list:
        return self.model.compute_action(state)

    def save(self):
        self.model.save(self.model_dir)
    
    def load(self):
        return None
    
    def clear(self):
        super().clear("ppo")
