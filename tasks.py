# -*- coding: utf-8 -*-
import sys
import os
from pathlib import Path

from invoke import task


__ABSPATH__ = Path(__file__).parent
__version__ = "v2021.1.0a2"


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
        print(pattern)
        if sys.platform in ('win32', 'cygwin'):
            abs_path = __ABSPATH__.joinpath(pattern)
            if os.path.exists(abs_path):
                c.run("@RD /S /Q {}".format(abs_path))
        else:
            c.run("rm -rf {}".format(pattern))


@task(pre=[clean])
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
        nsi_file = __ABSPATH__.joinpath("resources/installer/windows.nsi")
        c.run(f'makensis /V4 /DVERSION="{__version__}" "{nsi_file}"')
    elif sys.platform in ('darwin', 'linux'):
        pass
    else:
        raise EnvironmentError('Unknown operating system.')
