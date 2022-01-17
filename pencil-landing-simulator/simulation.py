import warnings
warnings.filterwarnings("ignore")

import pygame

from agents.dqn import DQNAgent
from environments.ground import GroundEnvironment


# Set up agent and environment
agent = DQNAgent(800, 450)
environment = GroundEnvironment(agent)

# Train model
# agent.train(environment)

# Test model
environment.reset()
while environment.running:
    environment.render()

    # Process pygame events
    events = pygame.event.get()
    for event in events:
        # Check for manual exit
        if event.type == pygame.QUIT:
            environment.running = False
        
    
    # Step through environment once
    state = environment.get_state()
    action = agent.get_action(state)
    environment.step(action)

    # Render environment at N fps
    environment.clock.tick(30)
