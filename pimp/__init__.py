#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import tempfile
import shutil
import subprocess
import sys

from tempdir import TempDir
import shutilwhich

parser = argparse.ArgumentParser()
parser.add_argument('--pip', default=None)
parser.add_argument('--python', default=sys.executable)
parser.add_argument('-q', '--quiet', action='store_true')
subparsers = parser.add_subparsers(dest='action')
install_parser = subparsers.add_parser('install')
install_parser.add_argument('packages', nargs='+')
install_parser.add_argument('-y', '--assumeyes', action='store_true')

for short_opt, long_opt in (('-I', '--ignore-installed'),
                            ('-U', '--upgrade'),
                            ('-M', '--use-mirrors')):
    install_parser.add_argument(short_opt, long_opt, action='append_const',
                                const=long_opt, dest='pass_on_flags',
                                help='Passed on to pip.')


def do_install(args):
    with TempDir() as download_dir, TempDir() as rpm_dir:
        argv = [
            args.pip_binary,
            'install',
            '--no-install',
            '--build', download_dir.name,
        ]

        if args.quiet:
            argv.append('--quiet')

        argv.extend(args.packages)

        if args.pass_on_flags:
            argv.extend(args.pass_on_flags)

        # downloads packages
        print "Downloading packages."
        subprocess.check_call(argv)

        # build rpms
        for pkg_dir in os.listdir(download_dir.name):
            print "Building %s." % pkg_dir
            pkg_path = os.path.join(download_dir.name, pkg_dir)
            setuppy = os.path.join(pkg_path, 'setup.py')
            argv = [args.python, setuppy, '--quiet', 'bdist_rpm',
                    '--binary-only',
                    '--dist-dir', rpm_dir.name,
                    '--python', args.python,
                    '--release', 'pimp',
            ]

            if args.quiet:
                argv.append('--quiet')


            with open('/dev/null', 'w') as devnull:
                subprocess.check_call(argv, cwd=pkg_path,
                                      stdout=devnull if args.quiet else None,
                                      stderr=devnull if args.quiet else None)

        # install rpms
        print 'Done building RPMs.'
        rpms = [os.path.join(rpm_dir.name, fn) for fn in os.listdir(rpm_dir.name)]
        if rpms:
            argv = ['sudo', 'yum', 'install']
            if args.assumeyes:
                argv.append('--assumeyes')
            argv.extend(rpms)
            print 'Installing %d packages' % len(rpms)
            subprocess.check_call(argv)
        print 'Installation complete.'


def main():
    args = parser.parse_args()

    pip_binary = args.pip
    if not pip_binary:
        for exc in ('python-pip', 'pip-python', 'pip'):
            pip_binary = shutil.which(exc)
            if pip_binary:
                break
    else:
        pip_binary = os.path.abspath(pip_binary)
        if not os.path.exists(pip_binary):
            pip_binary = None

    if not pip_binary:
        print >>sys.stderr, 'Cannot find pip.'
        sys.exit(1)

    args.pip_binary = pip_binary
    print "PIP Binary:", pip_binary
    print "Python binary:", args.python

    {
        'install': do_install
    }[args.action](args)
