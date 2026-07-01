"""
a
"""
import time
import pytest
import requests
from app import app

class TestApp:
    """
    Docstring for TestApp
    """
    @pytest.mark.parametrize(
    "arguments",
        [
            1,
            0,
            "Banana"
        ]
    )
    def test_ci_pipeline(self, arguments):
        """
        Docstring for test_try
        
        :param self: Description
        """
        if arguments == 1:
            assert app.sample_tests(arguments) is True
        elif arguments == 0:
            assert app.sample_tests(arguments) is False
        else:
            assert app.sample_tests(arguments) is False


#helper class for TestMain
class MockResponse:
    """
    Helper class for TestMain which patches the response data of requests.get and
    response.json
    """
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        """
        forces json to always return the given reponse code when MockResponse was called
        (MockResponse(data, 200) will always return 200)
        """
        return self.json_data


class TestMain:
    """
    Assigned tests for testing main in app/app.py
    """
    @pytest.mark.parametrize(
    "exception_type",
        [
            200,
            403
        ]
    )
    def test_main(self, monkeypatch: pytest.MonkeyPatch, exception_type):
        """
        Docstring for test_main_happy
        
        :param self: Description
        """
        #fake response data in the format that we would expect requests.get(url, params=params,
        # headers=headers, timeout=30) to return
        mock_data = {
            "message": {
                "items": [
                    {
                        "title": ["Test Article"],
                        "volume": "18",
                        "issue": "1",
                        "resource": {
                            "primary": {
                                "URL": "https://api.crossref.org/test"
                            }
                        }
                    }
                ]
            }
        }
        def mock_get(*args, **kwargs): # pylint: disable=W0613
            return MockResponse(mock_data, exception_type)

        #mock requests.get into always returning our mock_data and giving a 200 response
        monkeypatch.setattr(requests, 'get', mock_get)
        #mock time.sleep into skipping the pauses for an instant response
        monkeypatch.setattr(time, 'sleep', lambda x: None)

        if exception_type == 200:
            assert app.main() is True
        else:
            assert app.main() is None
