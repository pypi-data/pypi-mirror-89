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
desc: |
	A set of functions and decorators for functional programming.
---
"""

import inspect
import functools
from contextlib import contextmanager
from datamatrix.py3compat import *
from datamatrix import DataMatrix
from datamatrix._datamatrix._basecolumn import BaseColumn
from datamatrix._datamatrix._index import Index
from datamatrix._functional._memoize import memoize


@contextmanager
def profile(path=u'profile.txt', sortby=u'cumulative'):

	"""
	desc: |
		A context manager (`with`) for easy profiling, using cProfile. The
		results of the profile are written to the file specified in the `path`
		keyword (default=`u'profile'`), and the sorting order, as accepted by
		`pstats.Stats.sort_stats()`, is specified in the the `sortby` keyword
		(default=`u'cumulative'`).

		__Example:__

		%--
		python: |
		 from datamatrix import functional as fnc

		 with fnc.profile(path=u'profile.txt', sortby=u'cumulative'):
			 dm = DataMatrix(length=1000)
			 dm.col = range(1000)
			 dm.is_even = dm.col @ (lambda x: not x % 2)
		--%
	"""

	import cProfile
	import pstats
	if py3:
		import io
	else:
		import StringIO as io

	pr = cProfile.Profile()
	pr.enable()
	yield
	pr.disable()
	s = io.StringIO()
	ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
	ps.print_stats()
	with open(path, 'w') as fd:
		fd.write(s.getvalue())



def curry(fnc):

	"""
	desc: |
		A [currying](https://en.wikipedia.org/wiki/Currying) decorator that
		turns a function with multiple arguments into a chain of partial
		functions, each of which takes at least a single argument. The input
		function may accept keywords, but the output function no longer does
		(i.e. currying turns all keywords into positional arguments).

		__Example:__

		%--
		python: |
		 from datamatrix import functional as fnc

		 @fnc.curry
		 def add(a, b, c):

		 	return a + b + c

		 print(add(1)(2)(3)) # Curried approach with single arguments
		 print(add(1, 2)(3)) # Partly curried approach
		 print(add(1)(2, 3)) # Partly curried approach
		 print(add(1, 2, 3)) # Original approach multiple arguments
		--%

	arguments:
		fnc:
			desc:	A function to curry.
			type:	callable

	returns:
		desc:	A curried function that accepts at least the first argument, and
				returns a function that accepts the second argument, etc.
		type:	callable
	"""

	def inner(*args):

		if _count_unbound_arguments(fnc) == len(args):
			return fnc(*args)
		return curry(functools.partial(fnc, *args))

	if py3:
		return functools.wraps(fnc)(inner)
	return inner


def map_(fnc, obj):

	"""
	desc: |
		Maps a function (`fnc`) onto rows of datamatrix or cells of a column.

		If `obj` is a column, the function `fnc` is mapped is mapped onto each
		cell of the column, and a new column is returned. In this case,
		`fnc` should be a function that accepts and returns a single value.

		If `obj` is a datamatrix, the function `fnc` is mapped onto each row,
		and a new datamatrix is returned. In this case, `fnc` should be a
		function that accepts a keyword `dict`, where column names are keys and
		cells are values. The return value should be another `dict`, again with
		column names as keys, and cells as values. Columns that are not part of
		the returned `dict` are left unchanged.

		*New in v0.8.0*: In Python 3.5 and later, you can also map a function
		onto a column using the `@` operator:
		`dm.new = dm.old @ (lambda i: i*2)`

		__Example:__

		%--
		python: |
		 from datamatrix import DataMatrix, functional as fnc

		 dm = DataMatrix(length=3)
		 dm.old = 0, 1, 2
		 # Map a 2x function onto dm.old to create dm.new
		 dm.new = fnc.map_(lambda i: i*2, dm.old)
		 print(dm)
		 # Map a 2x function onto the entire dm to create dm_new, using a fancy
		 # dict comprehension wrapped inside a lambda function.
		 dm_new = fnc.map_(
		 	lambda **d: {col : 2*val for col, val in d.items()},
			dm)
		 print(dm_new)
		--%

	arguments:
		fnc:
			desc:	A function to map onto each row or each cell.
			type:	callable
		obj:
			desc:	A datamatrix or column to map `fnc` onto.
			type:	[BaseColumn, DataMatrix]

	returns:
		desc:	A new column or datamatrix.
		type:	[BaseColumn, DataMatrix]
	"""

	if not callable(fnc):
		raise TypeError('fnc should be callable')
	if isinstance(obj, BaseColumn):
		return obj._map(fnc)
	if not isinstance(obj, DataMatrix):
		raise TypeError(u'obj should be DataMatrix or BaseColumn')
	dm = obj[:]
	for row in dm:
		d = {col : val for col, val in row}
		d.update(fnc(**d))
		for col, val in d.items():
			row[col] = val
	return dm


def filter_(fnc, obj):

	"""
	desc: |
		Filters rows from a datamatrix or column based on filter function
		(`fnc`).

		If `obj` is a column, `fnc` should be a function that accepts a single
		value. If `obj` is a datamatrix, `fnc` should be a function that accepts
		a keyword `dict`, where column names are keys and cells are values. In
		both cases, `fnc` should return a `bool` indicating whether the row or
		value should be included.

		*New in v0.8.0*: You can also directly compare a column with a function
		or `lambda` expression. However, this is different from `filter_()` in
		that it returns a datamatrix object and not a column.

		__Example:__

		%--
		python: |
		 from datamatrix import DataMatrix, functional as fnc

		 dm = DataMatrix(length=5)
		 dm.col = range(5)
		 # Create a column with only odd values
		 col_new = fnc.filter_(lambda x: x % 2, dm.col)
		 print(col_new)
		 # Create a new datamatrix with only odd values in col
		 dm_new = fnc.filter_(lambda **d: d['col'] % 2, dm)
		 print(dm_new)
		--%

	arguments:
		fnc:
			desc:	A filter function.
			type:	callable
		obj:
			desc:	A datamatrix or column to filter.
			type:	[BaseColumn, DataMatrix]

	returns:
		desc:	A new column or datamatrix.
		type:	[BaseColumn, DataMatrix]
	"""

	if not callable(fnc):
		raise TypeError('fnc should be callable')
	if isinstance(obj, BaseColumn):
		return (obj == fnc)[obj.name]
	if not isinstance(obj, DataMatrix):
		raise TypeError(u'obj should be DataMatrix or BaseColumn')
	dm = obj
	keep = lambda fnc, row: fnc(**{col : val for col, val in row})
	return dm._selectrowid(
		Index([rowid for rowid, row in zip(dm._rowid, obj) if keep(fnc, row)])
	)


def setcol(dm, name, value):

	"""
	desc: |
		Returns a new DataMatrix to which a column has been added or in which
		a column has been modified.

		The main difference with regular assignment (`dm.col = 'x'`) is that
		`setcol()` does not modify the original DataMatrix, and can be used in
		`lambda` expressions.

		__Example:__

		%--
		python: |
		 from datamatrix import DataMatrix, functional as fnc

		 dm1 = DataMatrix(length=5)
		 dm2 = fnc.setcol(dm1, 'y', range(5))
		 print(dm2)
		--%

	arguments:
		dm:
			desc:	A DataMatrix.
			type:	DataMatrix
		name:
			desc:	A column name.
			type:	str
		value:
			desc:	The value to be assigned to the column. This can be any
					value this is valid for a regular column assignment.

	returns:
		desc:	A new DataMatrix.
		type:	DataMatrix
	"""

	if not isinstance(name, basestring):
		raise TypeError('name should be a string')
	newdm = dm[:]
	if isinstance(value, BaseColumn):
		if value._datamatrix is not dm:
			raise Exception('This column does not belong to this DataMatrix')
		value._datamatrix = newdm
	newdm[name] = value
	return newdm


# Private functions


def _count_unbound_arguments(fnc):

	"""
	visible: False

	desc:
		Counts how many unbound arguments fnc takes. This is a wrapper function
		that works around the quirk that partialed functions are not real
		functions in Python 2.
	"""

	nbound = 0
	# In Python 2, functools.partial doesn't return a real function object, so
	# we need to dig to arrive at the actual funcion while remembering how many
	# arguments were bound.
	while isinstance(fnc, functools.partial):
		nbound += len(fnc.args)
		fnc = fnc.func
	return len(inspect.getargspec(fnc).args) - nbound
