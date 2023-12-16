from pathlib import Path
import test_gha

def pytest_report_header(config):
    """Add information on the package version used in the tests.
    """
    modpath = Path(test_gha.__file__).resolve().parent
    return [ "test_gha: %s" % (test_gha.__version__),
             "          %s" % (modpath)]
