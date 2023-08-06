#!/usr/bin/env python3

"""
|===================================|
| Permet de changer les parametres. |
|===================================|
"""

# import warnings
# import ctypes
# import datetime
# import getpass
# import hashlib
# import ipaddress
# try:
#     import matplotlib
#     import matplotlib.figure
#     import matplotlib.backends.backend_tkagg
# except ImportError:
#     warnings.warn("'matplotlib' failed to import, no possibility show a graphic.")
#     matplotlib = None
# import multiprocessing
# import os
# import pprint
# import re
# import shutil
# import socket
# import sys
# import threading
# import time
# try:
#     import tkinter
#     import tkinter.messagebox
#     import tkinter.ttk
# except ImportError:
#     warnings.warn("'tkinter' failed to import, no possibility to have interface graphical.")
#     tkinter = None
from . import settings, install, uninstall
from .hmi import tkinter, ttk, checks
from .hmi.theme import *
from .. import security
from ..tools import Printer, get_temperature

# interaction avec l'utilisateur

class Config:
    """
    |================================|
    | Interface graphique permettant |
    | de configurer raisin.          |
    |================================|
    """
    def __init__(self, existing_window=None):
        """
        :param existing_window: Une fenetre tkinter presente par ailleur.
        """
        security.request_psw(force=True)
        self.settings = settings.settings
        if not tkinter:
            raise ImportError("La configuration n'est pas possible sans 'tkinter'.")
        if existing_window:             # si il y a deja une fenetre ouverte
            self.window = tkinter.Toplevel(existing_window) # on est oblige d'utiliser un toplevel sinon ca plante
            self.window.grab_set()      # on fige la fenetre parente
            self.window.protocol(
                "WM_DELETE_WINDOW",
                lambda : (self.window.destroy(), self.window.quit())) # il se trouve que ca semble fonctionner comme ca...
        else:                           # dans le cas ou aucune instance tkinter n'existe
            self.window = tkinter.Tk()  # et bien on en cre une tout simplement
        self.initializing_variables()   # on initialise les variables des widgets a partir de self.settings
        self.create_widgets()           # on rempli la fenetre avec les widget.configure()
        self.window.focus_force()       # on donne le focus a la nouvelle fenetre
        self.window.mainloop()          # on reste attentif aux actions de l'utilisateur
    
    def __del__(self):
        """
        Au moment de la destruction de la fenetre.
        """
        self.settings.flush()

    def initializing_variables(self):
        """
        Initialise toutes les variable et leur
        injecte la bonne valeur selon la configuration existante.
        """
        with Printer("Transfer of parameters to tkinter...") as p:
            p.show("Variable declaration")
            self.username_var = tkinter.StringVar()                 # variable qui comporte le username
            self.email_var = tkinter.StringVar()                    # variable qui comporte l'adresse email
            self.give_internet_activity_var = tkinter.IntVar()      # booleen concertant les statistiques d'internet, 0 => prive, 1 => publique
            self.give_activity_schedules_var = tkinter.IntVar()     # booleen concernant l'aliment ation du pc, 0 => prive, 1 => publique
            self.give_cpu_usage_var = tkinter.IntVar()              # booleen concernant les statistiques d'utilisation du CPU
            self.give_ram_usage_var = tkinter.IntVar()              # booleen concertant les statistique de remplissage de la RAM
            self.automatic_update_var = tkinter.IntVar()            # booleen qui dit si oui ou non, on fait les mises a jour

            self.limit_fan_noise_var = tkinter.IntVar()             # booleen qui dit si l'on regule ou non, le bruit du ventilateur
            self.maximum_temperature_var = tkinter.DoubleVar()      # c'est la temperature a partir de laquelle l'ordinateur devient bruyant
            self.limit_cpu_usage_var = tkinter.IntVar()             # booleen qui dit si on regule ou non l'utilisation du CPU
            self.low_cpu_usage_var = tkinter.IntVar()               # booleen qui dit si l'on met doit tenter de metre les rocessus en priorite basse
            self.limit_ram_usage_var = tkinter.IntVar()             # booleen qui dit si on regule ou non l'utilisation de la RAM
            self.limit_bandwidth_var = tkinter.IntVar()             # booleen qui dit si l'on doit ou non, limiter la bande passante
            self.recording_directory_var = tkinter.StringVar()      # repertoire d'enreigstrement des resultats
            self.free_size_var = tkinter.StringVar()                # espace memoire a laisser disponible dans le disque d'enregisrement des resultats
            self.restrict_access_var = tkinter.IntVar()             # booleen qui permet de savoir si on restreind les droits de cluster work

            self.port_var = tkinter.StringVar()                     # port d'ecoute du serveur
            self.listen_var = tkinter.StringVar()                   # nombre de connections maximum que le serveur accepte avant de rouspetter
            self.network_name_var = tkinter.StringVar()             # nom du reseau auquel on participe
            self.dns_ipv6_var = tkinter.StringVar()                 # nom de domaine ipv6
            self.dns_ipv4_var = tkinter.StringVar()                 # nom de domaine ipv4
            self.port_forwarding_var = tkinter.StringVar()          # port de redirection
            self.accept_new_client_var = tkinter.IntVar()           # booleen qui permet de dire si l'on demande ou non l'autorisation pour se connecter
            self.force_authentication_var = tkinter.IntVar()        # booleen qui permet de forcer l'authentification
            self.access_token_var = tkinter.StringVar()             # c'est l'access token pour dropbox

            p.show("Variable assignment")
            self.username_var.set(self.settings["account"]["username"]) # le username va apparaitre dans le Entry
            self.email_var.set(self.settings["account"]["email"])   # de meme, on fait apparaitre, l'email dans le entry
            self.give_internet_activity_var.set(self.settings["account"]["give_internet_activity"])# on met le bouton dans la bonne configuration
            self.give_activity_schedules_var.set(self.settings["account"]["give_activity_schedules"])
            self.give_cpu_usage_var.set(self.settings["account"]["give_cpu_usage"])
            self.give_ram_usage_var.set(self.settings["account"]["give_ram_usage"])
            self.automatic_update_var.set(self.settings["account"]["automatic_update"])

            self.limit_fan_noise_var.set(self.settings["cluster_work"]["limit_fan_noise"])
            self.maximum_temperature_var.set(self.settings["cluster_work"]["maximum_temperature"])
            self.limit_cpu_usage_var.set(self.settings["cluster_work"]["limit_cpu_usage"])
            self.low_cpu_usage_var.set(self.settings["cluster_work"]["low_cpu_usage"])
            self.limit_ram_usage_var.set(self.settings["cluster_work"]["limit_ram_usage"])
            self.limit_bandwidth_var.set(self.settings["cluster_work"]["limit_bandwidth"])
            self.recording_directory_var.set(self.settings["cluster_work"]["recording_directory"])
            self.free_size_var.set(str(self.settings["cluster_work"]["free_size"]))
            self.restrict_access_var.set(self.settings["cluster_work"]["restrict_access"])

            self.port_var.set(str(self.settings["server"]["port"]))
            self.listen_var.set(str(self.settings["server"]["listen"]))
            self.network_name_var.set(self.settings["server"]["network_name"])
            self.dns_ipv6_var.set(self.settings["server"]["dns_ipv6"])
            self.dns_ipv4_var.set(self.settings["server"]["dns_ipv4"])
            self.port_forwarding_var.set(str(self.settings["server"]["port_forwarding"]) if self.settings["server"]["port_forwarding"] else "")
            self.accept_new_client_var.set(not self.settings["server"]["accept_new_client"]) # la question est tournee dans l'autre sens
            self.force_authentication_var.set(self.settings["server"]["force_authentication"])
            self.access_token_var.set(self.settings["server"]["access_token"] if self.settings["server"]["access_token"] else "")

    def create_widgets(self):
        """
        Mise en place du contenu des fenetres.
        """
        with Printer("Creation of wigets...") as p:
            with Printer("Main root..."):
                self.window.columnconfigure(0, weight=1)                # numero de colone, etirement relatif: On rend l'onglet redimenssionable sur la largeur
                self.window.rowconfigure(0, weight=1)                   # on rend le menu legerement etirable verticalement
                self.window.rowconfigure(1, weight=10)                  # mais tout de meme 10 fois moins que le reste
                self.window.title("Interface de configuration de raisin") # ajout d'un titre a la fenetre principale
                self.window.bind("<Escape>", lambda event : self.window.destroy()) # la fenetre est detruite avec la touche echappe
                notebook = theme(tkinter.ttk.Notebook(self.window))    # preparation des onglets
                notebook.grid(row=1, column=0, columnspan=5,            # on place les onglets sur une ligne en haut a gauche
                    sticky="ewsn")                                      # on fait en sorte que la fenetre prenne toute la place qu'elle peut                         

            with Printer("Account tab..."):
                frame_account = theme(tkinter.Frame(notebook))         # creation d'un cadre pour deposer tous les widgets 'account'
                frame_account.columnconfigure(0, weight=1)              # la colone des operations en cours ne bougera pas trop
                frame_account.columnconfigure(1, weight=1)              # de meme, la colone des label ne change pas trop
                frame_account.columnconfigure(2, weight=30)             # par contre, celle qui comporte les champs de saisie s'etire le plus
                frame_account.columnconfigure(3, weight=1)              # la colone des infos et de l'aide ne bouge pas top non plus
                for i in range(1, 11):
                    frame_account.rowconfigure(i, weight=1)             # on va donner a chaque ligne le meme ration d'expension
                notebook.add(frame_account, text="Account")             # on ancre la fenetre dans le premier onglet
                
                p.show("Username")
                theme(tkinter.Label(frame_account, text="Username :")).grid(row=1, column=1, sticky="w") # il est plaque a gauche (w=west)
                username_widget = theme(tkinter.Entry(frame_account, textvariable=self.username_var)) # variable de la bare de saisie
                username_widget.bind("<KeyRelease>", lambda event: self.username_set()) # on check des que l'on sort du champ
                username_widget.bind("<KeyPress>", lambda event: 
                    self.put_refresh(event, self.username_canva))
                username_widget.grid(row=1, column=2, sticky="ew")      # prend toute la largeur
                theme(tkinter.Button(frame_account,
                    image=icons.info(),                               # icon affiche
                    command=lambda : self.show_info(
                        "Info username",
                        "Le 'username' permet de vous identifier plus facilement dans le reseau. "
                        "Des parametres comme l'adresse mac permetent déjà de vous identifier mais ce n'est pas très parlant.\n"
                        "Du point de vu crytographhique votre username sert de 'sel cryptographique'. "
                        "Ainsi, il est plus difficile de craquer votre mot de passe."),
                    )).grid(row=1, column=3)
                self.username_canva = theme(tkinter.Canvas(frame_account))
                self.username_canva.grid(row=1, column=0)

                p.show("Email")
                theme(tkinter.Label(frame_account, text="Email :")).grid(row=2, column=1, sticky="w")
                email_widget = theme(tkinter.Entry(frame_account, textvariable=self.email_var))
                email_widget.bind("<KeyRelease>", lambda event : self.email_set())
                email_widget.bind("<KeyPress>", lambda event :
                    self.put_refresh(event, self.email_canva))
                email_widget.grid(row=2, column=2, sticky="ew")
                theme(tkinter.Button(frame_account,
                    image=icons.info(),
                    command=lambda : self.show_info(
                        "Info email",
                        "Le fait de renseigner votre email permet de vous envoyer un nouveau mot de "
                        "passe si vous avez perdu l'ancien.\n"
                        "Du point de vu crytographique votre email sert de 'sel cryptographique'. "
                        "Ainsi, il est plus difficile de craquer votre mot de passe.")
                    )).grid(row=2, column=3)
                self.email_canva = theme(tkinter.Canvas(frame_account))
                self.email_canva.grid(row=2, column=0)

                p.show("Password")
                theme(tkinter.Button(frame_account,
                    text="Gerer le mot de passe",
                    command=self.security_set,
                    )).grid(row=3, column=1, columnspan=2, sticky="ew")
                theme(tkinter.Button(frame_account,
                    image=icons.info(),
                    command=lambda : self.show_info(
                        "Info mot de passe",
                        "Le mot de passe permet plusieur choses:\n"
                        " -Chiffrer les données.\n"
                        " -Empecher n'importe qui de tout casser facilement."),
                    )).grid(row=3, column=3)
                self.security_canva = theme(tkinter.Canvas(frame_account))
                self.security_canva.grid(row=3, column=0)

                p.show("Vie privee")
                theme(tkinter.Checkbutton(frame_account, 
                    variable=self.give_internet_activity_var,
                    text="Donner des informations concerant ma connection a internet",
                    command=self.give_internet_activity_set,            # action faite au moment de cocher et decocher la case
                    )).grid(row=4, column=1, columnspan=2, sticky="ew")
                theme(tkinter.Button(frame_account,
                    image=icons.info(),
                    command=lambda : self.show_info(
                        "Info internet",
                        "Si cette option est activee, les moments ou votre ordinateur "
                        "a accès à internet sont mémorisés. Ils sont en suite retransmis "
                        "au serveur principal.\nA quoi ça sert?\n"
                        "Cela permet d'optimiser la répartition des données pour tenter de "
                        "prédire les moments ou votre machine sera joingnable.")
                    )).grid(row=4, column=3)
                self.give_internet_activity_canva = theme(tkinter.Canvas(frame_account))
                self.give_internet_activity_canva.grid(row=4, column=0)
                theme(tkinter.Checkbutton(frame_account, 
                    variable=self.give_activity_schedules_var,
                    text="Donner des informations concerant l'alimentation de mon ordinateur",
                    command=self.give_activity_schedules_set,
                    )).grid(row=5, column=1, columnspan=2, sticky="ew")
                theme(tkinter.Button(frame_account,
                    image=icons.info(),
                    command=lambda : self.show_info(
                        "Info alimentation",
                        "Si cette option est activee, les moments ou votre ordinateur "
                        "est allumé sont mémorisés. Ils sont en suite retransmis "
                        "au serveur principal.\nA quoi ça sert?\n"
                        "Cela permet d'optimiser la répartition des données pour éviter "
                        "de donner des tâches trop longues si il y a de forte chances "
                        "que votre ordinateur s'etaigne en cour de route.")
                    )).grid(row=5, column=3)
                self.give_activity_schedules_canva = theme(tkinter.Canvas(frame_account))
                self.give_activity_schedules_canva.grid(row=5, column=0)
                theme(tkinter.Checkbutton(frame_account, 
                    variable=self.give_cpu_usage_var,
                    text="Donner des informations concerant la sollicitation du CPU",
                    command=self.give_cpu_usage_set,
                    )).grid(row=6, column=1, columnspan=2, sticky="ew")
                theme(tkinter.Button(frame_account,
                    image=icons.info(),
                    command=lambda : self.show_info(
                        "Info CPU",
                        "Si cette option est activee, Le taux d'utilisation du CPU est enrifistré."
                        "Cela permet d'anticiper les moments ou les resource de votre machines serons réduites."),
                    )).grid(row=6, column=3)
                self.give_cpu_usage_canva = theme(tkinter.Canvas(frame_account))
                self.give_cpu_usage_canva.grid(row=6, column=0)
                theme(tkinter.Checkbutton(frame_account, 
                    variable=self.give_ram_usage_var,
                    text="Donner des informations concerant l'utilisation de la RAM",
                    command=self.give_ram_usage_set,
                    )).grid(row=7, column=1, columnspan=2, sticky="ew")
                theme(tkinter.Button(frame_account,
                    image=icons.info(),
                    command=lambda : self.show_info(
                        "Info RAM",
                        "Si cette option est activee, Le taux d'utilisation de la RAM est enrifistré."
                        "Cela permet de selectionner les taches a donner. En effet, si un calcul trop gourmand en RAM "
                        "est demandé, le processus est exterminé sur le champs. Prédire la disponibilité de la RAM permet "
                        "de limiter le génocide.")
                    )).grid(row=7, column=3)
                self.give_ram_usage_canva = theme(tkinter.Canvas(frame_account))
                self.give_ram_usage_canva.grid(row=7, column=0)
                theme(tkinter.Checkbutton(frame_account, 
                    variable=self.automatic_update_var,
                    text="Faire les mises a jours automatiquement",
                    command=self.automatic_update_set,
                    )).grid(row=8, column=1, columnspan=2, sticky="ew")
                theme(tkinter.Button(frame_account,
                    image=icons.info(),
                    command=lambda : self.show_info(
                        "Info upgrade",
                        "Faire les mises a jour automatiquement permet de bénéficier de nouvelles fonctionalitées, "
                        "de corriger des bugs, et d'en créer d'autres! A vous de voir!")
                    )).grid(row=8, column=3)
                self.automatic_update_canva = theme(tkinter.Canvas(frame_account))
                self.automatic_update_canva.grid(row=8, column=0)

                p.show("Padlock")
                theme(tkinter.Button(frame_account,
                    text="Gerer l'antivol",
                    command=self.padlock_set
                    )).grid(row=9, column=1, columnspan=2, sticky="ew")
                theme(tkinter.Button(frame_account,
                    image=icons.info(),
                    command=lambda : self.show_info(
                        "Info padlock",
                        "Ce systeme de protection permet plusieures choses:\n"
                        " -Encrypter un dossier dès que l'ordi démare sur une nouvelle IP. "
                        "Des le chiffrage terminé, le mot de passe est demandé afin de tous décripter. "
                        "En cas de vol, cela empèche d'avoir acces aux données et à tous les sites qui demande un compte (facebook, zoom, discord...).\n"
                        " -Envoyer un couriel. Le couriel contient l'IP, la date et peut-être une image ou du son du potentiel voleur...")
                    )).grid(row=9, column=3)
                self.padlock_canvas = theme(tkinter.Canvas(frame_account))
                self.padlock_canvas.grid(row=9, column=0)

                p.show("Installation management")
                sous_frame_account = theme(tkinter.Frame(frame_account))
                sous_frame_account.grid(row=10, column=1, columnspan=2, sticky="ew")
                theme(tkinter.Button(sous_frame_account,
                    text="Reinstall",
                    command=lambda : (uninstall.main(), self.window.destroy(), install.main()) if question_binaire("Etes vous certain de vouloir faire ça?", default=True, existing_window=self.window) else None
                    )).pack(side=tkinter.LEFT)
                theme(tkinter.Button(sous_frame_account,
                    text="Uninstall",
                    command=lambda : (uninstall.main(), self.window.quit()) if question_binaire("Etes vous certain de vouloir faire ça?", default=True, existing_window=self.window) else None
                    )).pack(side=tkinter.RIGHT)
                theme(tkinter.Button(sous_frame_account,
                    text="Purge",
                    command=lambda : sys.stderr.write("Not Implemented!\n")
                    )).pack()

            with Printer("Cluster work tab..."):
                frame_cluster = theme(tkinter.Frame(notebook))         # creation de la fenetre pour la gestion du calcul parallele
                frame_cluster.columnconfigure(0, weight=1)              # la colone des operation en cours ne se deforme pas beaucoup
                frame_cluster.columnconfigure(1, weight=10)             # Les 3 colones cenrale
                frame_cluster.columnconfigure(2, weight=1)              # s'ecartenent toutes
                frame_cluster.columnconfigure(3, weight=10)             # de la meme maniere
                frame_cluster.columnconfigure(4, weight=1)              # enfin, la colone des infos ne bouge pas trop non plus
                frame_cluster.columnconfigure(5, weight=10)
                frame_cluster.columnconfigure(6, weight=1)
                for i in range(8):
                    frame_cluster.rowconfigure(i, weight=1)
                notebook.add(frame_cluster, text="Cluster Work")        # on ancre cette fenetre
                
                p.show("Nose")
                state_fan_noise = "disable" if get_temperature() is None else "normal"
                theme(tkinter.Checkbutton(frame_cluster,
                    variable=self.limit_fan_noise_var,
                    text="Limiter le bruit du ventilateur",
                    command=self.limit_fan_noise_set,
                    state=state_fan_noise,
                    )).grid(row=1, column=1, sticky="ew")
                self.limit_fan_noise_canva = theme(tkinter.Canvas(frame_cluster))
                self.limit_fan_noise_canva.grid(row=1, column=0)
                self.schedules_fan_noise_button = theme(tkinter.Button(frame_cluster,
                    text="Horaires de limitation",
                    command=self.schedules_fan_noise_set,
                    state=state_fan_noise if self.settings["cluster_work"]["limit_fan_noise"] else "disable"
                   ))
                self.schedules_fan_noise_button.grid(row=1, column=3, sticky="ew")
                self.schedules_fan_noise_canva = theme(tkinter.Canvas(frame_cluster))
                self.schedules_fan_noise_canva.grid(row=1, column=2)
                self.calibration_temperature_button = theme(tkinter.Button(frame_cluster,
                    text="Calibration",
                    command=self.maximum_temperature_set,
                    state=state_fan_noise if self.settings["cluster_work"]["limit_fan_noise"] else "disable"
                   ))
                self.calibration_temperature_button.grid(row=1, column=5, sticky="ew")
                self.maximum_temperature_canva = theme(tkinter.Canvas(frame_cluster))
                self.maximum_temperature_canva.grid(row=1, column=4)
                theme(tkinter.Button(frame_cluster,
                    image=icons.info(),
                    command=lambda : self.show_info(
                        "Info nose",
                        "Il arrive que les ordinateurs soient bruillant a cause du ventillateur. "
                        "Or la vitesse du ventillateur dépend essentiellement de la température des CPUs. "
                        "Cette option permet donc de calmer le processus dès que le CPU atteind une certaine température.")
                    )).grid(row=1, column=6)

                p.show("CPU")
                theme(tkinter.Checkbutton(frame_cluster,
                    variable=self.limit_cpu_usage_var,
                    text="Limiter L'utilisation du CPU",
                    command=self.limit_cpu_usage_set
                    )).grid(row=2, column=1, sticky="ew")
                self.limit_cpu_usage_canva = theme(tkinter.Canvas(frame_cluster))
                self.limit_cpu_usage_canva.grid(row=2, column=0)
                self.schedules_cpu_usage_button = theme(tkinter.Button(frame_cluster,
                    text="f: horaire -> limitation",
                    command=self.schedules_cpu_usage_set,
                    state="normal" if self.settings["cluster_work"]["limit_cpu_usage"] else "disable"
                   ))
                self.schedules_cpu_usage_button.grid(row=2, column=3, sticky="ew")
                self.schedules_cpu_usage_canva = theme(tkinter.Canvas(frame_cluster))
                self.schedules_cpu_usage_canva.grid(row=2, column=2)
                theme(tkinter.Checkbutton(frame_cluster,
                    variable=self.low_cpu_usage_var,
                    text="Priorité basse",
                    command=self.low_cpu_usage_set
                    )).grid(row=2, column=5, sticky="ew")
                self.low_cpu_usage_canva = theme(tkinter.Canvas(frame_cluster))
                self.low_cpu_usage_canva.grid(row=2, column=4)
                theme(tkinter.Button(frame_cluster,
                    image=icons.info(),
                    command=lambda : self.show_info(
                        "Info CPU",
                        "Reguler l'utilisation du cpu permet de garantir une réactivité de l'ordinateur.")
                    )).grid(row=2, column=6)

                p.show("RAM")
                theme(tkinter.Checkbutton(frame_cluster,
                    variable=self.limit_ram_usage_var,
                    text="Limiter L'utilisation de la RAM",
                    command=self.limit_ram_usage_set
                    )).grid(row=3, column=1, sticky="ew")
                self.limit_ram_usage_canva = theme(tkinter.Canvas(frame_cluster))
                self.limit_ram_usage_canva.grid(row=3, column=0)
                self.schedules_ram_usage_button = theme(tkinter.Button(frame_cluster,
                    text="f: horaire -> limitation",
                    command=self.schedules_ram_usage_set,
                    state="normal" if self.settings["cluster_work"]["limit_ram_usage"] else "disable"
                   ))
                self.schedules_ram_usage_button.grid(row=3, column=3, sticky="ew")
                self.schedules_ram_usage_canva = theme(tkinter.Canvas(frame_cluster))
                self.schedules_ram_usage_canva.grid(row=3, column=2)
                theme(tkinter.Button(frame_cluster,
                    image=icons.info(),
                    command=lambda : self.show_info(
                        "Info RAM",
                        "Reguler l'utilisation de la ram permet de garantir de ne pas figer l'ordinateur!")
                    )).grid(row=3, column=6)

                p.show("Bandwidth")
                theme(tkinter.Checkbutton(frame_cluster,
                    variable=self.limit_bandwidth_var,
                    text="Limiter la bande passante",
                    command=self.limit_bandwidth_set
                    )).grid(row=4, column=1, sticky="ew")
                self.limit_bandwidth_canva = theme(tkinter.Canvas(frame_cluster))
                self.limit_bandwidth_canva.grid(row=4, column=0)
                self.schedules_verification_button = theme(tkinter.Button(frame_cluster,
                    text="Horaires de limitation",
                    command=self.schedules_bandwidth_set,
                    state="normal" if self.settings["cluster_work"]["limit_bandwidth"] else "disable"
                    ))
                self.schedules_verification_button.grid(row=4, column=3, sticky="ew")
                self.schedules_bandwidth_canva = theme(tkinter.Canvas(frame_cluster))
                self.schedules_bandwidth_canva.grid(row=4, column=2)
                self.calibration_bandwidth_button = theme(tkinter.Button(frame_cluster,
                    text="Calibration",
                    command=self.maximum_bandwidth_set,
                    state="normal" if self.settings["cluster_work"]["limit_bandwidth"] else "disable"
                    ))
                self.calibration_bandwidth_button.grid(row=4, column=5, sticky="ew")
                self.maximum_bandwidth_canva = theme(tkinter.Canvas(frame_cluster))
                self.maximum_bandwidth_canva.grid(row=4, column=4)
                theme(tkinter.Button(frame_cluster,
                    image=icons.info(),
                    command=lambda : self.show_info(
                        "Info bandwidth",
                        "Limiter la bande passante permet d'assurer a l'utilisateur un debit minimum.")
                    )).grid(row=4, column=6)
               
                p.show("Recording")
                theme(tkinter.Label(frame_cluster, text="Repertoire d'enregistrement:")).grid(row=5, column=1, sticky="w")
                theme(tkinter.Label(frame_cluster, textvariable=self.recording_directory_var)).grid(row=5, column=3)
                self.recording_directory_canva = theme(tkinter.Canvas(frame_cluster))
                self.recording_directory_canva.grid(row=5, column=0)
                theme(tkinter.Button(frame_cluster,
                    text="Changer l'emplacement",
                    command=self.recording_directory_set
                    )).grid(row=5, column=5, sticky="ew")
                theme(tkinter.Button(frame_cluster,
                    image=icons.info(),
                    command=lambda : self.show_info(
                        "Info recording",
                        "Ce repertoire est le repertoire dans lequel est enregistre tous les resultats.\n"
                        "Les resultats, c'est l'ensemble de toutes les donnees dont il faut se souvenir.")
                    )).grid(row=5, column=6)
                theme(tkinter.Label(frame_cluster, text="Espace disponible (Mio):")).grid(row=6, column=1, sticky="w")
                theme(tkinter.Label(frame_cluster, textvariable=self.free_size_var)).grid(row=6, column=3)
                theme(tkinter.Button(frame_cluster,
                    text="Changer l'espace",
                    command=self.free_size_set
                    )).grid(row=6, column=5, sticky="ew")
                theme(tkinter.Button(frame_cluster,
                    image=icons.info(),
                    command=lambda : self.show_info(
                        "Info size",
                        "La valeur rentree la est la quantitee d'espace disque a ne pas depasser. "
                        "A force de stocker des resultats, cela pourrai finir par saturer le disque "
                        "dure. Mais grace a cette option, des que le disque dur atteint un niveau critique de remplissage, "
                        "raisin compresse les resultats, supprime ceux qui sont peu utilise... Bref il se debrouille "
                        "pour ne pas depasser le cota que vous lui permettez, meme si il doit en venir a tout supprimmer!")
                    )).grid(row=6, column=6)
                self.free_size_canva = theme(tkinter.Canvas(frame_cluster))
                self.free_size_canva.grid(row=6, column=0)

                p.show("Access")
                theme(tkinter.Checkbutton(frame_cluster,
                    variable=self.restrict_access_var,
                    text="Restreindre l'acces a ce repertoire",
                    command=self.restrict_access_set
                    )).grid(row=7, column=1, columnspan=5, sticky="ew")
                self.restrict_access_canva = theme(tkinter.Canvas(frame_cluster))
                self.restrict_access_canva.grid(row=7, column=0)
                theme(tkinter.Button(frame_cluster,
                    image=icons.info(),
                    command=lambda : self.show_info(
                        "Info acces",
                        "Quand cette option est cochée, La partie de raisin qui travail pour les autre "
                        "voit ces droits extremement reduit. En effet, il n'a acces en lecture et en ecriture que dans le repertoire "
                        "d'enregistrement des résultats, les droits d'excecution dans l'environement python "
                        "et les droits de lecture dans le repertoire .raisin. Partout ailleur, il n'a plus aucun droit.\n"
                        "Cela peut etre vu comme un avantage pour la securité, mais ça peut aussi etre embetant.")
                    )).grid(row=7, column=6)

            with Printer("Server tab..."):
                frame_server = tkinter.Frame(notebook, bg=JAUNE)        # creation de la fenetre pour la gestion de l'hebergement d'un serveur
                frame_server.columnconfigure(0, weight=1)
                frame_server.columnconfigure(1, weight=1)
                frame_server.columnconfigure(2, weight=30)
                frame_server.columnconfigure(3, weight=1)
                for i in range(9):
                    frame_server.rowconfigure(i, weight=1)
                notebook.add(frame_server, text="Server")               # on ancre cette fenetre

                p.show("Local port")
                theme(tkinter.Label(frame_server, text="Port local:")).grid(row=0, column=1, sticky="w")
                port_box = theme(tkinter.Spinbox(frame_server,
                    textvariable=self.port_var,
                    from_=1,
                    to=49151,
                    increment=1,
                    command=self.port_set
                    ))
                port_box.bind("<Return>", lambda event : self.port_set())
                port_box.bind("<KeyRelease>", lambda event : self.port_set())
                port_box.grid(row=0, column=2, sticky="ew")
                self.port_canva = theme(tkinter.Canvas(frame_server))
                self.port_canva.grid(row=0, column=0)
                theme(tkinter.Button(frame_server,
                    image=icons.info(),
                    command=lambda : self.show_info(
                        "Info port",
                        "Ce port la est le port d'ecoute sur le reseau local. Quand d'autre machines veulents "
                        "s'addresser a vous, elles cherchent a vous contacter par ce port la. Il faut donc vous assurer "
                        "que ce port est ouvert (pour que les autres puissent vous joindre). "
                        "Il faut aussi que vous choisissez un port qui ne soit pas pris par une autre application.")
                    )).grid(row=0, column=3)

                p.show("Listen")
                theme(tkinter.Label(frame_server, text="Nombre max de conections:")).grid(row=1, column=1, sticky="w")
                listen_box = theme(tkinter.Spinbox(frame_server,
                    textvariable=self.listen_var,
                    from_=1,
                    to=10000,
                    increment=1,
                    command=self.listen_set
                    ))
                listen_box.bind("<Return>", lambda event : self.listen_set())
                listen_box.bind("<KeyRelease>", lambda event : self.listen_set())
                listen_box.grid(row=1, column=2, sticky="ew")
                self.listen_canva = theme(tkinter.Canvas(frame_server))
                self.listen_canva.grid(row=1, column=0)
                theme(tkinter.Button(frame_server,
                    image=icons.info(),
                    command=lambda : self.show_info(
                        "Info listen",
                        "Ce nombre correpond au nombre de requette que le serveur acceptera avant de les refuser. "
                        "Par defaut, il en accepte 2 par coeurs dans la machine (%d)." % 2*os.cpu_count())
                    )).grid(row=1, column=3)

                p.show("Network name")
                theme(tkinter.Label(frame_server, text="Nom du réseau:")).grid(row=2, column=1, sticky="w")
                network_name_widget = theme(tkinter.Entry(frame_server, textvariable=self.network_name_var)) # variable de la bare de saisie
                network_name_widget.bind("<FocusOut>", lambda event: self.network_name_set()) # on check des que l'on sort du champ
                network_name_widget.bind("<KeyPress>", lambda event: 
                    self.put_refresh(event, self.network_name_canva))
                network_name_widget.grid(row=2, column=2, sticky="ew")
                self.network_name_canva = theme(tkinter.Canvas(frame_server))
                self.network_name_canva.grid(row=2, column=0)
                theme(tkinter.Button(frame_server,
                    image=icons.info(),
                    command=lambda : self.show_info(
                        "Info netwok name",
                        "'raisin' permet de faire collaborer tout un reseau. Mais peut-être voulez-vous "
                        "creer votre propre réseau, totalement étanche au reste. Il vous suffit dans ce cas d'entrer le "
                        "nom de votre reseau")
                    )).grid(row=2, column=3)

                p.show("DNS")
                theme(tkinter.Label(frame_server, text="DNS ipv6:")).grid(row=3, column=1, sticky="w")
                dns_ipv6_widget = theme(tkinter.Entry(frame_server, textvariable=self.dns_ipv6_var))
                dns_ipv6_widget.bind("<FocusOut>", lambda event: self.dns_ip_set(6))
                dns_ipv6_widget.bind("<KeyPress>", lambda event: 
                    self.put_refresh(event, self.dns_ipv6_canva))
                dns_ipv6_widget.grid(row=3, column=2, sticky="ew")
                self.dns_ipv6_canva = theme(tkinter.Canvas(frame_server))
                self.dns_ipv6_canva.grid(row=3, column=0)
                theme(tkinter.Button(frame_server,
                    image=icons.info(),
                    command=lambda : self.show_info(
                        "Info dns ipv6",
                        "Bien que les adresses ipv6 changent moin que l'ipv4, elles sont suceptible de bouger. "
                        "Si vous êtes suffisement geek pour vous creer un nom de domaine DNS, c'est de loin la meilleur "
                        "solution pour vous joindre n'importe quand depuis n'importe ou!")
                    )).grid(row=3, column=3)
                theme(tkinter.Label(frame_server, text="DNS ipv4:")).grid(row=4, column=1, sticky="w")
                dns_ipv4_widget = theme(tkinter.Entry(frame_server, textvariable=self.dns_ipv4_var))
                dns_ipv4_widget.bind("<FocusOut>", lambda event: self.dns_ip_set(4))
                dns_ipv4_widget.bind("<KeyPress>", lambda event: 
                    self.put_refresh(event, self.dns_ipv4_canva))
                dns_ipv4_widget.grid(row=4, column=2, sticky="ew")
                self.dns_ipv4_canva = theme(tkinter.Canvas(frame_server))
                self.dns_ipv4_canva.grid(row=4, column=0)
                theme(tkinter.Button(frame_server,
                    image=icons.info(),
                    command=lambda : self.show_info(
                        "Info dns ipv4",
                        "Votre ipv4 est succeptible de changer! Du coup, les autres client/serveur de raisin "
                        "peuvent metre du temps a retrouver vorte adresse. Pour rendre cette tache très repide et efficace, "
                        "vous pouvez vous créer un nom de domaine DNS et le rentrer dans cette case.")
                    )).grid(row=4, column=3)

                p.show("Port forwarding")
                theme(tkinter.Label(frame_server, text="Port forwarding:")).grid(row=5, column=1, sticky="w")
                port_forwarding_widget = theme(tkinter.Entry(frame_server, textvariable=self.port_forwarding_var))
                port_forwarding_widget.bind("<FocusOut>", lambda event : self.port_forwarding_set())
                port_forwarding_widget.bind("<KeyPress>", lambda event : 
                    self.put_refresh(event, self.dns_ipv4_canva))
                port_forwarding_widget.bind("<KeyRelease>", lambda event :
                    self.port_forwarding_var.set("".join((c for c in self.port_forwarding_var.get() if c.isdigit()))))
                port_forwarding_widget.grid(row=5, column=2, sticky="ew")
                self.port_forwarding_canva = theme(tkinter.Canvas(frame_server))
                self.port_forwarding_canva.grid(row=5, column=0)
                theme(tkinter.Button(frame_server,
                    image=icons.info(),
                    command=lambda : self.show_info(
                        "Info redirection",
                        "Pour vous contacter, il faut au moin une ip et un port. Seulement votre port peut etre vu "
                        "que de chez vous. Si un client exterieur veux vous contacter, il faut que vous mettiez en place "
                        "une 'redirection de port'. Dans cette case, vous pouvez entrer le port publique exterieur de votre box.")
                    )).grid(row=5, column=3)

                p.show("Preferences")
                theme(tkinter.Checkbutton(frame_server,
                    variable=self.accept_new_client_var,
                    text="Demander mon autorisation avant d'accepter les nouveaux clients",
                    command=self.accept_new_client_set
                    )).grid(row=6, column=1, columnspan=2, sticky="ew")
                self.accept_new_client_canva = theme(tkinter.Canvas(frame_server))
                self.accept_new_client_canva.grid(row=6, column=0)
                theme(tkinter.Button(frame_server,
                    image=icons.info(),
                    command=lambda : self.show_info(
                        "Info autorisation",
                        "Si cette option est cochee, toutes les personnes qui veulent "
                        "se connecter a votre serveur ne pourrons pas le faire tant que vous n'aurez pas donné "
                        "explicitement l'autorisation. Par contre, une fois le feu vert donné, "
                        "les personnes autorisée peuvent se connecter sans limites.")
                    )).grid(row=6, column=3)
                theme(tkinter.Checkbutton(frame_server,
                    variable=self.force_authentication_var,
                    text="Forcer les client a prouver leur identité",
                    command=self.force_authentication_set
                    )).grid(row=7, column=1, columnspan=2, sticky="ew")
                self.force_authentication_canva = theme(tkinter.Canvas(frame_server))
                self.force_authentication_canva.grid(row=7, column=0)
                theme(tkinter.Button(frame_server,
                    image=icons.info(),
                    command=lambda : self.show_info(
                        "Info autentification",
                        "Si cette option est cochee, tous ce qui veulent vous contacter "
                        "doivent prouver que c'est bien eux. Cette methode d'autentification fonctionne a partir "
                        "des clefs RSA. Cela est bon pour la securité mais ralenti enormément la vitesse de votre serveur "
                        "car a chaque connection, vous envoyez un defit au client et vous attendez sa reponsse avant "
                        "d'établir la connection pour de bon.")
                    )).grid(row=7, column=3)

                p.show("Access token")
                theme(tkinter.Label(frame_server, text="Dropbox access token:")).grid(row=8, column=1, sticky="w")
                access_token_widget = theme(tkinter.Entry(frame_server, textvariable=self.access_token_var))
                access_token_widget.bind("<FocusOut>", lambda event : self.access_token_set())
                access_token_widget.bind("<KeyPress>", lambda event : 
                    self.put_refresh(event, self.access_token_canva))
                access_token_widget.grid(row=8, column=2, sticky="ew")
                self.access_token_canva = theme(tkinter.Canvas(frame_server))
                self.access_token_canva.grid(row=8, column=0)
                theme(tkinter.Button(frame_server,
                    image=icons.info(),
                    command=lambda : self.show_info(
                        "Info acces token",
                        "Les access token dropbox sont des clefs d'acces pour un dossier particulier de votre compte dropbox. "
                        "Ceci permet de pouvoir assurer une liaison avec vorte machine dpuis l'exterieur meme si "
                        "vous n'avez pas de redirection de port. Cela permet aussi de remplacer le DNS. "
                        "Si vous ne savez pas comment faire, visitez ce lien: https://dropbox.tech/developers/generate-an-access-token-for-your-own-account")
                    )).grid(row=8, column=3)

    def username_set(self):
        """
        Verifie que le username soit correcte.
        Affiche une icone adequate.
        Pousse le changemement.
        """
        with Printer("Username update...") as p:
            username = self.username_var.get()
            if not checks.username_verification(username):
                p.show("Invalid username '%s'" % username)
                self.username_canva.delete("all")
                self.username_canva.create_image(8, 8, image=icons.error())
            else:
                if self.settings["account"]["username"] != username:
                    self.settings["account"]["username"] = username
                self.username_canva.delete("all")
                self.username_canva.create_image(8, 8, image=icons.ok())

    def email_set(self):
        """
        Verifie que l'adresse email soit correcte.
        Affiche une icone adequat.
        Pousse les modifications si il y en a.
        """
        with Printer("Email update...") as p:
            email = self.email_var.get()
            if not checks.email_verification(email):
                p.show("Invalid email address")
                self.email_canva.delete("all")
                self.email_canva.create_image(8, 8, image=icons.error())
            else:
                if email != self.settings["account"]["email"]:
                    self.settings["account"]["email"] = email
                self.email_canva.delete("all")
                self.email_canva.create_image(8, 8, image=icons.ok())

    def security_set(self):
        """
        Alias vers raisin.security.change_psw().
        """
        with Printer("Psw update...") as p:
            self.security_canva.delete("all")
            self.security_canva.create_image(8, 8, image=icons.refresh())
            import raisin.security as security
            try:
                security.change_psw(existing_window=self.window)
            except KeyboardInterrupt as e:
                self.security_canva.delete("all")
                self.security_canva.create_image(8, 8, image=icons.error())
                raise e from e
            self.security_canva.delete("all")
            self.security_canva.create_image(8, 8, image=icons.ok())

    def give_internet_activity_set(self):
        """
        Change l'action du boutton.
        """
        with Printer("Give internet activity update...") as p:
            self.give_internet_activity_canva.delete("all")
            self.give_internet_activity_canva.create_image(8, 8, image=icons.ok())
            give_internet_activity = bool(self.give_internet_activity_var.get())
            if self.settings["account"]["give_internet_activity"] != give_internet_activity:
                self.settings["account"]["give_internet_activity"] = give_internet_activity

    def give_activity_schedules_set(self):
        """
        Change l'action du boutton.
        """
        with Printer("Give activity schedules update...") as p:
            self.give_activity_schedules_canva.delete("all")
            self.give_activity_schedules_canva.create_image(8, 8, image=icons.ok())
            give_activity_schedules = bool(self.give_activity_schedules_var.get())
            if self.settings["account"]["give_activity_schedules"] != give_activity_schedules:
                self.settings["account"]["give_activity_schedules"] = give_activity_schedules

    def give_cpu_usage_set(self):
        """
        Change l'action du boutton.
        """
        with Printer("Give CPU usage update...") as p:
            self.give_cpu_usage_canva.delete("all")
            self.give_cpu_usage_canva.create_image(8, 8, image=icons.ok())
            give_cpu_usage = bool(self.give_cpu_usage_var.get())
            if self.settings["account"]["give_cpu_usage"] != give_cpu_usage:
                self.settings["account"]["give_cpu_usage"] = give_cpu_usage

    def give_ram_usage_set(self):
        """
        Change l'action du boutton.
        """
        with Printer("Give RAM usage update...") as p:
            self.give_ram_usage_canva.delete("all")
            self.give_ram_usage_canva.create_image(8, 8, image=icons.ok())
            give_ram_usage = bool(self.give_ram_usage_var.get())
            if self.settings["account"]["give_ram_usage"] != give_ram_usage:
                self.settings["account"]["give_ram_usage"] = give_ram_usage

    def automatic_update_set(self):
        """
        Change l'action du boutton.
        """
        with Printer("'automatick update' update...") as p:
            self.automatic_update_canva.delete("all")
            self.automatic_update_canva.create_image(8, 8, image=icons.ok())
            automatic_update = bool(self.automatic_update_var.get())
            if self.settings["account"]["automatic_update"] != automatic_update:
                self.settings["account"]["automatic_update"] = automatic_update
                self.settings.flush()

    def padlock_set(self):
        """
        Interagit avec l'utilisateur afin de recuperer ces volontees vis a vis de l'antivol.
        L'interaction se fait via self._padlock_change().
        Verifi que la saisie soit correcte grace a checks.padlock_verication(...).
        Si la saisie est bonne, les nouveaux parametres sont enregistres.
        """
        with Printer("Padlock update...") as p:
            self.padlock_canvas.delete("all")
            self.padlock_canvas.create_image(8, 8, image=icons.refresh())
            try:
                change_padlock(existing_window=self.window)
            except KeyboardInterrupt as e:
                self.padlock_canvas.delete("all")
                self.padlock_canvas.create_image(8, 8, image=icons.error())
                raise e from e
            self.padlock_canvas.delete("all")
            self.padlock_canvas.create_image(8, 8, image=icons.ok())

    def limit_fan_noise_set(self):
        """
        applique le changement du boutton
        """
        with Printer("Limit fan noise update...") as p:
            self.limit_fan_noise_canva.delete("all")
            self.limit_fan_noise_canva.create_image(8, 8, image=icons.ok())
            limit_fan_noise = bool(self.limit_fan_noise_var.get())
            if self.settings["cluster_work"]["limit_fan_noise"] != limit_fan_noise:
                self.settings["cluster_work"]["limit_fan_noise"] = limit_fan_noise
                self.settings.flush()
            self.schedules_fan_noise_button.configure(state="normal" if limit_fan_noise else "disable")
            self.calibration_temperature_button.configure(state="normal" if limit_fan_noise else "disable")

    def schedules_fan_noise_set(self):
        """
        permet d'interagire avec l'utilisateur afin de lui demander
        les horaires ou il veut limiter le bruit du ventilateur
        interragit lourdement avec 'self._schedules_change(...)'
        """
        with Printer("Schedules fan noise update...") as p:
            self.schedules_fan_noise_canva.delete("all")
            self.schedules_fan_noise_canva.create_image(8, 8, image=icons.refresh())
            values = [True, False]
            schedules = self._schedules_change(self.settings["cluster_work"]["schedules_fan_noise"], "limitation (oui ou non)", values)
            if not self.schedules_verification(schedules, values):
                p.show("Invalid schedules data")
                self.schedules_fan_noise_canva.delete("all")
                self.schedules_fan_noise_canva.create_image(8, 8, image=icons.error())
                raise ValueError("Les donnees des horaires de la reduction du bruit du ventillateur sont foireuses, aucun changement n'est opere.")
            else:
                self.settings["cluster_work"]["schedules_fan_noise"] = schedules
                self.settings.flush()
                self.schedules_fan_noise_canva.delete("all")
                self.schedules_fan_noise_canva.create_image(8, 8, image=icons.ok())

    def maximum_temperature_set(self):
        """
        met a jour la temperature de seuil des CPU
        a partir de laquel il commence a y avoir du bruit
        """
        with Printer("Maximum temperature update...") as p:
            self.maximum_temperature_canva.delete("all")
            self.maximum_temperature_canva.create_image(8, 8, image=icons.refresh())
            temperature = self._temperature_change()
            if not self.temperature_verification(temperature):
                p.show("Il y a eu un probleme pour la calibration de la temperature seuil.")
                self.maximum_temperature_canva.delete("all")
                self.maximum_temperature_canva.create_image(8, 8, image=icons.error())
                raise ValueError("Les donnees de la temperature sont foireuses, aucun changement n'est opere.")
            else:
                self.settings["cluster_work"]["maximum_temperature"] = temperature
                self.settings.flush()
                self.maximum_temperature_canva.delete("all")
                self.maximum_temperature_canva.create_image(8, 8, image=icons.ok())

    def temperature_verification(self, temperature):
        """
        retourne True si 'temperature' reflette bien une valeur de temperature plausible pour un processeur
        retourne False si il y a un quac
        """
        with Printer("Temperature verification...") as p:
            if type(temperature) not in (int, float):
                p.show("La temperature doit etre representee par un entier ou un flotant, pas par un %s." % type(temperature))
                return False
            if temperature < 20 or temperature > 100:
                p.show("Le tempertaure doit etre comprise en tre 20°C et 100°C. %d n'est pas dans cette fourchette." % temperature)
                return False
            return True

    def _temperature_change(self):
        """
        retourne la valeur de la nouvelle temperature
        """
        def quit(fen):
            """
            detruit la fenetre
            """
            class Tueur(threading.Thread):
                def __init__(self, papa):
                    threading.Thread.__init__(self)
                    self.papa = papa
                def run(self):
                    temperature_reader.je_dois_me_butter = True
                    while temperature_reader.is_alive():
                        pass
                    temperature_reader.consigne_glob.value = -1
                    fen.destroy()                                                           # selon qu'il y ai deja une fenetre en arriere plan
                    if "window" in self.papa.__dict__:                                      # on applique ou non la methode destroy
                        fen.quit()
            
            t = Tueur(self)
            t.start()
            valider.configure(state="disable")

        def consigne_verification(string_var):
            try:
                temperature = int(string_var.get()) if string_var.get().isdigit() else float(string_var.get())
            except ValueError:
                string_var.set(string_var.get()[:-1])
            else:
                string_var.set(str(max(20, min(100, temperature))))

        class TemperatureReader(threading.Thread):
            """
            meusure la temperature en temp reel du processeur
            et l'ecrit dans meusure_var
            """
            def __init__(self, consigne_temp, meusuree_var, consigne_glob, meusuree_glob):
                threading.Thread.__init__(self)
                self.consigne_temp = consigne_temp
                self.meusuree_var = meusuree_var
                self.consigne_glob = consigne_glob
                self.meusuree_glob = meusuree_glob
                self.je_dois_me_butter = False
                self.signature = time.time()

            def run(self):
                """
                methode lancee au moment du .start()
                """
                while not self.je_dois_me_butter:
                    temp_moy = raisin.get_temperature(0.2)
                    self.meusuree_var.set(str(round(temp_moy, 1)))
                    self.meusuree_glob.value = temp_moy                                 # on donne l'etat courant
                    self.consigne_glob.value = float(consigne_temp.get())               # et la consigne a atteindre

        def temperature_increases(consigne_glob, meusuree_glob):
            """
            adapte l'utilisation du cpu affin de le faire
            chauffer jusqu'a la temperature de consigne
            """
            cons = 1                                                                    # valeur bidon pour pouvoir demarer
            alpha = 0                                                                   # taux de cpu entre 0 et 1
            while cons > 0:                                                             # tant que l'on ne doit pas ce succider
                cons = consigne_glob.get_obj().value                                    # on recupere la temperature a atteindre
                meus = meusuree_glob.get_obj().value                                    # et la temperature actuelle
                
                alpha = max(0, min(1, alpha + (cons - meus)/1000))
                for i in range(int(alpha*6e6)):
                    pass
                time.sleep(0.1*(1-alpha))

        # initialisation de la fenetre
        if "window" in self.__dict__:                                               # si il y a deja une fenetre ouverte
            window = tkinter.Toplevel(self.window)                                  # on est oblige d'utiliser un toplevel sinon ca plante
            window.grab_set()                                                       # on fige la fenetre parente
            window.protocol("WM_DELETE_WINDOW", lambda : quit(window))              # il se trouve que ca semble fonctionner comme ca...
        else:                                                                       # dans le cas ou aucune instance tkinter n'existe
            window = tkinter.Tk()                                                   # et bien on en cre une tout simplement
            self.get_icons()

        # configuration de la fenetre
        window.title("Calibration temperature")
        window.configure(background=JAUNE)
        window.columnconfigure(0, weight=2)
        window.columnconfigure(1, weight=30)
        window.columnconfigure(2, weight=1)
        for i in range(4):
            window.rowconfigure(i, weight=1)
        window.focus_force()
        window.bind("<Escape>", lambda event : quit(window))

        # initialisation des variables
        temperature_var = tkinter.StringVar()                                       # contient la representation str de la temperature
        temperature_var.set(float(self.settings["cluster_work"]["maximum_temperature"])) # dans laquelle on injecte la temperature courante
        consigne_temp = tkinter.StringVar()                                         # contient la formule de la consigne en temperature
        consigne_temp.set("60")
        meusuree_var = tkinter.StringVar()                                          # contient la valeur de la temperature meusuree
        consigne_glob = multiprocessing.Value(ctypes.c_double, 60.0)                # contient la consigne mais c'est une variable global, pour passer entre les processus
        meusuree_glob = multiprocessing.Value(ctypes.c_double)                      # cette variable permet de transmetre la temperature meusuree aux threads
        temperature_reader = TemperatureReader(consigne_temp, meusuree_var, consigne_glob, meusuree_glob)
        threads = [multiprocessing.Process(target=temperature_increases, args=(consigne_glob, meusuree_glob)) for i in range(os.cpu_count())]

        # remplissage de la fenetre
        theme(tkinter.Label(window, text="Température de consigne (°C):")).grid(row=0, column=0, sticky="w")
        consigne_box = theme(tkinter.Spinbox(window,
            textvariable = consigne_temp,
            from_ = 20,
            to = 100,
            increment = 1
            ))
        consigne_box.bind("<Return>", lambda event : consigne_verification(consigne_temp))
        consigne_box.bind("<KeyRelease>", lambda event : consigne_verification(consigne_temp))
        consigne_box.grid(row=0, column=1, sticky="ew")
        theme(tkinter.Button(window,
            image=icons.info(),
            command=lambda : self.show_info(
                "Info consigne temperature",
                "Pour vous aider a trouver le seuil de temperature, vous pouvez essayer "
                "d'imposer une température au processeur en l'entrant dans ce champ de saisie.\n"
                "Aussitot, raisin va changer le taux d'utilisation du CPU afin d'emener l'ordinateur a "
                "la temperature demandee.")
            )).grid(row=0, column=2)
        theme(tkinter.Label(window, text="Température meusuree (°C):")).grid(row=1, column=0, sticky="w")
        theme(tkinter.Label(window, textvariable=meusuree_var)).grid(row=1, column=1)
        theme(tkinter.Button(window,
            image=icons.info(),
            command=lambda : self.show_info(
                "Info temperature meusuree",
                ("La valeur affichee est la valeur de la temperature reel actuelle. "
                "Elle est le resultat de la moyenne des "
                "temperatures de chacun des %d CPUs." % os.cpu_count()) \
                if raisin.psutil else \
                "Il faut installer le module 'raisin.psutil'.")
            )).grid(row=1, column=2)
        theme(tkinter.Label(window, text="Temperature de seuil (°C):")).grid(row=2, column=0, sticky="w")
        temperature_box = theme(tkinter.Spinbox(window,
            textvariable = temperature_var,
            from_ = 20,
            to = 100,
            increment = 1
            ))
        temperature_box.bind("<Return>", lambda event : consigne_verification(temperature_var))
        temperature_box.bind("<KeyRelease>", lambda event : consigne_verification(temperature_var))
        temperature_box.grid(row=2, column=1, sticky="ew")
        theme(tkinter.Button(window,
            image=icons.info(),
            command=lambda : self.show_info(
                "Info temperature seuil",
                "La temperature entree ici est la temperature limite a partir de laquelle le ventillateur "
                "commence a faire trop de bruit. Dans les moments ou la temperature est regulee (reglage depuis la fenetre parente), "
                "raisin fait son possible pour que l'ordinateur ne depasse pas cette temperature la.")
            )).grid(row=2, column=2)
        valider = theme(tkinter.Button(window, text="Valider", command=lambda : quit(window)))
        valider.grid(row=3, column=0, columnspan=2)

        temperature_reader.start()
        for p in threads:
            p.start()
        window.mainloop()

        return float(temperature_var.get())

    def limit_cpu_usage_set(self):
        """
        permet de basculer du mode ou il y a une regulation du cpu
        et du mode ou il n'y e a pas et inversement
        """
        with Printer("Limit cpu usage update...") as p:
            self.limit_cpu_usage_canva.delete("all")
            self.limit_cpu_usage_canva.create_image(8, 8, image=icons.ok())
            limit_cpu_usage = bool(self.limit_cpu_usage_var.get())
            if self.settings["cluster_work"]["limit_cpu_usage"] != limit_cpu_usage:
                self.settings["cluster_work"]["limit_cpu_usage"] = limit_cpu_usage
                self.settings.flush()
            self.schedules_cpu_usage_button.configure(state="normal" if limit_cpu_usage else "disable")

    def schedules_cpu_usage_set(self):
        """
        demande a l'utilisateurs le taux de limitation du CPU
        en fonction de l'heure de la journee
        interragit lourdement avec 'self._schedules_change(...)'
        """
        with Printer("Schedules cpu usage restriction update") as p:
            self.schedules_cpu_usage_canva.delete("all")
            self.schedules_cpu_usage_canva.create_image(8, 8, image=icons.refresh())
            values = list(range(101))   # c'est le pourcentage du taux de cpu maximum admissible
            schedules = self._schedules_change(self.settings["cluster_work"]["schedules_cpu_usage"], "maximum total de cpu admissible (%)", values)  
            if not self.schedules_verification(schedules, values):
                p.show("Invalid schedules data")
                self.schedules_cpu_usage_canva.delete("all")
                self.schedules_cpu_usage_canva.create_image(8, 8, image=icons.error())
                raise ValueError("Les donnees des horaires de la limitation du CPU sont foireuses, aucun changement n'est opere.")
            else:
                self.settings["cluster_work"]["schedules_cpu_usage"] = schedules
                self.settings.flush()
                self.schedules_cpu_usage_canva.delete("all")
                self.schedules_cpu_usage_canva.create_image(8, 8, image=icons.ok())

    def low_cpu_usage_set(self):
        """
        tente de metre les processus en priorite basse
        """
        with Printer("Low priority cpu usage update...") as p:
            self.low_cpu_usage_canva.delete("all")
            self.low_cpu_usage_canva.create_image(8, 8, image=icons.refresh())
            low_cpu_usage = bool(self.low_cpu_usage_var.get())
            raise NotImplementedError("Pfff, encore un truc qui reste a coder...")

    def limit_ram_usage_set(self):
        """
        permet de limiter ou non l'acces a la ram
        """
        with Printer("Limit ram usage update") as p:
            self.limit_ram_usage_canva.delete("all")
            self.limit_ram_usage_canva.create_image(8, 8, image=icons.ok())
            limit_ram_usage = bool(self.limit_ram_usage_var.get())
            if self.settings["cluster_work"]["limit_ram_usage"] != limit_ram_usage:
                self.settings["cluster_work"]["limit_ram_usage"] = limit_ram_usage
                self.settings.flush()
            self.schedules_ram_usage_button.configure(state="normal" if limit_ram_usage else "disable")

    def schedules_ram_usage_set(self):
        """
        demande a l'utilisateur la quantite de RAM maximum prise par le system
        a laisser disponible.
        interragit lourdement avec 'self._schedules_change(...)'
        """
        with Printer("Schedules ram usage restriction update...") as p:
            self.schedules_ram_usage_canva.delete("all")
            self.schedules_ram_usage_canva.create_image(8, 8, image=icons.refresh())
            if raisin.psutil:
                values = list(range(int((raisin.psutil.swap_memory().total + raisin.psutil.virtual_memory().total)/2**20))) # on met un increment de 1 Mio
            else:
                values = list(range(8*2**30)) # si on a aucune info sur la ram, on fait la supposition qu'elle fait 8 Gio
            schedules = self._schedules_change(self.settings["cluster_work"]["schedules_ram_usage"], "maximum total de ram admissible (Mio)", values)
            if not self.schedules_verification(schedules, values):
                p.show("Invalid schedules data")
                self.schedules_ram_usage_canva.delete("all")
                self.schedules_ram_usage_canva.create_image(8, 8, image=icons.error())
                raise ValueError("Les donnees des horaires de la limitation de la RAM sont foireuses, aucun changement n'est opere.")
            else:
                self.settings["cluster_work"]["schedules_ram_usage"] = schedules
                self.settings.flush()
                self.schedules_ram_usage_canva.delete("all")
                self.schedules_ram_usage_canva.create_image(8, 8, image=icons.ok())

    def limit_bandwidth_set(self):
        """
        permet de limier la bande passante
        """
        with Printer("Limit bandwidth update...") as p:
            self.limit_bandwidth_canva.delete("all")
            self.limit_bandwidth_canva.create_image(8, 8, image=icons.ok())
            limit_bandwidth = bool(self.limit_bandwidth_var.get())
            if self.settings["cluster_work"]["limit_bandwidth"] != limit_bandwidth:
                self.settings["cluster_work"]["limit_bandwidth"] = limit_bandwidth
                self.settings.flush()
            self.schedules_verification_button.configure(state="normal" if limit_bandwidth else "disable")
            self.calibration_bandwidth_button.configure(state="normal" if limit_bandwidth else "disable")

    def schedules_bandwidth_set(self):
        """
        demande a l'utilisateur les moments ou il shouaite
        limiter la bande passante
        """
        with Printer("Schedules bandwidth update...") as p:
            self.schedules_bandwidth_canva.delete("all")
            self.schedules_bandwidth_canva.create_image(8, 8, image=icons.refresh())
            values = [True, False]
            schedules = self._schedules_change(self.settings["cluster_work"]["schedules_bandwidth"], "limitation (oui ou non)", values)
            if not self.schedules_verification(schedules, values):
                p.show("Invalid schedules data")
                self.schedules_bandwidth_canva.delete("all")
                self.schedules_bandwidth_canva.create_image(8, 8, image=icons.error())
                raise ValueError("Les donnees des horaires limitation de la bande passante sont foireuses, aucun changement n'est opere.")
            else:
                self.settings["cluster_work"]["schedules_bandwidth"] = schedules
                self.settings.flush()
                self.schedules_bandwidth_canva.delete("all")
                self.schedules_bandwidth_canva.create_image(8, 8, image=icons.ok())

    def maximum_bandwidth_set(self):
        """
        aide l'utilisateur a choisir la bonne bande passante.
        met a jour les debits de seuil a partir desquels les effets
        de la bande passante commencent a se faire sentir
        """
        with Printer("Maximum bandwidth update...") as p:
            self.maximum_bandwidth_canva.delete("all")
            self.maximum_bandwidth_canva.create_image(8, 8, image=icons.refresh())
            downflow, rising_flow = self._bandwidth_change()
            if not self.bandwidth_verification(downflow, rising_flow):
                p.show("Il y a un pepin pour la calibration des debits critiques.")
                self.maximum_bandwidth_canva.delete("all")
                self.maximum_bandwidth_canva.create_image(8, 8, image=icons.error())
                raise ValueError("Les donnees du debit sont foireuses, aucun changement n'est opere.")
            else:
                self.settings["cluster_work"]["downflow"] = downflow
                self.settings["cluster_work"]["rising_flow"] = rising_flow
                self.settings.flush()
                self.maximum_bandwidth_canva.delete("all")
                self.maximum_bandwidth_canva.create_image(8, 8, image=icons.ok())

    def bandwidth_verification(self, downflow, rising_flow):
        """
        s'assure que les parametre soient corecte
        Renvoie True si les debit sont coherent, retourne False sinon
        """
        with Printer("Bandwidth verification...") as p:
            if type(downflow) not in (int, float):
                p.show("'downflow' doit etre un nonmbre, pas un %s." % type(downflow))
                return False
            if type(rising_flow) not in (int, float):
                p.show("'rising_flow' doit etre un nonmbre, pas un %s." % type(rising_flow))
                return False
            if downflow < 0 or downflow > 125:
                p.show("'downflow' doit etre compris entre 0 et 125 Mio/s. %d ne fait pas parti de cet intervalle." % downflow)
                return False
            if rising_flow < 0 or rising_flow > 125:
                p.show("'rising_flow' doit etre compris entre 0 et 125 Mio/s. %d ne fait pas parti de cet intervalle." % rising_flow)
                return False
            return True

    def _bandwidth_change(self):
        """
        interagit graphiquement avec l'utilisateur afin
        de recuperer les debits critique montant et descandant
        retourne les nouveaux debits (descendant, montant)
        """
        def quit(fen):
            """
            detruit la fenetre
            """
            fen.destroy()                                                           # selon qu'il y ai deja une fenetre en arriere plan
            if "window" in self.__dict__:                                           # on applique ou non la methode destroy
                fen.quit()  

        def verification(var):
            """
            s'assure que la variable contiene bien
            un nombre entre 0 et 125 avec 1 decimal au plus
            """
            content = var.get()
            try:
                value = float(content)
            except ValueError:
                value = 0
            value = round(min(125, max(0, value)), 1)
            if round(value) == value:
                var.set(str(round(value)))
            else:
                var.set(value)

        def down_test(dispo_down):
            """
            fait un test sur le debit descendant et affiche le resulat
            dans la variable 'dispo_down'
            """
            raise NotImplementedError("Pas de tests disponible pour le debit descendant")

        def up_test(dispo_up):
            """
            fait un test sur le debit montant et affiche le resulat
            dans la variable 'dispo_up'
            """
            raise NotImplementedError("Pas de tests disponible pour le debit montant")

        # initialisation de la fenetre
        if "window" in self.__dict__:                                               # si il y a deja une fenetre ouverte
            window = tkinter.Toplevel(self.window)                                  # on est oblige d'utiliser un toplevel sinon ca plante
            window.grab_set()                                                       # on fige la fenetre parente
            window.protocol("WM_DELETE_WINDOW", lambda : (window.destroy(), window.quit()))# il se trouve que ca semble fonctionner comme ca...
        else:                                                                       # dans le cas ou aucune instance tkinter n'existe
            window = tkinter.Tk()                                                   # et bien on en cre une tout simplement
            self.get_icons()

        # configuration de la fenetre
        window.title("Change padlock")
        window.configure(background=JAUNE)
        window.columnconfigure(0, weight=1)
        window.columnconfigure(1, weight=31)
        window.columnconfigure(2, weight=1)
        for i in range(5):
            window.rowconfigure(i, weight=1)
        window.focus_force()
        window.bind("<Escape>", lambda event : quit(window))

        # initialisation des variables
        downflow_var = tkinter.StringVar()                                          # debit descendant maximum
        downflow_var.set(str(self.settings["cluster_work"]["downflow"]))
        rising_flow_var = tkinter.StringVar()                                       # debit ascendant maximum
        rising_flow_var.set(str(self.settings["cluster_work"]["rising_flow"]))
        dispo_down = tkinter.StringVar()                                            # phrase qui indique le resultat du test du debit descendant
        dispo_down.set("Débit descendant disponible inconu")
        dispo_up = tkinter.StringVar()                                              # phrase qui indique le resultat du test du debit montant
        dispo_up.set("Débit montant disponible inconu")

        # remplissage de la fenetre
        theme(tkinter.Label(window, textvariable=dispo_down)).grid(row=0, column=0, sticky="w")
        theme(tkinter.Button(window,
            text="Lancer le test",
            command=lambda : down_test(dispo_down))).grid(row=0, column=1, sticky="ew")
        theme(tkinter.Button(window,
            image=icons.info(),
            command=lambda : self.show_info(
                "Info Debit",
                "Ce boutton lance un test de débit qui vous permet de vous faire une idée des ressource dons vous diposez.")
            )).grid(row=0, column=2)
        theme(tkinter.Label(window, text="Débit descendant admissible (Mio/s):")).grid(row=1, column=0, sticky="w")
        down_box = theme(tkinter.Spinbox(window,
            textvariable=downflow_var,
            from_=0,
            to=125,
            increment=0.1))
        down_box.bind("<Return>", lambda event : verification(downflow_var))
        down_box.bind("<KeyRelease>", lambda event : verification(downflow_var))
        down_box.grid(row=1, column=1, sticky="ew")
        theme(tkinter.Button(window,
            image=icons.info(),
            command=lambda : self.show_info(
                "Info Debit",
                "La valeur entree ici permet de restreindre le debit descendant maximum absulu par cette valeur.\n"
                "Dans les moments ou le debit est regulé (configurer les horaires dans la fenetre parente), toute les "
                "activitees concernées par le partage des ressources 'cluster work' verrons leur debit internet asservi "
                "par cette valeur.")
            )).grid(row=1, column=2)
        theme(tkinter.Label(window, textvariable=dispo_up)).grid(row=2, column=0, sticky="w")
        theme(tkinter.Button(window,
            text="Lancer le test",
            command=lambda : up_test(dispo_up))).grid(row=2, column=1, sticky="ew")
        theme(tkinter.Button(window,
            image=icons.info(),
            command=lambda : self.show_info(
                "Info Debit",
                "Ce boutton lance un test de débit qui vous permet de vous faire une idée des ressource dons vous diposez.")
            )).grid(row=2, column=2)
        theme(tkinter.Label(window, text="Débit montant admissible (Mio/s):")).grid(row=3, column=0, sticky="w")
        up_box = theme(tkinter.Spinbox(window,
            textvariable=rising_flow_var,
            from_=0,
            to=125,
            increment=0.1))
        up_box.bind("<Return>", lambda event : verification(rising_flow_var))
        up_box.bind("<KeyRelease>", lambda event : verification(rising_flow_var))
        up_box.grid(row=3, column=1, sticky="ew")
        theme(tkinter.Button(window,
            image=icons.info(),
            command=lambda : self.show_info(
                "Info Debit",
                "La valeur entree ici permet de restreindre le debit montant maximum absulu par cette valeur.\n"
                "Dans les moments ou le debit est regulé (configurer les horaires dans la fenetre parente), toute les "
                "activitees concernées par le partage des ressources 'cluster work' verrons leur debit internet asservi "
                "par cette valeur.")
            )).grid(row=3, column=2)
        theme(tkinter.Button(window, text="Valider", command=lambda : quit(window))).grid(row=4, column=0, columnspan=3)

        window.mainloop()

        return float(downflow_var.get()), float(rising_flow_var.get())

    def recording_directory_set(self):
        """
        deplace les repertoires ou sont enregistres les resultats
        """
        with Printer("Recording directory update...") as p:
            self.recording_directory_canva.delete("all")
            self.recording_directory_canva.create_image(8, 8, image=icons.refresh())
            recording_directory = tkinter.filedialog.askdirectory(
                parent=self.window,
                title="Repertoire d'enregistrement",
                initialdir=self.settings["cluster_work"]["recording_directory"])
            if not self.recording_directory_verification(recording_directory):
                p.show("Le repertoire \"%s\" n'est pas un repertoire d'enregistrement valide." % recording_directory)
                self.recording_directory_canva.delete("all")
                self.recording_directory_canva.create_image(8, 8, image=icons.error())
                raise ValueError("Ca capote là! Aller on va rien changer et tous va bien se passer!")
            with Printer("Deplacement des elements en cours..."):
                src = os.path.join(self.settings["cluster_work"]["recording_directory"], "results")
                dst = os.path.join(recording_directory, "results")
                if os.path.isdir(src):
                    shutil.move(src, dst)
                else:
                    os.mkdir(dst)
                self.settings["cluster_work"]["recording_directory"] = recording_directory
                self.settings.flush()
                self.recording_directory_var.set(recording_directory)
                self.recording_directory_canva.delete("all")
                self.recording_directory_canva.create_image(8, 8, image=icons.ok())

    def recording_directory_verification(self, recording_directory):
        """
        s'assure que le repertoire 'recording_directory' existe bien
        et que l'on a les droit d'ecriture dedan.
        Retourne False si l'une des cvonditions n'est pas respecee, True sinon.
        """
        with Printer("Recording directory verification...") as p:
            if type(recording_directory) is not str:
                p.show("'recording_directory' doit etre une chaine de caractere, pas un %s." % type(recording_directory))
                return False
            if not os.path.isdir(recording_directory):
                p.show("\"%s\" n'est pas un repertoire existant." % recording_directory)
                return False
            try:
                with open(os.path.join(recording_directory, "tmp"), "w") as f:
                    f.write("contenu test")
            except PermissionError:
                p.show("Il n'y a pas les droits d'ecriture dans le dossier \"%s\"." % recording_directory)
                return False
            else:
                os.remove(os.path.join(recording_directory, "tmp"))
            return True

    def free_size_set(self):
        """
        change la quantite d'espace disponible a maintenir
        """
        with Printer("Free size update...") as p:
            self.free_size_canva.delete("all")
            self.free_size_canva.create_image(8, 8, image=icons.refresh())
            question = "Quel espace doit etre libre (Mio) ?"
            default = str(self.settings["cluster_work"]["free_size"])
            try:
                free_size = question_reponse(question, default=default, validatecommand=self.free_size_verification, existing_window=self.window)
            except KeyboardInterrupt as e:
                self.free_size_canva.delete("all")
                self.free_size_canva.create_image(8, 8, image=icons.error())
                raise e from e
            else:
                self.free_size_var.set(str(free_size))
                self.settings["cluster_work"]["free_size"] = int(free_size)
                self.settings.flush()
                self.free_size_canva.delete("all")
                self.free_size_canva.create_image(8, 8, image=icons.ok())

    def free_size_verification(self, free_size):
        """
        s'assure que 'free_size' soit correcte
        """
        with Printer("Free size verification...") as p:
            if type(free_size) is str:
                if not free_size.isdigit():
                    p.show("'free_size' doit etre un entier positif.")
                    return False
                free_size = int(free_size)
            if type(free_size) is not int:
                p.show("'free_size' doit etre un entier ou une chaine de caractere, pas un %s." % type(free_size))
                return False
            dispo = int(shutil.disk_usage(self.settings["cluster_work"]["recording_directory"]).total/2**20)
            if free_size > dispo:
                p.show("Le disque fait seulement %d Mio!" % dispo)
                return False
            return True

    def restrict_access_set(self):
        """
        tente de restraindre ou de redonner les droits a l'application
        cluster work
        """
        with Printer("Restrict access update...") as p:
            self.restrict_access_canva.delete("all")
            self.restrict_access_canva.create_image(8, 8, image=icons.refresh())
            restrict_access = bool(self.restrict_access_var.get())
            self.settings["cluster_work"]["restrict_access"] = restrict_access
            self.settings.flush()
            self.restrict_access_canva.delete("all")
            self.restrict_access_canva.create_image(8, 8, image=icons.ok())

    def port_set(self):
        """
        met a jour le port si possible
        """
        with Printer("Port update...") as p:
            self.port_canva.delete("all")
            self.port_canva.create_image(8, 8, image=icons.refresh())
            port = self.port_var.get()
            if not self.port_verification(port):
                p.show("Il y a un bins dans le port.")
                self.port_canva.delete("all")
                self.port_canva.create_image(8, 8, image=icons.error())
            else:
                self.settings["server"]["port"] = int(port)
                self.settings.flush()
                self.port_canva.delete("all")
                self.port_canva.create_image(8, 8, image=icons.ok())

    def port_verification(self, port):
        """
        s'assure que le port d'ecoute specifie soit correcte
        retourne True si c'est la cas et False sinon
        """
        with Printer("Port verification...") as p:
            if type(port) is str:
                if not port.isdigit():
                    p.show("'port' doit etre un entier positif.")
                    return False
                port = int(port)
            if type(port) is not int:
                p.show("'port' doit etre un entier ou une chaine de caractere, pas un %s." % type(port))
                return False
            if port < 1 or port > 49151:
                p.show("'port' doit etre compris entre 1 et 49151.")
                return False
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                if raisin.Id().ipv4_lan:
                    sock.bind((str(raisin.Id().ipv4_lan), port))
                else:
                    sock.bind(("127.0.0.1", port))
                sock.listen()
                sock.close()
                sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
                if raisin.Id().ipv6:
                    sock.bind((str(raisin.Id().ipv6), port))
                else:
                    sock.bind(("::1", port))
                sock.listen()
                sock.close()
            except PermissionError:
                p.show("Le port %d nessecite d'avoir les droits d'administrateur, embetant!" % port)
                return False
            except OSError:
                p.show("Le port est deja utilise par une autre application")
                return False
            if port in raisin.communication.reserved_ports:
                proche = sorted((set(range(1024, 49152, 1)) - set(raisin.communication.reserved_ports)), key=lambda p : abs(p-port))[0]
                p.show("Ce port %d est reservé par l'institut de l'IANA. Le port libre le plus proche est le port %d." % (port, proche))
            return True

    def network_name_set(self):
        """
        met a jour le nom de serveur
        """
        with Printer("Netwok name update...") as p:
            self.network_name_canva.delete("all")
            self.network_name_canva.create_image(8, 8, image=icons.refresh())
            network_name = self.network_name_var.get()
            if not self.network_name_verification(network_name):
                p.show("Le nom de reseau n'est pas correcte")
                self.network_name_canva.delete("all")
                self.network_name_canva.create_image(8, 8, image=icons.error())
            else:
                self.settings["server"]["network_name"] = network_name
                self.settings.flush()
                self.network_name_canva.delete("all")
                self.network_name_canva.create_image(8, 8, image=icons.ok())

    def network_name_verification(self, network_name):
        """
        retourne True si 'network name'
        est un bon nom de serveur
        """
        return True

    def listen_set(self):
        """
        met a jour le nombre de connectioon simultanee maximum acceptable par le serveur
        """
        with Printer("Listen update...") as p :
            self.listen_canva.delete("all")
            self.listen_canva.create_image(8, 8, image=icons.refresh())
            listen = self.listen_var.get()
            if not self.listen_verification(listen):
                p.show("Le nombre de connection n'est pas valide.")
                self.listen_canva.delete("all")
                self.listen_canva.create_image(8, 8, image=icons.error())
            else:
                self.settings["server"]["listen"] = int(listen)
                self.settings.flush()
                self.listen_canva.delete("all")
                self.listen_canva.create_image(8, 8, image=icons.ok())

    def listen_verification(self, listen):
        """
        s'assure que le nombre de connection simultane maximum admissible par le serveur soit correct.
        retourne True si c'est la cas et False sinon
        """
        with Printer("Listen verification...") as p:
            if type(listen) is str:
                if not listen.isdigit():
                    p.show("'listen' doit etre un entier positif.")
                    return False
                listen = int(listen)
            if type(listen) is not int:
                p.show("'listen' doit etre un entier. Pas un %s." % type(listen))
                return False
            if listen < 1:
                p.show("'listen' doit etre supperieur ou egal a 1.")
                return False
            return True

    def dns_ip_set(self, version):
        """
        s'assure que le nom de de domaine donne poine bien vers ici
        """
        assert version == 6 or version == 4, "La version de protocole ip doit etre 6 ou 4, pas %s." % version # le %s c'est pas un erreur, au cas ou version ne soit pas int
        with Printer("DNS update...") as p:
            exec("self.dns_ipv%d_canva.delete('all')" % version)
            exec("self.dns_ipv%d_canva.create_image(8, 8, image=icons.refresh())" % version)
            dns = self.dns_ipv6_var.get() if version == 6 else self.dns_ipv4_var.get()
            if not dns:
                exec("self.dns_ipv%d_canva.delete('all')" % version)
                return
            if not self.dns_ip_verification(dns, version):
                p.show("Le nom de domaine donner n'est pas tout a fait bon.")
                exec("self.dns_ipv%d_canva.delete('all')" % version)
                exec("self.dns_ipv%d_canva.create_image(8, 8, image=icons.error())" % version)
            else:
                self.settings["server"]["dns_ipv%d" % version] = dns
                self.settings.flush()
                exec("self.dns_ipv%d_canva.delete('all')" % version)
                exec("self.dns_ipv%d_canva.create_image(8, 8, image=icons.ok())" % version)

    def dns_ip_verification(self, dns, version):
        """
        verfifi que le dns 'dns' soit bien un nom de domaine valide et que en plus de ca, il pointe bien ici, et c'est pas fini:
        il faut par dessus le marche qu'il prene en compte le bon protocole ip
        retourne True si toutes ces conditions sont satisfaites, False sinon
        """
        with Printer("DNS verification...") as p:
            if version != 6 and version != 4:
                p.show("La version de protocole ip doit etre 6 ou 4, pas %s." % version)
                return False
        if not raisin.re.fullmatch(r"(?!\-)(?:[a-zA-Z\d\-]{0,62}[a-zA-Z\d]\.){1,126}(?!\d+)[a-zA-Z\d]{1,63}", dns):
            p.show("Le nom de domaine doit satisfaire l'expression suivante: (?!\\-)(?:[a-zA-Z\\d\\-]{0,62}[a-zA-Z\\d]\\.){1,126}(?!\\d+)[a-zA-Z\\d]{1,63}$")
            return False
        try:
            ip = socket.gethostbyname(dns)
        except socket.gaierror:
            p.show("Ce nom de domaine n'existe pas!")
            return False
        p.show("Le domaine '%s' est associé a l'adresse '%s'." % (dns, ip))
        raisin.Id().update()
        if version == 6:
            if ipaddress.ip_address(ip) == raisin.Id().ipv6:
                return True
            elif ipaddress.ip_address(ip) == raisin.Id().ipv4_wan:
                p.show("Le DNS est bon, mais il est associer a une ipv4, pas 6, entrez le dans la case juste en dessous.")
                return False
            p.show("Le DNS ne pointe pas le bon endroit, il devrait pointer sur '%s'." % raisin.Id().ipv6)
            return False
        else:
            if ipaddress.ip_address(ip) == raisin.Id().ipv4_wan:
                return True
            elif ipaddress.ip_address(ip) == raisin.Id().ipv6:
                p.show("Le DNS est bon, mais il est associer a une ipv6, pas 4, entrez le dans la case juste au dessus.")
                return False
            p.show("Le DNS ne pointe pas le bon endroit, il devrait pointer sur '%s'." % raisin.Id().ipv4_wan)
            return False

    def port_forwarding_set(self):
        """
        met a jour le port de redirection
        """
        with Printer("Port forwarding update...") as p:
            self.port_forwarding_canva.delete("all")
            self.port_forwarding_canva.create_image(8, 8, image=icons.refresh())
            port = self.port_forwarding_var.get()
            if not self.port_forwarding_verification(port):
                p.show("La redirection de port actuelle ne fonctionne pas.")
                self.port_forwarding_canva.delete("all")
                self.port_forwarding_canva.create_image(8, 8, image=icons.error())
            else:
                self.settings["server"]["port_forwarding"] = int(port)
                self.settings.flush()
                self.port_forwarding_canva.delete("all")
                self.port_forwarding_canva.create_image(8, 8, image=icons.ok())

    def port_forwarding_verification(self, port):
        """
        regarde que la redirection de port announcee est bien coherente.
        Retourne True si c'est la cas et False si ce n'est pas le cas.
        """
        with Printer("Port forwarding verification...") as p:
            if type(port) is str:
                if not port.isdigit():
                    p.show("'port' doit etre un entier positif.")
                    return False
                port = int(port)
            if type(port) is not int:
                p.show("'port' doit etre un entier ou une chaine de caractere, pas un %s." % type(port))
                return False
            if port < 1 or port > 49151:
                p.show("'port' doit etre compris entre 1 et 49151.")
                return False

            return True
            raise NotImplementedError("Faire laverification que le port colle")

    def accept_new_client_set(self):
        """
        met a jor la variable pour accepeter les nouveau clients ou pas
        """
        with Printer("Accept new client update...") as p:
            self.accept_new_client_canva.delete("all")
            self.accept_new_client_canva.create_image(8, 8, image=icons.ok())
            accept_new_client = not bool(self.accept_new_client_var.get()) # not car la question est tournee dans l'autre sens
            if self.settings["server"]["accept_new_client"] != accept_new_client:
                self.settings["server"]["accept_new_client"] = accept_new_client
                self.settings.flush()

    def force_authentication_set(self):
        """
        met a jour la variable qui permet de forcer ou non l'authentification
        """
        with Printer("Accept new client update...") as p:
            self.force_authentication_canva.delete("all")
            self.force_authentication_canva.create_image(8, 8, image=icons.ok())
            force_authentication = bool(self.force_authentication_var.get())
            if self.settings["server"]["force_authentication"] != force_authentication:
                self.settings["server"]["force_authentication"] = force_authentication
                self.settings.flush()

    def access_token_set(self):
        """
        enregistre le nouvel acces token si il est valide
        """
        with Printer("Access token update...") as p:
            self.access_token_canva.delete("all")
            self.access_token_canva.create_image(8, 8, image=icons.refresh())
            access_token = self.access_token_var.get()
            if not self.access_token_verification(access_token):
                p.show("L'acces token specifier n'est pas corecte.")
                self.access_token_canva.delete("all")
                self.access_token_canva.create_image(8, 8, image=icons.error())
            else:
                self.settings["server"]["access_token"] = access_token
                self.settings.flush()
                self.access_token_canva.delete("all")
                self.access_token_canva.create_image(8, 8, image=icons.ok())

    def access_token_verification(self, access_token):
        """
        Retourne True si l'acces token Drobox est valide
        """
        with Printer("Access token verification...") as p:
            try:
                d = raisin.communication.dropbox.Dropbox("id", access_token)
                d.connect()
                return True
            except KeyboardInterrupt as e:
                raise e from e
            except Exception as e:
                print(e)
                p.show("Imposible de se connecter avec cet acces token.")
                return False

    def _schedules_change(self, schedules, ylabel, yvalues):
        """
        interagit avec l'utilisateur afin de lui demander des horaires de limitation
        'schedules' est le dictionaire des horaires deja existantes
        'ylabel' est le (STR) de la grandeur physique que l'on est entrain de limiter
        'yvalues' est la liste des valeurs possibles (du bas vers le haut)
        retourne le nouveau 'schedules' (pas une copie (attention au pointeur))
        """
        def quit(fen):
            """
            detruit la fenetre
            """
            fen.destroy()                                                           # selon qu'il y ai deja une fenetre en arriere plan
            if "window" in self.__dict__:                                           # on applique ou non la methode destroy
                fen.quit()
        
        def graph(day):
            """
            retourne un canvas qui contient la figure
            """
            if not matplotlib:
                raise ImportError("'matplotlib' is required to plot a graphic.")
            fig = matplotlib.figure.Figure(facecolor=JAUNE)                         # couleur de fond autour du graph
            ax = fig.add_subplot()
            ax.set_facecolor(JAUNE)                                                 # couleur de fond dans le graph
            ax.set_xlabel("time (hour)")
            ax.set_ylabel(ylabel)
            xfmt = matplotlib.dates.DateFormatter("%H:%M")                          # format de l'heure a afficher
            ax.xaxis.set_major_formatter(xfmt)

            # valeurs centrales
            dates_str = sorted(schedules[day], key = lambda d : int(60*d.split(":")[0]) + int(d.split(":")[1]))
            dates = [datetime.datetime.strptime(d, "%H:%M") for d in dates_str]
            list_y = [schedules[day][d] for d in dates_str]

            # valeurs initiale
            jour_suivant = {"monday": "tuesday", "tuesday": "wednesday", "wednesday": "thursday", "thursday": "friday", "friday": "saturday", "saturday": "sunday", "sunday": "monday"}
            jour_precedent = {v:c for c,v in jour_suivant.items()}
            initiale = schedules[jour_precedent[day]][sorted(schedules[jour_precedent[day]], key = lambda d : int(60*d.split(":")[0]) + int(d.split(":")[1]))[-1]]
            if datetime.datetime.strptime("00:00", "%H:%M") not in dates:
                dates.insert(0, datetime.datetime.strptime("00:00", "%H:%M"))
                list_y.insert(0, initiale)

            # valeur finale
            dates.append(datetime.datetime.strptime("23:59", "%H:%M"))
            list_y.append(list_y[-1])

            # fonction escalier
            for i in range(len(dates)-1):
                dates.insert(2*i + 1, dates[2*i + 1])
                list_y.insert(2*i + 1, list_y[2*i])

            ax.plot(dates, list_y, "o-", color=POURPRE)

            graph = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=frames[day])
            return graph.get_tk_widget()

        def redraw():
            """
            redessine les graphs
            """
            for day in canvas_graph:
                canvas_graph[day].delete("all")
                canvas_graph[day] = graph(day)
                canvas_graph[day].grid(row=0, column=0, columnspan=2, sticky="nesw") # on ajoute un graphique tkinter

        def validate():
            """
            verifie que chaque entree soit correcte, applique les changements
            a schedules si il y a du nouveau
            """
            # global schedules
            with Printer("Check the input...") as p:
                nouv_schedules = {}
                for day in entrees_var:
                    canvas_entree[day].delete("all")
                    canvas_entree[day].create_image(8, 8, image=icons.refresh())
                    bloc = r"(\s*\d{1,2}[h:]\d{1,2}(?:(?:\s*:\s*)|\s+)[a-zA-Z0-9\.]+)"
                    patern = bloc + r"(?:\s*[,;]" + bloc + r")*"
                    nouv_schedules[day] = {}
                    echec = True                                                    # on part defaitiste puis on va voir si ca s'arrange
                    res = re.fullmatch(patern, entrees_var[day].get())
                    if res:
                        echec = False
                        for group in re.compile(bloc).findall(entrees_var[day].get()):
                            decomposition = re.search(r"(?P<heures>\d+)[h:](?P<minutes>\d+).+?(?P<value>[a-zA-Z0-9\.]+)", group)
                            heures = int(decomposition.group("heures"))
                            minutes = int(decomposition.group("minutes"))
                            try:
                                value = eval(decomposition.group("value"))
                            except KeyboardInterrupt as e:
                                raise e from e
                            except:
                                echec = True
                            else:
                                if heures >= 24 or minutes >= 60 or value not in yvalues:
                                    echec = True
                                else:
                                    nouv_schedules[day]["%s:%s" % (("0"+str(heures))[-2:], ("0"+str(minutes))[-2:])] = value
                    if echec:
                        canvas_entree[day].delete("all")
                        canvas_entree[day].create_image(8, 8, image=icons.error())
                    else:
                        if schedules[day] != nouv_schedules[day]:
                            schedules[day] = nouv_schedules[day]
                            redraw()
                        canvas_entree[day].delete("all")
                        canvas_entree[day].create_image(8, 8, image=icons.ok())

        # initialisation de la fenetre
        if "window" in self.__dict__:                                               # si il y a deja une fenetre ouverte
            window = tkinter.Toplevel(self.window)                                  # on est oblige d'utiliser un toplevel sinon ca plante
            window.grab_set()                                                       # on fige la fenetre parente
            window.protocol("WM_DELETE_WINDOW", lambda : (window.destroy(), window.quit()))# il se trouve que ca semble fonctionner comme ca...
        else:                                                                       # dans le cas ou aucune instance tkinter n'existe
            window = tkinter.Tk()                                                   # et bien on en cre une tout simplement
            self.get_icons()
        
        # configuration de la fenetre
        window.title("Schedules configuration")
        window.rowconfigure(0, weight=1)
        window.columnconfigure(0, weight=1)
        window.bind("<Escape>", lambda event : quit(window))

        notebook = theme(tkinter.ttk.Notebook(window))
        notebook.grid(row=0, column=0, sticky="nesw")
        frames = {}
        entrees = {}
        entrees_var = {}
        canvas_entree = {}
        canvas_graph = {}
        for day in ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"):
            frames[day] = theme(tkinter.Frame(window))
            notebook.add(frames[day], text=day)
            frames[day].rowconfigure(0, weight=31)
            frames[day].rowconfigure(1, weight=1)
            frames[day].rowconfigure(2, weight=1)
            frames[day].columnconfigure(0, weight=1)
            frames[day].columnconfigure(1, weight=32)
            canvas_graph[day] = graph(day)
            canvas_graph[day].grid(row=0, column=0, columnspan=2, sticky="nesw") # on ajoute un graphique tkinter

            canvas_entree[day] = theme(tkinter.Canvas(frames[day]))
            canvas_entree[day].grid(row=1, column=0)

            entrees_var[day] = tkinter.StringVar()
            entrees_var[day].set(", ".join(("%s: %s" % (d.replace(":","h"), v) for d,v in schedules[day].items())))
            entrees[day] = theme(tkinter.Entry(frames[day], textvariable=entrees_var[day]))
            entrees[day].grid(row=1, column=1, sticky="ew")
            entrees[day].bind("<KeyRelease>", lambda event : validate())

            theme(tkinter.Button(frames[day], text="Valider", command=lambda : quit(window))).grid(row=2, column=0, columnspan=2)


        window.mainloop()
        return schedules

    def schedules_verification(self, schedules, values):
        """
        verifie que 'shedules' soit coherent pour la verification des horaires
        retourne True si c'est correcte, False sinon
        """
        with Printer("Padlock verification...") as p:
            if type(schedules) is not dict:
                p.show("'schedules' doit etre un dictionaire, pas un %s." % type(schedules))
                return False
            for day in ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"):
                if not day in schedules:
                    p.show("The '%s' key is missing." % day)
                    return False
                if type(schedules[day]) is not dict:
                    p.show("Chaque jour doit etre represente par un dictionaire, pas par un %s." % type(schedules[day]))
                    return False
                for date, limitation in schedules[day].items():
                    if not re.fullmatch(r"\d{1,2}:\d{1,2}", date):
                        p.show("Le format de la date doit satisfaire l'expression reguliere: \\d{1,2}:\\d{1,2}. %s ne la respecte pas." % date)
                        return False
                    h, m = date.split(":")
                    if int(h) >= 24:
                        p.show("On ne peut pas metre une heure plus tardive que 23h.")
                        return False
                    if int(m) >= 60:
                        p.show("Il n'y a pas plus de 60 minutes dans une heure!")
                        return False
                    if limitation not in values:
                        p.show("Les valeurs doivent etre dans %s.\nCe n'est pas le cas de %s." % (values, limitation))
            return True

    def show_info(self, title, message):
        """
        affiche une fenetre d'aide comportant le titre 'title'
        et le contenu de message 'message'
        """
        if tkinter:
            tkinter.messagebox.showinfo(title, message)
        else:
            raise NotImplementedError("Impossible d'afficher l'aide de facon non graphique")

    def put_refresh(self, event, canvas):
        """
        met dans canvas l'icon refrech si
        event est une touche imprimable
        """
        if event.keysym not in ("Tab", "Return", "Escape"):
            canvas.delete("all")
            canvas.create_image(8, 8, image=icons.refresh())

def change_padlock(*, existing_window=None):
    """
    Change l'antivol de raisin'.
    """
    with Printer("Change the raisin padlock parameters..."):
        import raisin.application.hmi.padlock as padlock
        break_time, cipher, notify_by_email, paths = padlock.get_new_padlock(existing_window=existing_window)
        settings.settings["account"]["padlock"]["break_time"] = break_time
        settings.settings["account"]["padlock"]["cipher"] = cipher
        settings.settings["account"]["padlock"]["notify_by_email"] = notify_by_email
        settings.settings["account"]["padlock"]["paths"] = paths
        settings.settings.flush()

