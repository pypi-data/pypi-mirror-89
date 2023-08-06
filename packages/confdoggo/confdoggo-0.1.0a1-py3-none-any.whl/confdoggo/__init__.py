#  Copyright (C) 2020  The confdoggo Authors
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from .core import *
from .__version__ import *
import mimetypes

# add YAML to mimetypes database.
# necessary because yaml does not yet have
# an official mime type.
mimetypes.add_type("application/x-yaml", ".yaml")
mimetypes.add_type("application/x-yaml", ".yml")
mimetypes.add_type("application/confdoggo", ".doggo")
del mimetypes
