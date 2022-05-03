import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from PencilLandingSimulator.log import Log  # noqa: E402
from PencilLandingSimulator import app  # noqa: E402
import sys  # noqa: E402
import colorama  # noqa: E402
import argparse  # noqa: E402


if __name__ == '__main__':
    '''
        This script processes input from user and runs the main application.
    '''
    # Initialise coloured text
    colorama.init(convert=True)

    # Parse input arguments
    parser = argparse.ArgumentParser(prog="PencilLandingSimulator", description="Train an agent to propulsively land.")
    parser.add_argument('-agent', choices=['manual', 'dqn', 'ppo'], help="choose the agent", default='manual')
    parser.add_argument('-env', choices=['ground'], help="choose the environment", default='ground')
    parser.add_argument('-verbose', action='store_true', dest='verbose', help="show extra output", default=False)
    parser.add_argument('-version', action='version', version='%(prog)s@dev')

    # Note: Help and Version command are handled by argparse
    args = parser.parse_args(sys.argv[1:])

    # Handle verboseness
    if args.verbose:
        Log.verboseness = 1

    # Process arguments and run module
    app.main(args)
