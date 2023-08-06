from databricksbundle.container.entryPointContainerLoader import entryPointExists

if entryPointExists():
    from databricksbundle.container.entryPointContainerLoader import container # pylint: disable = import-outside-toplevel, unused-import
else:
    from databricksbundle.container.pyprojectContainerLoader import container # pylint: disable = import-outside-toplevel, unused-import
