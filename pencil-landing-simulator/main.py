import warnings
warnings.filterwarnings("ignore")

import pygame

from agents.dqn import DQNAgent
from environments.ground import GroundEnvironment


# Set up agent and environment
agent = DQNAgent(800, 450)
environment = GroundEnvironment()

# Train model
# agent.train(environment)

# Test model
environment.reset(agent)
while environment.running:
    # Check for manual exit
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            environment.running = False
    
    # Pass through one game loop
    state = environment.get_state(agent)
    action = agent.get_action(state)
    environment.step(agent, action)
    environment.render(agent)

    # Tick keeps render at N FPS
    environment.clock.tick(30)
