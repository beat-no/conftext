import os
import sys
import configparser

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


def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def write_config(filepath, config):
    with open(filepath, 'w') as config_file_obj:
        config.write(config_file_obj)
    print("Wrote config to %s" % filepath)


def print_config(config):
    print('[%s]' % '/'.join(config[CONFTEXT_SECTION].values()))


###
# Public API
###

def get_config(**kwargs):
    """
    Get config
    
    kwargs can be used to overwrite settings from config file. If the value of a kwarg is `None`,
    it will be ignored.
    """
    config_file = find_config_file()
    if config_file:
        config = read_config(config_file)[CONFTEXT_SECTION]
        for key, val in kwargs.items():
            if key in config and val is not None:
                config[key] = val
        return config
    else:
        raise FileNotFoundError(
            'No "%s" file in search from "%s" to stop paths: %s, nor in default path: "%s"' % (
                CONFTEXT_FILENAME,
                os.getcwd(),
                stop_paths,
                default_config_path()))
