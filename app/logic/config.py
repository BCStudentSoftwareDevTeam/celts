import yaml

import collections.abc as collections

def deep_update(d, u):
    """
    Update old_dict in place with the values from new_dict, respecting nested dictionaries.
    Adapted from this stackoverflow answer: https://stackoverflow.com/a/32357112
    """
    if d is None: d = {}
    if not u: return d

    for key, val in u.items():
        if isinstance(d, collections.Mapping):
            if isinstance(val, collections.Mapping):
                r = deep_update(d.get(key, {}), val)
                d[key] = r
            else:
                d[key] = u[key]
        else:
            d = {key: u[key]}
    return d

def load_config_files(app):
    # we want to switch between three config files
    update_config_from_yaml(app, "default.yml")
    update_config_from_yaml(app, f"{app.env}.yml")
    update_config_from_yaml(app, "local-override.yml")
 
def update_config_from_yaml(app, configFile):
    """
    Update the application config with a yml file based on the Flask environment.
    """
    with open(f"app/config/{configFile}", 'r') as ymlfile:
        try:
            app.config.update(deep_update(app.config, yaml.load(ymlfile, Loader=yaml.FullLoader)))
        except TypeError:
            print(F"There was an error loading the override config file {configFile}.")
