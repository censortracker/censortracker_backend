import os
from pathlib import Path, PurePath

BASE_DIR = Path(__file__).parent.parent.parent.parent.resolve()


def err(msg, fatal=True):
    """
    Error "thrower" with "ignore" support
    Useful cases where error can be either ignored or not in the same place
    (depending on external condition)
    """
    if fatal:
        raise Exception(msg)


def is_file(file_path):
    return Path(file_path).is_file()


localdev_env_path = BASE_DIR
server_env_path = BASE_DIR.parent.parent
if is_file("%s/.env" % (server_env_path)):
    env_path = server_env_path
elif is_file("%s/.env" % (localdev_env_path)):
    env_path = localdev_env_path
else:
    err(
        "Can't distinguish whether we deploying on dev's machine or server. " +
        "Please, create .env file either in %s or %s" %
        (env_path, env_path.parent.parent),
        True
    )


def keepcast(what=None):
    """
    Callable "caster" to keep current var. type
    (to be used as default cast method)
    """
    return what


def strtobool(value):
    TRUE_VALUES = {"y", "yes", "t", "true", "on", "1"}
    FALSE_VALUES = {"n", "no", "f", "false", "off", "0", ""}
    if isinstance(value, bool):
        return value
    value = value.lower()

    if value in TRUE_VALUES:
        return True
    elif value in FALSE_VALUES:
        return False

    raise ValueError("Invalid truth value: " + value)


def boolcast(value):
    return bool(strtobool(str(value)))


def _load_file(file_name, fatal=True):
    """
    Loader for .env files
    """
    file_path = PurePath("%s/%s" % (env_path, file_name))
    data = {}
    if is_file(file_path):
        with open(file_path, "r", encoding='UTF-8') as envfile:
            for line in envfile:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                k, v = line.split('=', 1)
                k = k.strip()
                v = v.strip()
                if len(v) >= 2 and ((v[0] == "'" and v[-1] == "'")
                                    or (v[0] == '"' and v[-1] == '"')):
                    v = v[1:-1]
                data[k] = v
    else:
        err("No such file: %s" % (file_path), (file_name == ".env"))

    return data


def env(var, fatal=True, default=None, cast=keepcast):
    """
    "Syntactic sugared" wrapper around os.getenv and .env files.
    Supports err().
    """
    val = os.getenv(var)

    if not val:
        cfg = _load_file(".env.ci")
        cfg.update(_load_file(".env"))
        val = cfg[var] if var in cfg else None
    if not val:
        if default is not None:
            fatal = False
        err('"%s" is neither defined in system environment, ' +
            'neither can be found in .env/.env.ci files' % (var), fatal)
        val = default
    if cast is bool:
        cast = boolcast
    return cast(val)
