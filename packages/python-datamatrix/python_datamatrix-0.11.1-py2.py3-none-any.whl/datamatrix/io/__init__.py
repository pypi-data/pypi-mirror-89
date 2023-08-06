# -*- coding: utf-8 -*-

"""
This file is part of datamatrix.

datamatrix is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

datamatrix is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with datamatrix.  If not, see <http://www.gnu.org/licenses/>.

---
desc:
	Functions to read and write DataMatrix objects from and to file.
---
"""

from datamatrix.py3compat import *
from datamatrix.io._text import readtxt, writetxt
from datamatrix.io._pickle import readpickle, writepickle
from datamatrix.io._excel import readxlsx, writexlsx
