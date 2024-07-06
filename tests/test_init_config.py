import os
from pytest import mark
from syndot import init_config
from tests.conftest import TEST_DATA_PATH, reset_environment


@mark.config
class TestInitConfig:

    @mark.genuine
    def test_function(self, monkeypatch):
        reset_environment()

        def mock_config_path():
            return os.path.join(TEST_DATA_PATH, '.config', 'syndot')

        def mock_log_path():
            return os.path.join(
                TEST_DATA_PATH, '.local', 'share', 'syndot', 'log_file.log')

        config_path = mock_config_path()
        log_file_path = mock_log_path()

        monkeypatch.setattr(init_config, 'CONFIG_DIR_PATH', config_path)
        monkeypatch.setattr(init_config, 'LOG_FILE_PATH', log_file_path)

        assert not os.path.exists(config_path)

        init_config.init_config()

        assert os.path.exists(config_path)
        assert os.path.isdir(config_path)
        for asset in ['templates', 'colorschemes']:
            asset_path = os.path.join(config_path, asset)
            assert os.path.exists(asset_path)
            assert os.path.isdir(asset_path)
            assert os.listdir(asset_path)
        assert os.path.exists(log_file_path)
        assert os.path.isfile(log_file_path)

        reset_environment()
