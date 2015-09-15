#!/usr/bin/env python
import json

with open("config.json") as fp:
	config_obj = json.load(fp)


def rename(name):
	return config_obj['name_mapping'][name]

def get_package(name):
    return config_obj["package_mapping"][name]

def get_signature(mod_type, port_type):
    return {
    'Integer' : {
        'out' : '(org.vistrails.vistrails.basic:Integer)',
        'out0': '(org.vistrails.vistrails.basic:Integer)',
        'in' : '(org.vistrails.vistrails.basic:Integer)'
    },
    'String' : {
        'out' : '(org.vistrails.vistrails.basic:String)',
        'string' : '(org.vistrails.vistrails.basic:String)'
    },
    'List' : {
        'in0' : '(org.vistrails.vistrails.basic:Module)',
        'in1' : '(org.vistrails.vistrails.basic:Module)',
        'out0' : '(org.vistrails.vistrails.basic:List)'
    },
    'ConcatenateString' : {
        'val1' : '(org.vistrails.vistrails.basic:String)',
        'val2' : '(org.vistrails.vistrails.basic:String)',
        'out' : '(org.vistrails.vistrails.basic:String)'
    },
    'WriteFile' : {
        'in' : '(org.vistrails.vistrails.basic:String)',
        'out' : '(org.vistrails.vistrails.basic:File)'
    },
    'FileSink' : {
        'in0' : '(org.vistrails.vistrails.basic:File)',
    },
    'Sum' : {
        'val' : '(org.vistrails.vistrails.basic:List)',
        'out' : '(org.vistrails.vistrails.basic:Variant)'
    },
    'PythonSource' : {
        'out' : '(org.vistrails.vistrails.basic:String)'
        #default : '(org.vistrails.vistrails.basic:String)'
    },
    'MatlabSource' : {
        'out' : '(org.vistrails.vistrails.basic:String)'
        #default : '(org.vistrails.vistrails.basic:String)'
    },
    'File' : {
        'out' : '(org.vistrails.vistrails.basic:File)'
    }

    }[mod_type][port_type]

# Get the version from the vt name
def get_version(name):
    return {
    'Integer' : '2.1',
    'String' : '2.1',
    'List' : '2.1',
    'ConcatenateString' : '2.1',
    'WriteFile' : '2.1',
    'FileSink' : '2.1',
    'Sum' : '0.2.4',
    'PythonSource' : '2.1',
    'MatlabSource' : '2.1',
    'File' : '' ####################
    }[name]

def get_port_name(mod_type, port_type):
    return {
    'Integer' : {
        'out' : 'value',
        'out0': 'value_as_string',
        'in' : 'value'
    },
    'String' : {
        'out' : 'value',
        'string' : 'value'
    },
    'List' : {
        'in0' : 'head',
        'in1' : 'head',
        'out0' : 'value'
    },
    'ConcatenateString' : {
        'val1' : 'str1',
        'val2' : 'str2',
        'out' : 'value'
    },
    'WriteFile' : {
        'in' : 'in_value',
        'out' : 'out_value'
    },
    'FileSink' : {
        'in0' : 'file'
    },
    'Sum' : {
        'val' : 'InputList',
        'out' : 'Result'
    },
    'PythonSource' : {
        'out' : 'source',
        'string' : 'source'
        #defalut : port type
    },
    'MatlabSource' : {
        'out' : 'source',
        'string' : 'source'
        #defalut : port type
    },
    'File' : {
        'out' : 'source'
    }
    }[mod_type][port_type]

def get_port_type(mod_type, port_type):
    return {
    'Integer' : {
        'out' : 'source',
        'out0': 'source',
        'in' : 'destination'
    },
    'String' : {
        'out' : 'source',
        'string' : 'destination'
    },
    'List' : {
        'in0' : 'destination',
        'in1' : 'destination',
        'out0' : 'source'
    },
    'ConcatenateString' : {
        'val1' : 'destination',
        'val2' : 'destination',
        'out' : 'source'
    },
    'WriteFile' : {
        'out' : 'source',
        'in' : 'destination'
    },
    'FileSink' : {
        'in0' : 'destination'
    },
    'Sum' : {
        'val' : 'destination',
        'out' : 'source'
    },
    'PythonSource' : {
        'out' : 'source',
        'string' : 'destination',
        'custom_in' : 'destination',
        'custom_out' : 'source'
        #default : 'destination'
    },
    'MatlabSource' : {
        'out' : 'source',
        'string' : 'destination',
        'custom_in' : 'destination',
        'custom_out' : 'source'
        #default : 'destination'
    },
    'File' : {
        'out' : 'source'
    }
    }[mod_type][port_type]

