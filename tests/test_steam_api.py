from steam_api import __version__


def test_version():
    assert __version__ == '0.1.0'

    # Test with pytest
    # When writing tests, will need to mock what calling steamn api would return for all functions in bot helper
    # dependency injection research this for testing.   steam_api is a fake thing for the sake of testing
    # for testing this will need to pass in a fake steam_api.
    # steam_api functions should be tested sperarely not part of this
