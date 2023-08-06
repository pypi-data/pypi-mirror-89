import os
from pathlib import Path
import tomlkit
from injecta.container.ContainerInterface import ContainerInterface
from injecta.dtype.classLoader import loadClass

def _loadAppConfig(pyprojectPath: Path) -> list:
    with pyprojectPath.open('r') as t:
        config = tomlkit.parse(t.read())

        if (
            'tool' not in config
            or 'poetry' not in config['tool']
            or 'plugins' not in config['tool']['poetry']
            or 'bricksflow' not in config['tool']['poetry']['plugins']
        ):
            raise Exception('[tool.poetry.plugins.bricksflow] section is missing in pyproject.toml')

        return config['tool']['poetry']['plugins']['bricksflow']

def initAppContainer(appEnv: str) -> ContainerInterface:
    workingDir = Path(os.getcwd())

    appConfig = _loadAppConfig(workingDir.joinpath('pyproject.toml'))
    containerInitConfig = appConfig['container-init'].split(':')

    initContainerFunction = loadClass(containerInitConfig[0], containerInitConfig[1])

    return initContainerFunction(appEnv)

container = initAppContainer(os.environ['APP_ENV'])
