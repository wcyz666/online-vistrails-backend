#!/usr/bin/env python
import json

with open("config.json") as fp:
	config_obj = json.load(fp)


def rename(name):
	return config_obj['name_mapping'][name]

def get_package(name):
    return config_obj["package_mapping"][name]

def get_signature(mod_type, port_type):
	return config_obj['sig_mapping'][mod_type][port_type]

# Get the version from the vt name
def get_version(name):
    return config_obj['version_mapping'][name]

def get_port_name(mod_type, port_type):
    return config_obj['port_name_mapping'][mod_type][port_type]

def get_port_type(mod_type, port_type):
    return config_obj["port_type_mapping"][mod_type][port_type]

def get_init_count():
	return config_obj["init_count"]
	
if __name__== "__main__":
	assert rename("List") == "List"
	assert get_package("Integer") == "org.vistrails.vistrails.basic"
	assert get_signature("Float", "in") == "(org.vistrails.vistrails.basic:Float)"
	assert get_version("Integer") == "2.1"
	assert get_port_name("Float", "out0") == "value_as_string"
	assert get_port_type("MatlabSource", "custom_out") == "source"
	assert get_init_count()['action'] == 1
