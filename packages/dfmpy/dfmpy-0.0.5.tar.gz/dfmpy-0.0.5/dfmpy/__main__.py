#!/usr/bin/env python3

# TODO docs

# pylint: disable=wrong-import-position

from platform import python_version
from platform import python_version_tuple

# TODO unit test
__PYTHON_MAJOR_VERSION = int(python_version_tuple()[0])
if __PYTHON_MAJOR_VERSION < 3:
    raise SystemError('dfmpy requires Python 3.6+, not ' + python_version())

# TODO unit test
__PYTHON_MIN_VERSION = int(python_version_tuple()[1])
if __PYTHON_MIN_VERSION < 6:
    raise SystemError('dfmpy requires Python 3.6+, not ' + python_version())

import logging
from argparse import ArgumentParser
from logging import StreamHandler
from logging import getLogger
from sys import stdout

import pkg_resources

from dfmpy.commands.add import add_main
from dfmpy.commands.initialize import initialize_main
from dfmpy.commands.ls import ls_main
from dfmpy.commands.uninstall import uninstall_main
from dfmpy.commands.sync import sync_main
from dfmpy.utils.interactive import check_for_interactivity
from dfmpy.utils.logging import get_formatter

# TODO docs
LOG = getLogger()

# TODO docs
__LOG_LEVELS = tuple([
    logging.CRITICAL,
    logging.ERROR,
    logging.WARNING,
    logging.INFO,
    logging.DEBUG,
])


def get_version_str():
    # TODO docs
    # TODO unit test
    return '%(prog)s ' + pkg_resources.require('dfmpy')[0].version


def __setup_logger(verbosity_index=None):
    # TODO docs
    # TODO unit test
    if not verbosity_index:
        verbosity_index = 1
    verbosity_index = max(0, min(len(__LOG_LEVELS) - 1, verbosity_index))
    log_level = __LOG_LEVELS[verbosity_index]
    # formatter = Formatter('%(asctime)s %(levelname)s %(message)s')
    formatter = get_formatter('%(levelname)s %(message)s')
    handler = StreamHandler(stdout)
    handler.setFormatter(formatter)
    logger = getLogger()
    logger.setLevel(log_level)
    logger.addHandler(handler)


def __parse_arguments():
    # TODO docs
    # TODO unit test
    # TODO go through all "help" docs and make sure they are consistent.

    verbose_args = tuple(['-v', '--verbose'])
    verbose_kwargs = {
        'action': 'count',
        'default': 1,
        'dest': 'verbosity',
        'help': 'Set verbosity level, multiple flags increase the level.',
    }
    force_args = tuple(['-f', '--force'])
    force_kwargs = {
        'action': 'store_true',
        'default': False,
        'dest': 'force',
    }
    interactive_args = tuple(['-i', '--interactive'])
    interactive_kwargs = {
        'action': 'store_true',
        'default': False,
        'dest': 'interactive',
    }

    parser = ArgumentParser(prog='dfmpy')
    main_verbose_kwargs = verbose_kwargs.copy()
    del main_verbose_kwargs['dest']
    parser.add_argument(*verbose_args,
                        **main_verbose_kwargs,
                        dest='main_verbosity')
    parser.add_argument('-V',
                        '--version',
                        action='version',
                        version=get_version_str())
    subparsers = parser.add_subparsers(help='sub-command help')

    add_parser = subparsers.add_parser('add', help='add file help')
    add_parser.set_defaults(func=add_main)
    add_parser.add_argument(*verbose_args, **verbose_kwargs)
    add_parser.add_argument(*force_args,
                            **force_kwargs,
                            help='Force overwriting of files.')
    add_parser.add_argument(*interactive_args,
                            **interactive_kwargs,
                            help='Interactively add files to the dotfiles repo,'
                                 ' and then sync it.')
    add_parser.add_argument('-F',
                            '--files',
                            dest='files',
                            help='Add one or more files to the dotfiles repo, '
                                 'then sync it.',
                            nargs='+')

    init_parser = subparsers.add_parser('init', help='initialize help')
    init_parser.set_defaults(func=initialize_main)
    init_parser.add_argument(*verbose_args, **verbose_kwargs)
    init_parser.add_argument(*force_args,
                             **force_kwargs,
                             help='Force overwriting of files.')
    init_parser.add_argument(*interactive_args,
                             **interactive_kwargs,
                             help='Interactively overwrite files if there are'
                                  ' conflicts.')

    ls_parser = subparsers.add_parser('list', help='list help')
    ls_parser.set_defaults(func=ls_main)
    ls_parser.add_argument(*verbose_args, **verbose_kwargs)

    sync_parser = subparsers.add_parser('sync', help='sync help')
    sync_parser.set_defaults(func=sync_main)
    sync_parser.add_argument(*verbose_args, **verbose_kwargs)
    sync_parser.add_argument(*force_args,
                             **force_kwargs,
                             help='Overwrite files if there are conflicts.')
    sync_parser.add_argument(*interactive_args,
                             **interactive_kwargs,
                             help='Interactively overwrite files if there are'
                                  ' conflicts.')

    uninstall_parser = subparsers.add_parser('uninstall', help='uninstall help')
    uninstall_parser.set_defaults(func=uninstall_main)
    uninstall_parser.add_argument(*verbose_args, **verbose_kwargs)
    uninstall_parser.add_argument(*force_args,
                                  **force_kwargs,
                                  help='Force removal of all files.')
    uninstall_parser.add_argument(*interactive_args,
                                  **interactive_kwargs,
                                  help='Interactively remove of files.')

    args = parser.parse_args()
    if not hasattr(args, 'func'):
        parser.print_help()
        parser.exit()

    # Since a argument cannot exist on both the main parser as well as a
    # sub-parser we need to normalize here.  They technically can both exist,
    # but the sub-parser overwrites any value calculated from parsing the main
    # arguments.
    if 'main_verbosity' in args:
        args.verbosity += args.main_verbosity - 1

    return args


def main():
    # TODO docs
    # TODO unit test?
    args = __parse_arguments()
    __setup_logger(args.verbosity)
    try:
        LOG.debug('Arguments: %s', args)

        if 'interactive' in args \
                and args.interactive \
                and not check_for_interactivity():
            raise RuntimeError(
                'Cannot run interactively while not attached to a TTY.')

        args.func(args)

    except KeyboardInterrupt:
        print('')
        LOG.warning('Leaving dfmpy prematurely.')

    # except Exception as e:
    #     LOG.critical(e)
    #     LOG.exception(e)

    except BaseException as exception:  # pylint: disable=broad-except
        # LOG.critical(exception)
        LOG.exception(exception)


if __name__ == '__main__':
    main()
