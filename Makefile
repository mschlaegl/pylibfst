# Copyright (c) 2022 Manfred SCHLAEGL <manfred.schlaegl@gmx.at>
#
# SPDX-License-Identifier: BSD 3-clause "New" or "Revised" License
#

.PHONY: all package install clean

all: package

package:
	rm -rf dist/*
	python3 -m build

install: clean package
	pip3 uninstall pylibfst -y
	pip3 install dist/pylibfst*.whl --user

clean:
	rm -rf build dist pylibfst.egg-info