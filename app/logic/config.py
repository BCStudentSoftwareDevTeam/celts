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

def load_config_files(conf, env):
    # New Funct: 
    # load in default
    # with open(environment_file) as ymlfile:
    # deep_update(override with ymlfile)
    # with open(local_override) as ymlfile:
    # deep_update(override with ymlfile)
    
    import yaml

    with open("app/config/default.yml", 'r') as ymlfile:
        try:
            conf.update(deep_update(conf, yaml.load(ymlfile, Loader=yaml.FullLoader)))
        except TypeError:
            print("There was an error loading the override config file default.yml. It might just be empty.")
    with open("app/config/"+ env + ".yml", 'r') as ymlfile:
        try:
            conf.update(deep_update(conf, yaml.load(ymlfile, Loader=yaml.FullLoader)))
        except TypeError:
            print(f"There was an error loading the override config file {env}.yml. It might just be empty.")
    
    return conf