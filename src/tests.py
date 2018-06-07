import pytest

from .main import TwitterService as Twitter


@pytest.fixture
def vcr_config():
    return {
        'filter_headers': [('authorization', 'CONTENT_FILTERED')],
    }


@pytest.mark.vcr()
def test_admin_init():
    assert Twitter().get_admin()


@pytest.mark.vcr()
def test_user_content_generation():
    assert Twitter().get_admin().generate()


@pytest.mark.vcr()
def test_user_content_generation_is_list():
    assert type(Twitter().get_admin().generate())


@pytest.mark.vcr()
def test_user_content_generation_is_list_of_strings():
    assert type(Twitter().get_admin().generate()[0]) == str
