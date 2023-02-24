from .component import Component, MetaComponent, abstract
from .component import implements, implementations, interfacedoc
from .api import IProvider
from .exceptions import Error, PIDError, ApiError
from .tools.parameters import HasParam

import re
from requests import get
import os

_providers = {}


class MetaProvider(MetaComponent):
    """Metaclass of the Provider class, used mainly for ensuring
    that provider id's are wellformed and unique"""

    valid_id = re.compile("^[a-z][_a-z0-9]*$")

    def __new__(cls, name, bases, d):
        new_class = super(MetaProvider, cls).__new__(cls, name, bases, d)
        if new_class in implementations(IProvider):
            id = str(new_class.id())
            if id in _providers:
                # Doctest test can duplicate a provider
                # This can be identify by the conditon "module == '__main__'"
                new_path = os.path.realpath(inspect.getfile(new_class))
                id_path = os.path.realpath(inspect.getfile(_provider[id]))
                if new_class.__module__ == '__main__':
                    new_class = _provider[id]
                elif _provider[id].__module__ == '__main__':
                    pass
                elif new_path == id_path:
                    new_class = _provider[id]
                else:
                    raise ApiError("%s at %s and %s at %s have the same id: '%s'"
                                   % (new_class.__name__, new_path,
                                      _provider[id].__name__, id_path,
                                      id))
            if not MetaProvider.valid_id.match(id):
                raise ApiError("%s has a malformed id: '%s'"
                               % (new_class.__name__, id))

            _providers[id] = new_class

        return new_class


class Provider(Component, metaclass=MetaProvider):

    """Base component class of all providers"""

    abstract()
    implements(IProvider)

    def __init__(self):
        super(Provider, self).__init__()

    @interfacedoc
    @classmethod
    def description(self):
        try:
            descr = self.__doc__.lstrip().split('\n')[0]
        except AttributeError:
            return '*** NO DESCRIPTION FOR THIS PROVIDER ***'

        return descr

def providers(interface=IProvider, recurse=True):
    """Returns the providers implementing a given interface and, if recurse,
    any of the descendants of this interface."""
    return implementations(interface, recurse)

def get_provider(provider_id):
    """Return a provider by its pid"""
    if not provider_id in _providers:
        raise PIDError("No provider registered with id: '%s'"
                       % provider_id)
    return _providers[provider_id]

def list_providers(interface=IProvider):
    lst = interface.__name__ + "\n"
    lst += '=' * len(interface.__name__) + "\n"
    provs = providers(interface, False)
    for p in provs:
        lst += f"  * {p.id()} :" + "\n"
        lst += f"    \t\t{p.name()}" + "\n"
    return lst


def list_providers_rst(interface=IProvider):
    lst = '\n' + interface.__name__  + '\n'
    lst += '=' * len(interface.__name__) + '\n'
    provs = providers(interface, False)
    for p in provs:
        lst += f"  * **{p.id()}** : {p.name()}" + '\n'
    return lst