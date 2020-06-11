import pytest
import conftext


def test_get_conftext_schemas():
    print(conftext.conftext.get_schemas())


def test_get_config():
    test_conf = dict(service='fabel', context='devdb')
    assert conftext.get_config(**test_conf) == test_conf
    
    with pytest.raises(conftext.NoConftext):
        conftext.get_config()