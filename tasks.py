# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from invoke import task


@task
def prepare(ctx):
    """Generate environment installing dependencies"""
    ctx.run('pip install -t . -r lambda-requirements.txt')
    ctx.run('rm -f lambda.zip')
    ctx.run('zip -r lambda.zip *')


if __name__ == '__main__':
    print('This file is used by calling invoke')
    from invoke.main import program

    program.run()
