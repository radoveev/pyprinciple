# -*- coding: utf-8 -*-
"""Loader module for pyprinciple

This module is the entry point to the python layer of Il_principle
during initialization. It is imported by the launcher.

Copyright (C) 2017 Radomir Matveev GPL 3.0+

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

# --------------------------------------------------------------------------- #
# Import libraries
# --------------------------------------------------------------------------- #
import logging


# --------------------------------------------------------------------------- #
# Execute
# --------------------------------------------------------------------------- #
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.info("Launching GUI")
import gui
gui.main()
