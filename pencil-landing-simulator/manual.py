import warnings
warnings.filterwarnings("ignore")

import pygame

from agents.dqn import BaseAgent
from environments.ground import GroundEnvironment


# Set up agent and environment
agent = BaseAgent(800, 450)
environment = GroundEnvironment(agent, (800, 900))

# Store which keys have been pressed down or up
action = [0, 0, 0]
keys = [False, False, False]

environment.reset()
while environment.running:
    # Process pygame events
    events = pygame.event.get()
    for event in events:
        # Check for manual exit
        if event.type == pygame.QUIT:
            environment.running = False
        
        # Check for key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                keys[0] = True
            if event.key == pygame.K_LEFT:
                keys[1] = True
            if event.key == pygame.K_RIGHT:
                keys[2] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                keys[0] = False
            if event.key == pygame.K_LEFT:
                keys[1] = False
            if event.key == pygame.K_RIGHT:
                keys[2] = False

    # Convert key presses to actions
    for i in range(len(keys)):
        if keys[i]:
            action[i] = 1
        else:
            action[i] = 0
    
    environment.step(action)

    # Render environment at N fps
    environment.render()
    environment.clock.tick(30)
