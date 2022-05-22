# Pencil Landing Simulator

This is my first solo attempt at a Reinforcement Leaning project in Python, exploring whether an agent can land a pencil autonomously in different environments. Not at all inspired by SpaceX. It's like the traditional [CartPole Environment](https://github.com/openai/gym/blob/e2266025e6c77641629f1ce8b12b4f73bca91352/gym/envs/classic_control/cartpole.py) but with a requirement to land vertically and slowly.

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
python -m PLSimulator ...
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
