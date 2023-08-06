# TODO docs

from logging import getLogger

from dfmpy.utils.config import get_config
from dfmpy.utils.files.finder import get_expected_paths
from dfmpy.utils.files.finder import get_installed_paths

# TODO docs
LOG = getLogger()


def __unique_key_for_value(items, find_value):
    # TODO docs
    # TODO unit test
    keys = tuple([key for key, value in items if value == find_value])
    if not keys:
        return None
    if len(keys) != 1:
        raise LookupError(f'Multiple keys for value: {find_value} => {keys}')
    return keys[0]


def __get_broken_paths(expected_paths, installed_paths):    # pylint: disable=unused-argument
    # TODO docs - The installed file points to a non-existent file.
    # TODO unit test
    LOG.debug('Finding installed files that point to non-existent files.')
    for installed_path in installed_paths:
        if not installed_path.resolve().exists():
            yield installed_path, installed_path.resolve()


def __get_stale_paths(expected_paths, installed_paths):
    # TODO docs - The installed file resolves to the wrong repo file.
    # TODO unit test
    LOG.debug('Finding installed files that resolve to the wrong file.')
    for installed_path in installed_paths:
        expected = __unique_key_for_value(expected_paths.items(),
                                          installed_path.resolve())
        if installed_path != expected:
            yield installed_path, expected


def __get_not_installed_paths(expected_paths, installed_paths):
    # TODO docs - The expected file is not pointed to by an installed file.
    # TODO unit test
    LOG.debug('Finding expected files that are not installed.')
    installed_files_keys = installed_paths.keys()
    for expected_path in expected_paths.keys():
        if expected_path not in installed_files_keys:
            yield expected_path, expected_paths[expected_path]


def __get_proper_paths(expected_paths, installed_paths):
    # TODO docs - The expected file is properly installed.
    # TODO unit test
    # TODO this needs testing once "sync" is implemented!
    LOG.debug('Finding installed properly installed files.')
    installed_files_keys = installed_paths.keys()
    for expected_path in expected_paths:
        if expected_path in installed_files_keys:
            installed = installed_paths[expected_path]
            if expected_path.resolve() == installed.resolve():
                yield expected_path, expected_paths[expected_path]


def __print(logger, files, message, comparator_symbol):
    # TODO docs
    # TODO unit test
    if files:
        for idx, (left, right) in enumerate(files):
            if idx == 0:
                # Since "files" could be a generator, only log the message if we
                # can actually iterate over the items.  Thus only print for the
                # first element.
                logger(message)
            logger('%s %s %s', left, comparator_symbol, right)


def ls():   # pylint: disable=invalid-name
    # TODO docs
    # TODO unit test
    # TODO add a "--tree" option to the this command

    install_dir = get_config().install_dir
    repository_dir = get_config().repository_dir

    expected_paths = get_expected_paths(install_dir, repository_dir)
    installed_paths = get_installed_paths(install_dir, repository_dir)

    broken = __get_broken_paths(expected_paths, installed_paths)
    __print(LOG.critical, broken, 'Found broken files:', '?=')

    stale = __get_stale_paths(expected_paths, installed_paths)
    __print(LOG.error, stale, 'Found stale files:', '~=')

    not_installed = __get_not_installed_paths(expected_paths, installed_paths)
    __print(LOG.warning, not_installed, 'Found files not installed:', '!=')

    proper = __get_proper_paths(expected_paths, installed_paths)
    __print(LOG.info, proper, 'Found installed files:', '==')


def ls_main(cli):   # pylint: disable=unused-argument
    # TODO docs
    # TODO unit test
    ls()
