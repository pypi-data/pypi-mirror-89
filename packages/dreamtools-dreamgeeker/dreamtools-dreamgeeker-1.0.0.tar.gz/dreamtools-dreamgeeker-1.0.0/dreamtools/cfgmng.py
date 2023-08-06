# -*- coding: utf-8 -*-
# cfgmng.py

"""
Gestion fichiers de configurations (YAML)

pathfile : dreamtools/cfgmng.py

Repertoires par défaut
----------------------
.. note::
    * PROJECT_DIR/cfg/PROJECT_DIR/cfg/.log.yml : Fichier de configuration des logs
    * PROJECT_DIR/cfg/.app.yml : Fichier de configuration de l'application
    * PROJECT_DIR/cfg/categorie.yml : Fichier de liste définie par un code et un libelle
    * PROJECT_DIR/cfg/mailing.yml : Fichier de mails préparés
    * PROJECT_DIR/cfg/validators.yml : Fichier de validation(cf CERBERUS)
    * PROJECT_DIR/cfg/normalizor.yml : Fichier de normalization(cf CERBERUS)

Class CFBases
-------------
"""

import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper, CSafeLoader as SafeLoader
except ImportError:
    from yaml import Loader, Dumper, SafeLoader


from . import tools


class CFGEngine(object):
    """
    cfg engine
    """
    __dir_path = None

    @staticmethod
    def initial(baz_dir='cfg'):
        """

        :param str baz_dir:
        :return:
        """
        CFGEngine.__dir_path = tools.path_build(tools.PROJECT_DIR, baz_dir)

    @staticmethod
    def working_directory(sub_dir):
        CFGEngine.initial()
        return tools.path_build(CFGEngine.__dir_path, sub_dir)

    @staticmethod
    def loading(filepath, code=None, mode='r'):
        """
        Récupération des parametres de configuration du fichier <filepath> section <r>

        :param str filepath: Fichier de configuration
        :param str code: référence parametres à récupérer, optionnel
        :param str mode: bytes par defaut
        :return: configuration | None

        """
        config = None

        try:
            if tools.file_exists(filepath):
                with open(filepath, mode) as cfg:
                    cfg = yaml.load(cfg, Loader=SafeLoader)
                    if type(cfg).__name__ == "dict":
                        cfg = dict(cfg)
                    elif type(cfg).__name__ == "list":
                        cfg = list(cfg)

                    config = cfg.get(code) if code else cfg
        except Exception as ex:
            print(f'[Chargement du fichier {filepath}:\n', ex)
        finally:
            return config

    @staticmethod
    def save_cfg(d, f, m="w"):
        """
        Enregistrement d' un fichier
        ========================================

        :param dict[str:str]|list[] d: données à enregistrer
        :param str f: nom du fichier
        :param str m, default (write): mode "w|a", optional
        :return:
        """
        tools.makedirs(tools.dir_parent(f))

        with open(f, m) as f_yml:
            yaml.dump(d, stream=f_yml, allow_unicode=True)

        return f


class CFGBases(CFGEngine):
    """
    Cette class permet de gere des fichiers de configuration disponibles dans le repertoire <PROJET_DIR>/cfg
    """
    CFG_DIR = CFGEngine.working_directory('')  # databases parameters
    __logs = tools.path_build(CFG_DIR, '.log.yml')
    __app = tools.path_build(CFG_DIR, '.app.yml')
    __categories = tools.path_build(CFG_DIR, 'categorie.yml')
    __mail = tools.path_build(CFG_DIR, 'mailing.yml')
    __validator = tools.path_build(CFG_DIR, 'validators.yml')  # databases parameters
    __normalisator = tools.path_build(CFG_DIR, 'normalizor.yml')  # databases parameters

    @staticmethod
    def logs_cfg():
        """ Configuration des logs

        :Exemple:
            >>> import import logging.config as log_config
            >>> import logging
            >>> log_config.dictConfig(CFGBases.logs_cfg())
            >>> tracker = logging.getLogger('PROD|TEST')
            >>> tracker.info("Exemple dun message d'information")

        """

        return CFGBases.loading(CFGBases.__logs)

    @staticmethod
    def app_cfg(code=None):
        """ Parametres application

        :param str code: clé a retourner (filtre)
        :return: Configuration
        """
        return CFGBases.loading(CFGBases.__app, code)

    @staticmethod
    def validator():
        """ Parametres de validation de formulaire

        :param str code: référence du formulaire
        :return: parametres de validation
        :rtype: dict
        """
        return CFGBases.loading(CFGBases.__validator)

    @staticmethod
    def normalizor():
        """ Parametres de normalisation de formulaire
        :return: parametres de normaisation
        :rtype: dict
        """
        return CFGBases.loading(CFGBases.__normalisator)

    @staticmethod
    def mailing_lib(code):
        """ Mail préparé

        :param str code: référence du mail à envoyer
        :return: mail

        """
        return CFGBases.loading(CFGBases.__mail, code)

    @staticmethod
    def categorie_lib(code=None):
        """ Liste de definition

        :param str code: référence du de la liste
        :return: liste(s) de categories
        :rtype: dict
        """
        return CFGBases.loading(CFGBases.__categories)

__all__ = ['CFGBases']
