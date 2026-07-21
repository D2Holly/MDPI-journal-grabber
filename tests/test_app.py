"""
a
"""
import time
import pytest
import requests
from app import app


def fake_param_data():
    """
    Docstring for fake_param_data
    
    :return: Description
    :rtype: Any
    """
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
    return mock_data


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
        def mock_get(*args, **kwargs): # pylint: disable=W0613
            return MockResponse(fake_param_data(), exception_type)

        #mock requests.get into always returning our mock_data and giving a 200 response
        monkeypatch.setattr(requests, 'get', mock_get)
        #mock time.sleep into skipping the pauses for an instant response
        monkeypatch.setattr(time, 'sleep', lambda x: None)

        if exception_type == 200:
            assert app.main() is True
        else:
            assert app.main() == 403


class TestGetResponse:
    """
    a
    """
    @pytest.mark.parametrize(
    "exception_type",
        [
            200,
            500
        ]
    )
    def test_get_response_success_and_fail(self, monkeypatch: pytest.MonkeyPatch, exception_type):
        """
        Docstring for test_response_happy
        
        :param self: Description
        """
        def mock_get(*args, **kwargs): # pylint: disable=W0613
            return MockResponse(fake_param_data(), exception_type)

        #mock requests.get into always returning our mock_data and giving a 200 response
        monkeypatch.setattr(requests, 'get', mock_get)
        monkeypatch.setattr(time, 'sleep', lambda x: None)

        if exception_type == 200:
            assert app.get_response_data(None, None, None) is True
        else:
            assert app.get_response_data(None, None, None) == exception_type



    def test_get_response_empty(self, monkeypatch: pytest.MonkeyPatch):
        """
        Docstring for test_response_happy
        
        :param self: Description
        """
        data = fake_param_data()
        data['message']['items'].clear()

        def mock_get(*args, **kwargs): # pylint: disable=W0613
            return MockResponse(data, 200)

        #mock requests.get into always returning our mock_data and giving a 200 response
        monkeypatch.setattr(requests, 'get', mock_get)
        monkeypatch.setattr(time, 'sleep', lambda x: None)

        assert app.get_response_data(None, None, None) is False


class TestOutput:
    """
    a
    """
    def test_get_response_success_and_fail(self, capsys):
        """
        Docstring for test_response_happy
        
        :param self: Description
        """
        data = fake_param_data()
        app.output_response_data(data)

        captured = capsys.readouterr()
        assert "Title: Test Article" in captured.out
        assert "URL: https://api.crossref.org/test" in captured.out
        assert "Volume: 18" in captured.out
        assert "Issue: 1" in captured.out
