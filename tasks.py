# -*- coding: utf-8 -*-
import sys
from pathlib import Path

from invoke import task


@task
def clean(c, docs=False, bytecode=False, extra=''):
    patterns = ['build']
    if docs:
        patterns.append('docs/_build')
    if bytecode:
        patterns.append('**/*.pyc')
    if extra:
        patterns.append(extra)
    for pattern in patterns:
        c.run("rm -rf {}".format(pattern))


@task(clean)
def build(c, docs=False):
    c.run("python setup.py build")
    if docs:
        c.run("sphinx-build docs docs/_build")


@task
def freeze(c):
    app_name = r'PlottingApp'
    icon_path = rf'{Path(__file__).parent.joinpath("resources/icons/PlottingApp.ico")}'

    if sys.platform in ('win32', 'cygwin'):
        options = r'--windowed --noconfirm --clean'
        resources_path = rf'--add-data {Path(__file__).parent.joinpath("resources")};resources'
        script_path = r'src\launch.py'
    elif sys.platform in ('darwin', 'linux'):
        options = r'--onefile --windowed --noconfirm --clean'
        resources_path = rf'--add-data {Path(__file__).parent.joinpath("resources")}:resources'
        script_path = r'src/launch.py'
    else:
        raise EnvironmentError('Unknown operating system.')

    c.run(rf'pyinstaller {options} -i{icon_path} -n{app_name} {resources_path} {script_path}')


@task(pre=[freeze])
def installer(c):
    if sys.platform in ('win32', 'cygwin'):
        # c.run(f"makensis /V4 /DVERSION={__version__} windows.nsi")
        c.run("cd resources/installer")
        c.run("makensis /V4 windows.nsi")
    elif sys.platform in ('darwin', 'linux'):
        pass
    else:
        raise EnvironmentError('Unknown operating system.')
