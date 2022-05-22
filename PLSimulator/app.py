import pygame

from PLSimulator.log import Log
from PLSimulator.agents.agent import BaseAgent
from PLSimulator.environments.environment import BaseEnvironment
from PLSimulator.environments.planet import EarthEnvironment, MarsEnvironment


def manual(environment: BaseEnvironment, fps: int = 30) -> None:
    '''
        Let the user control the landing in the environment given

        Parameters:
            environment: The environment to run the game in
            fps: Frame rate for rendering the environment

        Returns:
            None
    '''
    # Set up environment
    environment.reset()

    # Store which keys have been pressed down or up
    action = [0, 0, 0]
    keys = [False, False, False]

    # Iterate until environment has finished
    while environment.running:
        # Process pygame events
        events = pygame.event.get()
        for event in events:
            # Check for manual exit
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
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
                action[i] = 1.5
            else:
                action[i] = 0

        # Update the environment with the action
        environment.step(action)

        # Render environment at N fps
        environment.render()
        environment.clock.tick(fps)


def simulate(agent: BaseAgent, environment: BaseEnvironment, fps: int = 30) -> None:
    '''
        Let the agent control the landing in the environment given

        Parameters:
            agent: The agent to put in the environment
            environment: The environment to run the game in
            fps: Frame rate for rendering the environment

        Returns:
            None
    '''
    # Set up environment
    environment.reset()

    # Iterate until environment has finished
    while environment.running:
        # Step through environment once
        state = environment.state(agent)

        # Get action of the agent
        action = agent.get_action(state)

        # Update the environment with the action
        environment.step(action)

        # Render environment at N fps
        environment.render()
        environment.clock.tick(fps)


def main(args: dict) -> None:
    '''
        Process the arguments and determine the top-level functions to execute

        Parameters:
            args: Dict of arguments input from the user

        Returns:
            None
    '''
    # Initialise the agent
    if args.agent == 'dqn':
        agent = BaseAgent()  # TODO: DQNAgent()
    elif args.agent == 'ppo':
        agent = BaseAgent()  # TODO: PPOAgent()
    elif args.agent == 'manual':
        agent = BaseAgent()
    else:
        Log.error(f"Could not load agent '{args.agent}'.")
    
    # Initialise the environment
    if args.env == 'space':
        environment = EarthEnvironment(agent)
    else:
        Log.error(f"Could not load environment '{args.env}'.")

    # Simulate the environment
    if args.agent == 'manual':
        manual(environment)
    else:
        # TODO: Train agent if needed
        simulate(agent, environment)
