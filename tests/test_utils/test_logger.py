from hypothesis import given, settings, HealthCheck
from hypothesis.strategies import text, characters
import os
from pytest import mark
from syndot.utils import logger
from tests.conftest import TEST_DATA_PATH


@mark.config
class TestInitConfig:

    @mark.genuine
    @given(message=text(
        min_size=5,
        max_size=10,
        alphabet=characters(min_codepoint=97, max_codepoint=122)))
    @settings(max_examples=100,
              deadline=None,
              suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_function(self, message, monkeypatch, caplog):

        def mock_log_path():
            return os.path.join(
                TEST_DATA_PATH, '.config', 'syndot', 'log_file.log')

        log_file_path = mock_log_path()
        monkeypatch.setattr(logger, 'LOG_FILE_PATH', log_file_path)

        logger.log_error(error_message=message)
        log = caplog.text.strip()

        assert isinstance(log, str)
        assert log
        assert log.endswith(message)
