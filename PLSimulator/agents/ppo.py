import os
from ray.rllib.agents import ppo

from PLSimulator.agents.agent import BaseAgent


class PPOAgent(BaseAgent):
    '''
        PPOAgent

        This agent uses a PPO model for training and controlling the agent
    '''

    def __init__(self, env_config):
        super().__init__("ppo", env_config["name"])

        config = ppo.DEFAULT_CONFIG.copy()
        config["log_level"] = "WARN"
        config["num_workers"] = 1
        config["num_sgd_iter"] = 10
        config["sgd_minibatch_size"] = 250
        config["env_config"] = env_config
        self.model = ppo.PPOTrainer(config, env_config["name"])

    def train(self):
        return self.model.train()

    def step(self, state: list) -> list:
        return self.model.compute_single_action(state)

    def save(self):
        self.model.save(self._model_dir)

    def load(self, number):
        if number == 'last':
            number = max([int(c[11:]) for c in os.listdir(self._model_dir) if c.startswith("checkpoint")])

        self.model.restore(
            os.path.join(
                self._model_dir,
                f"checkpoint_{str(number).zfill(6)}",
                f"checkpoint-{number}"
            )
        )
