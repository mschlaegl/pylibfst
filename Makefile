# Copyright (c) 2022 Manfred SCHLAEGL <manfred.schlaegl@gmx.at>
#
# SPDX-License-Identifier: BSD 3-clause "New" or "Revised" License
#

.PHONY: all lint _style style package install clean

all: package

lint:
	# from .github/workflows/python-package.yml
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

_style:
	black .

style: _style lint

package:
	rm -rf dist/*
	python3 -m build

install: clean package
	pip3 uninstall pylibfst -y
	pip3 install dist/pylibfst*.whl --user

clean:
	# remove all possible artifacts
	rm -rf \
		build \
		dist \
		pylibfst.egg-info \
		fst/libfstapi.a \
		fst/CMakeFiles \
		fst/CMakeCache.txt \
		fst/cmake_install.cmake \
		fst/Makefile
