from music import Music
from background import Background
from base_pipeline import BasePipeline


def test_music_import():
    assert Music(BasePipeline()) is not None


def test_background_import():
    assert Background(BasePipeline()) is not None
