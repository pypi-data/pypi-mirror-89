# pylint: skip-file
import ioc

from .secret import get_signer
from .secret import get_secret_key


def setup_ioc(*args, **kwargs):
    ioc.provide('ApplicationSigner', get_signer())
    ioc.provide('ApplicationSecretKey', get_secret_key())
