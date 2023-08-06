# TODO docs

from logging import getLogger
from pathlib import Path

from dfmpy.utils.files import path_is_directory
from dfmpy.utils.files import path_is_file
from dfmpy.utils.files import path_is_symlink
from dfmpy.utils.interactive import ask_to

# TODO docs
LOG = getLogger()


def __delete_empty_directories(file_path, root_names):
    # TODO docs
    # TODO unit test
    root_paths = [Path(r) for r in root_names]
    for parents in file_path.parents:
        if parents in root_paths:
            # Exit this loop to finish quickly since we hit a root.
            break

        if not list(parents.iterdir()):
            # Directory is empty, delete it.
            parents.rmdir()
            LOG.warning('Unlinked empty directory: %s', parents)
        else:
            # Exit early since we hit a non-empty directory.
            LOG.debug('Parent directory not empty, not unlinking: %s', parents)
            break


def unlink_path(path, force, interactive, roots=None):
    # TODO docs
    # TODO unit test
    if not roots:
        roots = ('',)

    if ask_to(f'Unlink path: {path}', force, interactive):
        if path_is_directory(path):
            path.rmdir()
            LOG.warning('Removed directory: %s', path)
        elif path_is_file(path):
            path.unlink()
            LOG.warning('Removed file: %s', path)
        elif path_is_symlink(path):
            path.unlink()
            LOG.warning('Removed symlink: %s', path)
        else:
            path.unlink()
            LOG.error('Removed unknown file type: %s', path)
        __delete_empty_directories(path, roots)

    else:
        LOG.info('Simulated unlink: %s -> %s', str(path), path.resolve())


def remove_broken_files(installed_paths, force, interactive):
    # TODO docs
    # TODO unit test
    LOG.info('Checking for broken files.')
    for installed_path in installed_paths:
        if not installed_path.resolve().exists():
            unlink_path(installed_path, force, interactive)
