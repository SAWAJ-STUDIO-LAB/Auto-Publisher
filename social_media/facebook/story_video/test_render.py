from frames import Frames
from composer import Composer
from base_pipeline import BasePipeline


def test_frames_import():
    assert Frames() is not None


def test_composer_import():
    assert Composer(BasePipeline()) is not None
