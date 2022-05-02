# Pencil Landing Simulator

TODO

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
conda activate URLAnalayser
```

## Usage
Make sure you have conda environment installed before running the Pencil Landing Simulator:

```
python -m PencilLandingSimulator ...
```

Run the testing scripts in the base directory:
```
python -m autopep8 . --in-place --aggressive --recursive --max-line-length 120
python -m flake8 . --max-line-length=120
python -m pytest URLAnalyser/tests/ --disable-pytest-warnings --cov=URLAnalyser -vs
```

To update the environment file, run:
```
conda env export > environment.yml
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
