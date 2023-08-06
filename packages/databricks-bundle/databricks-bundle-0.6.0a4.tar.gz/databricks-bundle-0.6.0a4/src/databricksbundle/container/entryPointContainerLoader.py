import os
import sys
from injecta.container.ContainerInterface import ContainerInterface
from injecta.dtype.classLoader import loadClass

if sys.version_info >= (3, 8):
    from importlib import metadata as importlib_metadata # pylint: disable = no-name-in-module
else:
    import importlib_metadata

def _getContainerInit():
    entryPoints = importlib_metadata.entry_points().get('bricksflow', ())

    for entryPoint in entryPoints:
        if entryPoint.name == "container-init":
            return entryPoint.value

    raise Exception('bricksflow\'s container-init entry_point not defined')

def entryPointExists():
    return 'bricksflow' in importlib_metadata.entry_points()

def initAppContainer(appEnv: str) -> ContainerInterface:
    containerInitConfig = _getContainerInit().split(':')

    initContainerFunction = loadClass(containerInitConfig[0], containerInitConfig[1])

    return initContainerFunction(appEnv)

container = initAppContainer(os.environ['APP_ENV'])
