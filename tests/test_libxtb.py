# This file is part of xtb.
#
# Copyright (C) 2020 Sebastian Ehlert
#
# xtb is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# xtb is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with xtb.  If not, see <https://www.gnu.org/licenses/>.


from xtbwheel import API_VERSION
from xtbwheel.libxtb import get_api_version


def parse_version(x: str) -> tuple[int, int, int]:
    result: list[int] = [int(i) for i in str(x).split(".")]
    if len(result) < 3:
        result += [0] * (3 - len(result))
    return result[0], result[1], result[2]


def test_api_version():
    """Ensure that the API version is compatible."""
    assert parse_version(get_api_version()) >= parse_version(API_VERSION)
