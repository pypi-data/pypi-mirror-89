# -*- coding: utf-8 -*-
"""Microapp package"""

from .utils import funcargs, funcargseval, appdict
from .framework import load_appclass, register_appclass, unregister_appclass
from .manage import Manager
#from .project import Project, MicroappProject
from .project import Project
from .group import (Group, GroupCmd, DepartureNode, ArrivalNode,
                    EntryNode, ExitNode, Hub, AppEdge)
from .app import App

class MicroappProject(Project):
    """Microapp default project"""

    _name_ = "microapp"
    _version_ = "0.3.12"
    _description_ = "A command-line portal to Microapp apps."
    _long_description_ = "A command-line portal to Microapp apps."
    _author_ = "Youngsung Kim"
    _author_email_ = "youngsung.kim.act2@gmail.com"
    _url_ = "https://github.com/grnydawn/microapp"

def run_command(**kwargs): 
    prj = MicroappProject()
    return prj.run_command(**kwargs)
    

def run_class(cls, **kwargs):
    prj = MicroappProject()
    return prj.run_class(cls, **kwargs)
