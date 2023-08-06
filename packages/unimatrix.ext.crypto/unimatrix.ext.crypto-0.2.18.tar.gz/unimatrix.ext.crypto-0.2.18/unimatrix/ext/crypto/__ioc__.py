# pylint: skip-file
import ioc

from .secret import get_signer
from .secret import get_secret_key
from .defaultkeystore import DefaultKeystore


def setup_ioc(*args, **kwargs):
    ioc.provide('ApplicationSigner', get_signer())
    ioc.provide('ApplicationSecretKey', get_secret_key())
    if not ioc.is_satisfied('Keystore'):
        ioc.provide('Keystore', DefaultKeystore())
