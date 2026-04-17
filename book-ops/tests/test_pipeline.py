"""Unit tests for pipeline.py orchestration logic."""

import pytest
from pipeline import run_pipeline_dry


class TestRunPipelineDry:
    """Tests for run_pipeline_dry function."""

    def test_run_pipeline_dry(self):
        result = run_pipeline_dry()
        assert isinstance(result, list)
        assert len(result) == 3
        assert "Python" in result[0].title
