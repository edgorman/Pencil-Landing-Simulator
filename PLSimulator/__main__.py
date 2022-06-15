import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from PLSimulator.log import Log  # noqa: E402
from PLSimulator import app  # noqa: E402
from PLSimulator import constants  # noqa: E402
import sys  # noqa: E402
import colorama  # noqa: E402
import argparse  # noqa: E402


if __name__ == '__main__':
    '''
        This script processes input from user and runs the main application.
    '''
    # Initialise coloured text
    colorama.init(convert=True)

    # Configure agent and environment choices
    agent_choices = list(app.AGENT_OBJCECTS_DICT.keys())
    env_choices = list(constants.ENV_CONFIG.keys())

    # Parse input arguments
    parser = argparse.ArgumentParser(prog="PLSimulator", description="Train an agent to propulsively land.")
    parser.add_argument('-agent', choices=agent_choices, help="choose the agent", default='manual')
    parser.add_argument('-env', choices=env_choices, help="choose the environment", default='earth')
    parser.add_argument('-verbose', action='store_true', dest='verbose', help="show extra output", default=False)
    parser.add_argument('-version', action='version', version='%(prog)s@dev')

    # Note: Help and Version command are handled by argparse
    args = parser.parse_args(sys.argv[1:])

    # Handle verboseness
    if args.verbose:
        Log.verboseness = 1

    # Process arguments and run module
    app.main(args)
