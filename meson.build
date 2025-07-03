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

project(
  'xtbwheel',
  'c',
  license: 'LGPL-3.0-or-later',
  default_options: [
    'default_library=static',
    'buildtype=debugoptimized',
  ]
)
install = true

xtb_dep = dependency(
  'xtb',
  version: '>=@0@'.format(meson.project_version()),
  fallback: ['xtb-latest', 'xtb_dep'],
  default_options: [
    'default_library=static',
    'c_api=true',
  ],
)
# xtb_dep = dependency('xtb-latest', static: true)
xtb_header = files('include' / 'xtb.h')

cc = meson.get_compiler('c')

pymod = import('python')
python = pymod.find_installation(
  get_option('python_version'),
  modules: [
    'cffi',
  ],
  pure: false,
)
python_dep = python.dependency(required: true)

# Python's CFFI is horrible in working with preprocessor statements,
# therefore, we have to preprocess the header before passing it to the ffibuilder
xtb_pp = configure_file(
  command: [
    cc,
    '-I@0@'.format(
      meson.current_source_dir() / 'include',
      # TODO: support in upstream xtb
      # xtb_dep.get_variable(
      #   pkgconfig: 'includedir',
      #   cmake: 'tblite_INCLUDE_DIRS',
      #   internal: 'includedir',
      # ).split().get(0)
    ),
    '-DXTB_CFFI',
    '-E',
    '@INPUT@',
  ],
  input: xtb_header,
  output: '_libxtb.h',
  capture: true,
)

# This is the actual out-of-line API processing of the ffibuilder
xtb_cffi_srcs = configure_file(
  command: [python, files('ffibuilder.py'), '@INPUT@', '@BASENAME@'],
  input: xtb_pp,
  output: '@BASENAME@.c',
)

# Actual generation of the Python extension, since the shared_module does not work
# well with dependency objects, we will trick it by linking a whole static lib
xtb_pyext = python.extension_module(
  '_libxtb',
  link_whole: static_library(
    '_libxtb',
    xtb_cffi_srcs,
    dependencies: [xtb_dep, python_dep],
  ),
  dependencies: [xtb_dep, python_dep],
  install: install,
  subdir: 'xtbwheel',
)

if install
  python.install_sources(
    files(
      'xtbwheel' / '__init__.py',
      'xtbwheel' / 'interface.py',
      'xtbwheel' / 'libxtb.py',
      'xtbwheel' / 'utils.py',
      'xtbwheel' / 'ase.py' ,
      'xtbwheel' / 'qcschema.py',
    ),
    subdir: 'xtbwheel',
  )
endif
