from databricksbundle.notebook.decorator.DuplicateColumnsChecker import DuplicateColumnsChecker
from databricksbundle.notebook.decorator.containerLoader import containerInitEnvVarDefined
from databricksbundle.notebook.function.ArgumentsResolver import ArgumentsResolver

if containerInitEnvVarDefined():
    from databricksbundle.container.envVarContainerLoader import container as _container  # pylint: disable = import-outside-toplevel
else:
    from databricksbundle.container.pyprojectContainerLoader import container as _container  # pylint: disable = import-outside-toplevel

argumentsResolver: ArgumentsResolver = _container.get(ArgumentsResolver)
duplicateColumnsChecker: DuplicateColumnsChecker = _container.get(DuplicateColumnsChecker)
