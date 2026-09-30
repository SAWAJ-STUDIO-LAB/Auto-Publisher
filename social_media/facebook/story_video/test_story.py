from story_pipeline import StoryPipeline


def test_pipeline_import():
    p = StoryPipeline()
    assert p is not None


def test_sanitize():
    p = StoryPipeline()
    assert p.sanitize("  hello\nworld  ") == "hello world"
