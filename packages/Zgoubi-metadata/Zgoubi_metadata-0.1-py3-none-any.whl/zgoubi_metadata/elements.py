#!/usr/bin/env python3

import os
import pkg_resources

_directory = "data/elements_yaml/"

def get_raw_yaml():
	elements_yaml = {}
	for _f in pkg_resources.resource_listdir(__name__, _directory):
		elements_yaml[_f.rpartition(".")[0]] = pkg_resources.resource_string(__name__, os.path.join(_directory, _f))
	return elements_yaml

def get_parsed():
	from yaml import safe_load

	elements = {}
	for k,v in get_raw_yaml().items():
		elements[k] = safe_load(v)
	return elements
