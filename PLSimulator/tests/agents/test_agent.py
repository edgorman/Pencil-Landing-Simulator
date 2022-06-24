import os
import mock
import tempfile

from PLSimulator.agents.agent import BaseAgent


def test_init():
    with tempfile.TemporaryDirectory() as tmp_dir:
        with mock.patch('PLSimulator.agents.agent.MODEL_DATA_DIRECTORY', tmp_dir):
            x = BaseAgent("a", "b")
        
        assert x._model_dir == os.path.join(tmp_dir, "a", "b")
        assert "a" in os.listdir(tmp_dir)
        assert "b" in os.listdir(os.path.join(tmp_dir, "a"))


def test_clear():
    with tempfile.TemporaryDirectory() as tmp_dir:
        with mock.patch('PLSimulator.agents.agent.MODEL_DATA_DIRECTORY', tmp_dir):
            x = BaseAgent("a", "b")
        
        open(os.path.join(x._model_dir, "f"), "w")
        assert "f" in os.listdir(x._model_dir)
        x.clear()
        assert "f" not in os.listdir(x._model_dir)


def test_graph():
    with tempfile.TemporaryDirectory() as tmp_dir:
        with mock.patch('PLSimulator.agents.agent.MODEL_DATA_DIRECTORY', tmp_dir):
            x = BaseAgent("a", "b")
        
        episode_data = [
            {'min': 0, 'mean': 1, 'max': 2},
            {'min': 0, 'mean': 1, 'max': 2},
            {'min': 0, 'mean': 1, 'max': 2},
            {'min': 0, 'mean': 1, 'max': 2},
            {'min': 0, 'mean': 1, 'max': 2}
        ]
        x.graph(episode_data)
        assert "rewards_per_episode.png" in os.listdir(x._model_dir)
