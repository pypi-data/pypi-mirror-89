#!/usr/bin/env python3

# Copyright (c) 2016, Cyril Roelandt
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
import argparse
import configparser
import logging
import os
import sys

import pkg_resources


class FeedFixer(object):
    '''The base class of all plugins'''
    @staticmethod
    def _expand_path(path):
        path = os.path.expanduser(path)  # Expands '~'
        path = os.path.expandvars(path)  # Expands environment variables
        return path


def init_logger(debug_mode=False):
    logger = logging.getLogger('sf2cf')
    if debug_mode:
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(levelname)10s | [+] %(message)s')
    else:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('[+] %(message)s')
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
    return logger


def is_valid_conf_file(filename):
    if not os.path.exists(filename):
        raise argparse.ArgumentTypeError('%s does not exist' % filename)

    if not os.access(filename, os.R_OK):
        raise argparse.ArgumentTypeError('%s is not readable.' % filename)

    return filename


def default_config_file():
    config_home = os.environ.get('XDG_CONFIG_HOME',
                                 os.path.expanduser('~/.config'))
    return os.path.join(config_home, 'sf2cf/config')


def create_parser(plugins):
    parser = argparse.ArgumentParser(description='Rewrite Atom/RSS feeds.')
    # NOTE: If we used 'default_config_file()' as a default for '--conf', the
    # typecheck would be applied to it. Should the default config file not
    # exist, the user would get a warning about that, but it would mention the
    # '--conf' option even though they did not use it. Since this is confusing,
    # we do not use a default here, and manually set if it is needed later.
    parser.add_argument('-c', '--conf',
                        type=lambda f: is_valid_conf_file(f),
                        help='configuration file to use')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='turn on debug logging')
    parser.add_argument('-l', '--list', action='store_true',
                        help='list available modules')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 0.1')

    for plugin_name in plugins.keys():
        parser.add_argument('--help-%s' % plugin_name, dest='help_plugin',
                            action='store_const', const=plugin_name,
                            help='Show help for the %s plugin' % plugin_name)
    return parser


def main():
    plugins = {}
    for entrypoint in pkg_resources.iter_entry_points('sf2cf.feed'):
        plugin_cls = entrypoint.load()
        plugins[plugin_cls.name] = plugin_cls

    parser = create_parser(plugins)
    args = parser.parse_args()
    logger = init_logger(args.debug)

    if args.help_plugin:
        plugin_cls = plugins[args.help_plugin]
        try:
            print("* DESCRIPTION")
            print(plugin_cls.description)
            print("\n* SAMPLE CONF")
            print(plugin_cls.sample_conf)
        except AttributeError:
            print("The '%s' plugin does not provide enough documentation")
            sys.exit(1)
        sys.exit(0)

    if args.list:
        for plugin_name, plugin_cls in plugins.items():
            print('%s %s' % (plugin_name, plugin_cls.version))
            print('\t%s' % plugin_cls.description)
        sys.exit(0)

    if not args.conf:
        args.conf = default_config_file()
        try:
            is_valid_conf_file(args.conf)
        except argparse.ArgumentTypeError:
            sys.exit('No configuration file was specified, and the default '
                     f'one {args.conf} does not exist or is not readable')

    config = configparser.ConfigParser()
    config.read(args.conf)

    for section_name, section in config.items():
        if not section_name.startswith('feed:'):
            continue

        try:
            plugin_name = section['plugin']
        except KeyError:
            logger.error('You MUST specify a plugin.')
            continue
        logger.info('Loading %s' % plugin_name)

        try:
            plugin_cls = plugins[plugin_name]
        except KeyError:
            logger.error('Unknown plugin %s' % plugin_name)
            continue

        try:
            plugin = plugin_cls(section)
            plugin.run()
        except:  # noqa
            logger.error(f'Unknown error while running the "{plugin_name}" '
                         'plugin')
    sys.exit(0)


if __name__ == '__main__':
    main()
