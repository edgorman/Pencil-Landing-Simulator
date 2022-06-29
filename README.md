# Pencil Landing Simulator

This is my first attempt at designing a reinforcement learning environment where an agent must land itself on a landing pad using a rocket engine and rcs thrusters. Not at all inspired by SpaceX. The agent observes the environment through 5 variables that represent position, velocity and angle relative to the landing pad, and its actions include being able to fire the engine or rcs thruster independently.

[![Lint and Test Application](https://github.com/edgorman/Pencil-Landing-Simulator/actions/workflows/test-and-lint.yml/badge.svg)](https://github.com/edgorman/Pencil-Landing-Simulator/actions/workflows/test-and-lint.yml)

<img src="docs/gifs/success.gif" width="300" alt="Example of pencil landing successfully.">

## Installation
Use the following command to clone the respository:
```
cd your/repo/directory
git clone https://github.com/edgorman/Pencil-Landing-Simulator
```

Install [Anaconda](https://www.anaconda.com/) and create a python environment using this command:
```
conda env create --file environment.yml
```

And then activate it using conda
```
conda activate PLSimulator
```

## Usage
Make sure you have conda environment installed before running the Pencil Landing Simulator:

```
python -m PLSimulator [-h] [-env {earth,moon,mars}] [-agent {manual,ppo}] [-load LOAD] [-save_video] [-verbose] [-version]
```

Without any optional arguments, the program will run in manual mode for the Earth environment. The following are some example commands and what they perform.

Run the program with a manual agent in the moon environment:
```
python -m PLSimulator -env moon -agent manual
```

Run the program with a ppo agent in the mars environment while saving the last run as output:
```
python -m PLSimulator -env mars -agent ppo -save_video
```

Run the program with the last checkpoint from a previously trained agent:
```
python -m PLSimulator -env earth -agent ppo -load last
```

Run the testing scripts in the base directory:
```
python -m autopep8 . --in-place --aggressive --recursive --max-line-length 120
python -m flake8 . --max-line-length=120
python -m pytest PLSimulator/tests/ --disable-pytest-warnings --cov=PLSimulator -vs
```

To update the environment file, run:
```
conda env export > environment.yml
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
