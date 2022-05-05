import pygame

from PencilLandingSimulator.log import Log
from PencilLandingSimulator.agents.agent import BaseAgent
from PencilLandingSimulator.environments.environment import BaseEnvironment
from PencilLandingSimulator.environments.ground import GroundEnvironment


def manual(environment: BaseEnvironment, fps: int = 30) -> None:
    '''
        Let the user control the landing in the environment given

        Parameters:
            environment: The environment to run the game in
            fps: Frame rate for rendering the environment

        Returns:
            None
    '''

    # Set up controllable agent in environment
    agent = BaseAgent()
    environment.set_agent(agent)
    environment.reset((800, 0), (0, 0), 0, (0, 0))

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
                action[i] = 1
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
    # Set up agent in environment
    environment.set_agent(agent)
    environment.reset()

    # Iterate until environment has finished
    while environment.running:
        # Step through environment once
        state = environment.get_state()

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
    # Initialise the environment
    if args.env == 'ground':
        environment = GroundEnvironment()
    else:
        Log.error(f"Could not load environment '{args.env}'.")

    # Initialise the agent
    if args.agent == 'dqn':
        agent = BaseAgent()
    elif args.agent == 'ppo':
        agent = BaseAgent()  # TODO: PPOAgent()
    elif args.agent == 'manual':
        pass
    else:
        Log.error(f"Could not load agent '{args.agent}'.")

    # Simulate the environment
    if args.agent == 'manual':
        manual(environment)
    else:
        # TODO: Train agent if needed
        simulate(agent, environment)
