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
    
    def get_action(self, state: list) -> list:
        return self.model.compute_action(state)

    def get_saved(self):
        return None

    def train(self, environment_name):
        self.model = ppo.PPOTrainer(env=environment_name)

        # for i in range(100):
        #     self.model.train()
        #     print(i)
        # print("training complete")