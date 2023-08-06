#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
The Mito package, which contains functions for creating a Mito sheet. 

To generate a new sheet, simply run:

import mitosheet
mitosheet.sheet()

If running mitosheet.sheet() just prints text that looks like `MitoWidget(...`, then you need to 
install the JupyterLab extension manager by running:

jupyter labextension install @jupyter-widgets/jupyterlab-manager;

Run this command in the terminal where you install Mito. It should take 5-10 minutes to complete.

Then, restart your JupyterLab instance, and refresh your browser. Mito should now render.

NOTE: if you have any issues with installation, please email book a demo time at https://calendly.com/trymito/mito-early-access-demo
"""

from mitosheet.example import MitoWidget, sheet
from mitosheet.errors import CreationError, EditError
from mitosheet._version import __version__, version_info

# Export all the sheet functions
from mitosheet.sheet_functions import *

from .nbextension import _jupyter_nbextension_paths