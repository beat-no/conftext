import os
import sys
from configparser import ConfigParser
from invoke import task, Program, Collection

CONFTEXT_FILENAME = '.conftext.ini'
CONFTEXT_SECTION = 'conftext'


###
# Library
###

def user_home():
    return os.path.expanduser('~')


def default_config_path():
    return os.path.join(user_home(), '.config', CONFTEXT_FILENAME[1:])


stop_paths = [os.path.sep, os.path.dirname(user_home())]


def find_config_file():
    """
    Find config files
    
    Will first look for `.conftext.ini` in the current working dir and then subsequently upwards the
    users home directory, or if home is not found, upwards to top-level dir `/`.
    
    Then it will look for `~/.config/conftext.ini`
    
    Returns `False` if no files found.
    """
    current_path = os.getcwd()
    
    # Check from current dir upwards `stop_paths` dir for `.conftext.ini`
    while current_path not in stop_paths:
        candidate_path = os.path.join(current_path, CONFTEXT_FILENAME)
        if os.path.isfile(candidate_path):
            return candidate_path
        else:
            current_path = os.path.dirname(current_path)
    
    # Check for default path `~/.config/conftext.ini`
    candidate_path = default_config_path()
    if os.path.isfile(candidate_path):
        return candidate_path
    
    # Finally return false if no conf file found.
    return False


def ask_config_path():
    cwd_config_path = os.path.join(os.getcwd(), CONFTEXT_FILENAME)
    print("No config file was found. Create one with default settings?")
    print("[1] %s" % default_config_path())
    print("[2] %s" % cwd_config_path)
    choice = input("Type 1 or 2 then enter: ")
    
    if choice == '1':
        return default_config_path()
    elif choice == '2':
        return cwd_config_path
    else:
        sys.exit('Invalid choice: %s' % choice)


def write_config(filepath, config):
    with open(filepath, 'w') as config_file_obj:
        config.write(config_file_obj)
    print("Wrote config to %s" % filepath)


def read_config(config_file)->ConfigParser:
    config = ConfigParser()
    config.read(config_file)
    return config


def print_config(config):
    print('[%s]' % '/'.join(config[CONFTEXT_SECTION].values()))


###
# Public API
###

class NoConftext(Exception):
    pass


def get_config(**kwargs)->ConfigParser:
    """
    Get config
    
    kwargs can be used to overwrite settings from config file. If the value of a kwarg is `None`,
    it will be ignored.
    """
    config_file = find_config_file()
    
    if not config_file and not kwargs:
        raise NoConftext('No "%s" file found and no kwargs given.' % CONFTEXT_FILENAME)
    
    if config_file:
        config = read_config(config_file)[CONFTEXT_SECTION]
    else:
        config = dict()
    
    for key, val in kwargs.items():
        if val is not None:
            config[key] = val
    
    return config


@task(default=True)
def show(ctxt):
    """
    Show config context
    """
    config_file = find_config_file()
    if not config_file:
        config_file = ask_config_path()
        config = create_initial_config()
        write_config(config_file, config)
    print_config(read_config(config_file))
###
# Invoke setup
###

namespace = Collection()
namespace.add_task(show)
program = Program(namespace=namespace)
