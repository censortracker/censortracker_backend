import os
from pathlib import Path, PurePath

from decouple import AutoConfig

BASE_DIR = Path(__file__).parent.parent.parent.parent

# Loading `.env` files
# See docs: https://gitlab.com/mkleehammer/autoconfig
config = AutoConfig(search_path=BASE_DIR.joinpath("config"))


def err(msg, fatal=True):
    """
    Error "thrower" with "ignore" support
    Useful cases where error can be either ignored or not in the same place
    (depending on external condition)
    """
    if fatal:
        raise Exception(msg)


def keepcast(what=None):
    """
    Callable "caster" to keep current var. type
    (to be used as default cast method)
    """
    return what


def env(var, fatal=True, default=None, cast=keepcast):
    """
    "Syntactic sugared" wrapper around os.getenv.
    Supports err().
    """
    val = os.getenv(var)
    if default is not None:
        fatal = False
    if not val:
        err('"%s" is not defined' % (var), fatal)
        val = default
    return cast(val)


def secret(secret_name, fatal=True, default=None, cast=keepcast, stack_name=None):
    """
    Docker Secrets loader
    """
    val = None
    if default is not None:
        fatal = False
        val = default
    if stack_name is None:
        stack_name = env("PROJECT")
    secret_path = PurePath("/run/secrets/%s.%s.secret" % (stack_name, secret_name))
    if os.path.isfile(secret_path):
        with open(secret_path, "r") as secfile:
            val = secfile.read().replace("\n", "")
    else:
        err('Secret "%s" ("%s") is missing' % (secret_name, secret_path), fatal)
    return cast(val)
