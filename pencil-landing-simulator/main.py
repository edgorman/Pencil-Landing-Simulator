import warnings
warnings.filterwarnings("ignore")

import pygame

from agent import DQNAgent
from environment import BaseEnvironment


# Set up agent and environment
agent = DQNAgent(800, 450)
environment = BaseEnvironment(agent)

# Train model
# agent.train(environment)

# Test model
environment.reset()
while environment.running:
    # Check for manual exit
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            environment.running = False
    
    # Pass through one game loop
    state = environment.get_state()
    action = agent.get_action(state)
    environment.step(action)
    environment.render()

    # Tick keeps render at N FPS
    environment.clock.tick(30)
