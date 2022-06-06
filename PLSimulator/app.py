import ray
import json
import pygame
from ray.tune.registry import register_env

from PLSimulator.log import Log
from PLSimulator.agents.agent import BaseAgent
from PLSimulator.agents.ppo import PPOAgent
from PLSimulator.environments.environment import BaseEnvironment
from PLSimulator.environments.planet import EarthEnvironment
from PLSimulator.environments.planet import MarsEnvironment
from PLSimulator.environments.planet import MoonEnvironment


AGENT_OBJCECTS_DICT = {
    'manual': BaseAgent,
    'ppo': PPOAgent,
    'dqn': BaseAgent,  # TODO
}

ENVIRONMENT_OBJECTS_DICT = {
    'earth': EarthEnvironment,
    'mars': MarsEnvironment,
    'moon': MoonEnvironment,
}


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
    Log.info("User has started the simulation.")

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
            action[i] = 1 if keys[i] else 0
            environment._pencil.entities[i].isRenderable = keys[i]

        # Update the environment with the action
        state, reward, done, info = environment.step(action)

        # Render environment at N fps
        if fps > 0:
            environment.render()
            environment.clock.tick(fps)
        Log.info(f"State: {state}, Action: {action}, Reward: {reward}, Done: {done}.")
    Log.success("Agent has finished the simulation.")


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
    Log.info("Agent has started the simulation.")

    # Iterate until environment has finished
    while environment.running:
        # Step through environment once
        state = environment.state()

        # Get action of the agent
        action = agent.step(state)

        # Toggle pencil sub entities on/off
        for i in range(len(action)):
            environment._pencil.entities[i].isRenderable = abs(action[i]) > 0

        # Update the environment with the action
        state, reward, done, info = environment.step(action)

        # Render environment at N fps
        if fps > 0:
            environment.render()
            environment.clock.tick(fps)
        Log.info(f"State: {state}, Action: {action}, Reward: {reward}, Done: {done}.")
    Log.success(f"Agent has finished the simulation.")


def train(agent: BaseAgent) -> BaseAgent:
    '''
        Train the agent in the environment given

        Parameters:
            agent: The agent to train in the environment

        Returns:
            None
    '''
    Log.info("Loading Ray...")
    info = ray.init(ignore_reinit_error=True)
    Log.success(f"Loaded dashboard at http://{info['webui_url']}")

    results = []
    episode_data = []
    episode_json = []

    Log.info("Clearing previous training...")
    agent.clear()

    Log.info("Starting training...")
    num_iter = 10
    for n in range(num_iter):
        result = agent.train()
        results.append(result)

        episode = {'n': n, 
               'episode_reward_min': result['episode_reward_min'], 
               'episode_reward_mean': result['episode_reward_mean'], 
               'episode_reward_max': result['episode_reward_max'],  
               'episode_len_mean': result['episode_len_mean']}
    
        episode_data.append(episode)
        episode_json.append(json.dumps(episode))
        agent.save()
    Log.success("Finished training agent.")


def main(args: dict) -> None:
    '''
        Process the arguments and determine the top-level functions to execute

        Parameters:
            args: Dict of arguments input from the user

        Returns:
            None
    '''
    agent = AGENT_OBJCECTS_DICT[args.agent]
    environment = ENVIRONMENT_OBJECTS_DICT[args.env]

    if args.agent == 'manual':
        Log.info("Loading the environment in manual mode.")
        manual(environment())
    else:
        Log.info("Registering RL environment.")
        # register(id=args.env+"-v0", entry_point=ENVIRONMENT_OBJECTS_DICT[args.env])
        register_env(args.env+"-v0", lambda config: environment())
        Log.success("Finished registering RL environment.")

        Log.info("Initialise RL agent.")
        agent = agent(args.env+"-v0")
        Log.success("Finished initialising RL agent.")

        Log.info("Train RL agent.")
        # train(agent, ENVIRONMENT_OBJECTS_DICT[args.env])
        Log.success("Finished training RL agent.")

        Log.info("Loading the environment in agent mode.")
        simulate(agent, environment())

    Log.success("Exiting application.")
