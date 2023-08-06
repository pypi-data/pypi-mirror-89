# TODO docs

from datetime import datetime
from logging import getLogger
from pathlib import Path
from shutil import copyfile
from shutil import move

from pkg_resources import resource_filename
from xdgenvpy import XDGPedanticPackage

# TODO docs
LOG = getLogger()

# TODO consider renaming this to a "config" command, where it can be initialized
#  or "edit" the configs.

# TODO docs - Using the pedantic object as we want to ensure the full directory
#  paths up to the file exist!
__XDG = XDGPedanticPackage('dfmpy')

# TODO docs
_BACKUP_SUFFIX = datetime.now().strftime('.%Y%m%d_%H%M%S.dfmpy.backup')


def __install_file(resource_name, overwrite=False):
    # TODO docs
    # TODO unit test
    base_resource = resource_filename('dfmpy.resources', resource_name)
    LOG.debug('Found: %s', base_resource)

    installed_file = Path(__XDG.XDG_CONFIG_HOME).joinpath(resource_name)
    if installed_file.exists() and not overwrite:
        LOG.error('Not overwriting: %s', installed_file)

    elif installed_file.exists() and overwrite:
        # TODO create a backup of the existing file!!
        backup_file = str(installed_file) + _BACKUP_SUFFIX
        move(installed_file, backup_file)
        LOG.warning('Backed up: %s', backup_file)
        copyfile(base_resource, installed_file)
        LOG.warning('Overwrote: %s', installed_file)

    else:
        copyfile(base_resource, installed_file)
        LOG.info('Installed: %s', installed_file)


def initialize(force=False, interactive=False):
    # TODO do not overwrite existing files
    # TODO docs
    # TODO unit test
    # TODO implement interactive
    if interactive:
        raise NotImplementedError('Interactive not yet implemented.')
    __install_file('config.ini', overwrite=force)
    __install_file('ignore.globs', overwrite=force)


def initialize_main(cli):
    # TODO docs
    # TODO unit test
    initialize(cli.force, cli.interactive)
