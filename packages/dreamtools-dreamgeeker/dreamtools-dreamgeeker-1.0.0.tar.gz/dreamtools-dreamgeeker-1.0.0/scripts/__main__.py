#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __main__.py

import sys, shutil

from dreamtools.cfgmng import CFGBases as cfgloader
from dreamtools import tools
#from source import source


def setproject ():
    """
    Intialisation du projet
    """
    import pkg_resources

    base = tools.dir_worked()
    dest= tools.path_build(base, 'cfg')

    print ('**************************************************************************')
    print('** Création architecture')
    print('** -----------------------------------------------------------------------')
    print('** Répertoire logs ')
    tools.makedirs(tools.path_build(base, 'logs'))
    print('**\t>> Répertoire créé : ', tools.path_build(base, 'logs'))
    print('** Répertoire configuration')
    src = pkg_resources.resource_filename('dreamtools', 'cfg')
    shutil.copytree(src, dest)
    print('**\t>> Répertoire créé : ', dest)
    print('**=======================================================================-')


if __name__ == "__main__":
    sys.exit(setproject())