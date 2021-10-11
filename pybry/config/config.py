import python_json_config
from dynaconf import Dynaconf
import tempfile
import os

from pybry.utils.forgivingjson import loadf, dumpf, ForgivingJson
from pybry.utils.logutil import logger


def save_config(filepath, data):
    from pybry.utils.forgivingjson import dumpf
    dumpf(filepath, data)

def load_config(filepath, **kwargs):
    data = None
    try:
        data = load_config_dynaconf(filepath, **kwargs)
    except Exception as ex:
        logger.warning(f'Could not open config file {filepath} as dynaconf settings')
        
    if not data:
        configdata = ForgivingJson.loadf(filepath)
        # create config parser
        builder = python_json_config.ConfigBuilder()

        config = builder.parse_config(configdata)

        # config.add("config_file", cfgpath)

        data = config.to_dict()
        
    return data

def load_config_dynaconf(filepath, **kwargs):
    configobj = Dynaconf(**kwargs
        # envvar_prefix="MYPROGRAM",
        # settings_files=["settings.toml", ".secrets.toml"],
        # environments=True,
        # load_dotenv=True,
        # env_switcher="MYPROGRAM_ENV",
        # **more_options
    )

    if os.path.isfile(filepath) or os.path.islink(filepath):
        if filepath and str(filepath).endswith(".json"):
            tmpf = tempfile.TemporaryFile(prefix=os.path.basename(__file__), suffix="loader")
            data = loadf(filepath)
            dumpf(tmpf.name, data)
            return configobj.load_file(path=tmpf.name)  # list or `;/,` separated allowed
        else:
            return configobj.load_file(filepath)

    return configobj


# settings = load_config()

