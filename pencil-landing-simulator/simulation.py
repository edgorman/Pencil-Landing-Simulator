import warnings
warnings.filterwarnings("ignore")

from agents.dqn import DQNAgent
from environments.ground import GroundEnvironment


# Set up agent and environment
agent = DQNAgent(800, 450)
environment = GroundEnvironment(agent, (800, 900))

# Train model
# agent.train(environment)

# Test model
environment.reset()
while environment.running:    
    # Step through environment once
    state = environment.get_state()
    action = agent.get_action(state)
    environment.step(action)

    # Render environment at N fps
    environment.render()
    environment.clock.tick(30)
