# Copyright (c) 2022 Manfred SCHLAEGL <manfred.schlaegl@gmx.at>
#
# SPDX-License-Identifier: BSD 3-clause "New" or "Revised" License
#

#
# C Sources to check with cppcheck
#
# check libfst only patially.
# fstapi.c and lz4.c need fixes upstream
#
#CPPCHECK_C_SOURCES=\
	fst/fastlz.c fst/fastlz.h \
	fst/fstapi.c fst/fstapi.h \
	fst/fstext.c fst/fstext.h \
	fst/lz4.c fst/lz4.h \
	fst/fst_win_unistd.h
CPPCHECK_C_SOURCES=\
	fst/fastlz.c fst/fastlz.h \
	fst/fstapi.h \
	fst/fstext.c fst/fstext.h \
	fst/lz4.h \
	fst/fst_win_unistd.h

#
# C Sources to format automaticallys
# (don't touch original libfst)
#
ASTYLE_ARGS=--options=none --suffix=none --quiet \
	    --style=linux --indent=force-tab=8 --pad-header --pad-oper --indent-preprocessor
ASTYLE_C_SOURCES=\
	fst/fstext.c fst/fstext.h


.PHONY: all lint check _style style test package install clean

all: package

lint:
	# from .github/workflows/python-package.yml
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	cppcheck -q -f ${CPPCHECK_C_SOURCES}
check: lint

_style:
	black .
	astyle $(ASTYLE_ARGS) $(ASTYLE_C_SOURCES)

style: _style lint

test:
	pytest

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
