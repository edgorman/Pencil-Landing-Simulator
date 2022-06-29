# Pencil Landing Simulator

This is my first solo attempt at a Reinforcement Leaning project in Python, exploring whether an agent can land a pencil autonomously in different environments. Not at all inspired by SpaceX. It's like the traditional [CartPole Environment](https://github.com/openai/gym/blob/e2266025e6c77641629f1ce8b12b4f73bca91352/gym/envs/classic_control/cartpole.py) but with a requirement to land vertically and slowly.

[![Lint and Test Application](https://github.com/edgorman/Pencil-Landing-Simulator/actions/workflows/test-and-lint.yml/badge.svg)](https://github.com/edgorman/Pencil-Landing-Simulator/actions/workflows/test-and-lint.yml)

<img src="docs/gifs/success.gif" width="250px" alt="Example of pencil landing successfully.">

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
