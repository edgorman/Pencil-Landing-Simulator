import pygame

from agent import BaseAgent
from environment import BaseEnvironment


# Set up agent and environment
agent = BaseAgent(800, 450)
environment = BaseEnvironment(agent)

environment.reset()

# Iterate until environment has ceased
while environment.running:
    # Check for manual exit
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            environment.running = False
    
    # Render the environment
    environment.render()

    # Get the state of the environment
    state = environment.get_state()

    # Get the action from the agent
    action = agent.get_action(state)

    # Get result of action in environment
    reward, info = environment.step(action)

    # Tick
    environment.clock.tick(30)

# Calculate final reward now environment is complete
print("finished")