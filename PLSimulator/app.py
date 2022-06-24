import ray
import pygame
from ray.tune.registry import register_env

from PLSimulator.log import Log
from PLSimulator.agents.agent import BaseAgent
from PLSimulator.agents.ppo import PPOAgent
from PLSimulator.constants import ENV_CONFIG
from PLSimulator.environments.environment import BaseEnvironment


AGENT_OBJCECTS_DICT = {
    'manual': BaseAgent,
    'ppo': PPOAgent,
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
    done, quit = False, False
    environment.reset()
    environment.render()
    Log.info("User has started the simulation.")

    # Store which keys have been pressed down or up
    action = [0, 0, 0]
    keys = [False, False, False]

    # Iterate until environment has finished
    while not done and not quit:
        # Process pygame events
        events = pygame.event.get()
        for event in events:
            # Check for manual exit
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit = True

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

        # Update the environment with the action
        state, reward, done, info = environment.step(action)

        # Render environment at N fps
        if fps > 0:
            environment.render()
            environment.clock.tick(fps)
        Log.info(f"State: {state}, Action: {action}, Reward: {reward}, Done: {done}, Info: {info}.")
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
    done = False
    environment.reset()
    environment.render()
    Log.info("Agent has started the simulation.")

    # Iterate until environment has finished
    while not done:
        # Step through environment once
        state = environment.state()

        # Get action of the agent
        action = agent.step(state)

        # Update the environment with the action
        state, reward, done, info = environment.step(action)

        # Render environment at N fps
        if fps > 0:
            environment.render()
            environment.clock.tick(fps)
        Log.info(f"State: {state}, Action: {action}, Reward: {reward}, Done: {done}, Info: {info}.")
    Log.success("Agent has finished the simulation.")


def train(agent: BaseAgent, episode_length: int = 1) -> BaseAgent:
    '''
        Train the agent in the environment given

        Parameters:
            agent: The agent to train in the environment
            episode_length: Number of episodes to train agent

        Returns:
            None
    '''
    # Set up Ray
    Log.info("Loading Ray...")
    ray.init(ignore_reinit_error=True)

    # Set up agent
    Log.info("Clearing previous training...")
    agent.clear()

    # Set up episode history
    episodes = []
    save_frequency = max(1, round(episode_length / 10))

    # Start agent training
    Log.info(f"Starting training for {episode_length} episodes...")
    for n in range(1, episode_length + 1):
        # Train the agent for this episode
        result = agent.train()

        # Store results
        episode = {
            'min': round(result['episode_reward_min'], 1),
            'mean': round(result['episode_reward_mean'], 1),
            'max': round(result['episode_reward_max'], 1),
        }
        episodes.append(episode)
        Log.info(f"Episode {n} -> {episode}.")

        # Save current model to local folder
        if n % save_frequency == 0 or n == 1:
            agent.save()
            Log.info(f"Saving episode {n}.")

    # Save last model if not saved already
    if episode_length % 10 != 0:
        agent.save()
        Log.info(f"Saving episode {n}.")

    # Generate analysis graphs
    Log.info("Generating graphs for training.")
    agent.graph(episodes)

    # Shutting down Ray
    Log.info("Closing Ray...")
    ray.shutdown()


def main(args: dict) -> None:
    '''
        Process the arguments and determine the top-level functions to execute

        Parameters:
            args: Dict of arguments input from the user

        Returns:
            None
    '''
    agent = AGENT_OBJCECTS_DICT[args.agent]
    environment = BaseEnvironment
    env_config = ENV_CONFIG[args.env]

    if args.agent == 'manual':
        Log.info("Rendering the environment in manual mode.")
        manual(environment(env_config))
    else:
        Log.info("Registering RL environment.")
        register_env(env_config["name"], lambda config: environment(config))
        Log.success("Finished registering RL environment.")

        Log.info("Initialise RL agent.")
        agent = agent(env_config)
        Log.success("Finished initialising RL agent.")

        if args.load == "":
            Log.info("Train RL agent.")
            train(agent, episode_length=31)
            Log.success("Finished training RL agent.")
        else:
            Log.info("Load RL agent.")
            try:
                agent.load(args.load)
            except Exception as e:
                Log.error(str(e))
            Log.success("Finished loading RL agent.")

        Log.info("Rendering the environment in agent mode.")
        simulate(agent, environment(env_config))

    Log.info("Exiting application.")
