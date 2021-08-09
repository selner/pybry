from dynaconf import Dynaconf, settings
import tempfile
import os

from pybry.utils.forgivingjson import loadf, dumpf

def save_config(filepath, data):
    from pybry.utils.forgivingjson import dumpf
    dumpf(filepath, data)

def load_config(filepath, **kwargs):
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

