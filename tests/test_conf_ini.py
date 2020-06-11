import pytest
from conftext import conftext
from conftext import get_ini_config
from conftext import conf_ini

CONFTEXT_ONLY_GLOBAL = conftext.read_from_file("""
[conftext]
environment = development
service = fabel
""")

CONFTEXT_WITH_MODULE_SECTION = conftext.read_from_file("""
[conftext]
environment = development
service = fabel

[rytm.clients.dummy]
environment = development
""")

FILEPATH_DEFAULT_SECTION = "tests/config/rytm/dummy/default_section.ini"
FILEPATH_MULTI_SECTION = "tests/config/rytm/dummy/multi_section.ini"


def test_get_ini_config_ok(regtest):
    print(get_ini_config(FILEPATH_DEFAULT_SECTION), file=regtest)


@pytest.mark.xfail(raises=FileNotFoundError)
def test_get_ini_config_nok():
    get_ini_config("./invalid/path.ini")


def test_get_config_section(regtest):
    
    config = conf_ini.read_config(FILEPATH_DEFAULT_SECTION)
    print(conf_ini.get_config_section(
        config, CONFTEXT_WITH_MODULE_SECTION, "rytm.clients.dummy"), file=regtest)
    print(conf_ini.get_config_section(
        config, CONFTEXT_ONLY_GLOBAL, "rytm.clients.dummy"), file=regtest)
    
    config = conf_ini.read_config(FILEPATH_MULTI_SECTION)
    print(conf_ini.get_config_section(
        config, CONFTEXT_WITH_MODULE_SECTION, "rytm.clients.dummy"), file=regtest)
    print(conf_ini.get_config_section(
        config, CONFTEXT_ONLY_GLOBAL, "rytm.clients.dummy"), file=regtest)


def test_get_config(regtest):
    
    print(get_ini_config(
        FILEPATH_MULTI_SECTION,
        CONFTEXT_WITH_MODULE_SECTION,
        module_name="rytm.clients.dummy"
    ), file=regtest)
