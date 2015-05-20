import json
import xml.etree.ElementTree as ElementTree
from pprint import pprint

from link import Link
from module import Module
import HTMLParser
import urllib


# Go from web name to vt name
def rename(name):
    return {
        'Integer' : 'Integer',
        'String' : 'String',
        'List' : 'List',
        'ConcatenateString' : 'ConcatenateString',
        'WriteFile' : 'WriteFile',
        'FileSink' : 'FileSink',
        'Sum' : 'Sum',
        'PythonSource' : 'PythonSource',
        'File' : 'File',
        'MatlabSource' : 'MatlabSource',
    }[name]

# Get the package name from the vt name
def get_package(name):
    return {
        'Integer' : 'org.vistrails.vistrails.basic',
        'String' : 'org.vistrails.vistrails.basic',
        'List' : 'org.vistrails.vistrails.basic',
        'ConcatenateString' : 'org.vistrails.vistrails.basic',
        'WriteFile' : 'org.vistrails.vistrails.basic',
        'FileSink' : 'org.vistrails.vistrails.basic',
        'Sum' : 'org.vistrails.vistrails.control_flow',
        'PythonSource' : 'org.vistrails.vistrails.basic',
        'MatlabSource' : 'org.vistrails.vistrails.basic',
        'File' : 'org.vistrails.vistrails.basic'
    }[name]

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

with open('nodes.json', 'r') as webfile:
    data = json.load(webfile)
    webfile.close()

modules = []
links = []
integerNodes = []
count = {'action' : 1, 'add' : 0, 'module' : 0, 'location' : 0, 'connection' : 0, 'port' : 0, 'function' : 0, 'parameter' : 0}
ignoreValueIntegerNode = ''

inportname = {}
inporttype = {}
outportname = {}
outporttype = {}
# Read in all the nodes from json
for node in data['nodes']:

    id = node['nid']
    type = rename(node['type'])
    x = node['x']
    y = node['y']
    
    if type == 'MatlabSource':
        tmp = node['fields']['in'][0].get('val')
        with open('matlab.m', 'w') as f:
            f.write(tmp)
        tmp = """from subprocess import call\nmatlab_loc="/var/matlab/bin/matlab"\nfile_loc="./matlab.m"\ncall([matlab_loc, '-nojvm', '-nodisplay', '-r "run ' + file_loc[:-2] + ';exit;"'])"""
        h = HTMLParser.HTMLParser()
        s = h.unescape(tmp)#convert html format into normal string
        value = urllib.quote(s)#convert normal string into url format
        type = 'PythonSource'

    elif type == 'String':
        value = node['fields']['in'][0]['val']
    elif type == 'Integer':
        value = node['fields']['in'][0]['val']
        # save nid of integer nodes to later check if it occurs in between workflow flow or as a starting point
        # This is done because integer can act as a convertor from int to string also for SUM
        integerNodes.append(id)
    elif type == 'PythonSource':
        tmp = node['fields']['in'][0].get('val')
        if tmp != None:
            h = HTMLParser.HTMLParser()
            s = h.unescape(tmp)#convert html format into normal string
            value = urllib.quote(s)#convert normal string into url format
        else:
            value = ''
        #port
        #inportlen = len(node['fields']['in'])
        inportlen = len(node['custom_fields']['inputs'])
        outportlen = len(node['custom_fields']['outputs'])
        
        for i in range(0, inportlen):
            key = node['fields']['in'][i+1].get('name')
            inportname[i] = node['custom_fields']['inputs'][key]['key']
            inporttype[i] = node['custom_fields']['inputs'][key]['type']
        for i in range(0, outportlen):
            key = node['fields']['out'][i+1].get('name')
            outportname[i] = node['custom_fields']['outputs'][key]['key']
            outporttype[i] = node['custom_fields']['outputs'][key]['type']
    elif type == 'File':
        value = '/PATH' + node['fields']['in'][0]['val']###########
    else:
        value = ''

    modules.append(Module(id, type, x, y, value))
# Read in all the connections from json
for conn in data['connections']:
    par1 = conn['from_node']
    prt1 = conn['from']
    par2 = conn['to_node']
    prt2 = conn['to']
    links.append(Link(par1, par2, prt1, prt2))
    # check if any integer node is part of "to _node", then we will know if occurs in between workflow
    if par2 in integerNodes:
        ignoreValueIntegerNode = par2

# Define the initial vistrail xml tree
vt = ElementTree.Element('vistrail')
vt.attrib['id'] = ''
vt.attrib['name'] = ''
vt.attrib['version'] = '1.0.3'
vt.attrib['xmlns:xsi'] = 'http://www.w3.org/2001/XMLSchema-instance'
vt.attrib['xsi:schemaLocation'] = 'http://www.vistrails.org/vistrail.xsd'

# Translate all of the json nodes to xml modules

for mod in modules:
    act = ElementTree.SubElement(vt, 'action')
    act.attrib['date'] = '2014-01-01 00:00:00'
    act.attrib['id'] = str(count['action'])
    act.attrib['prevId'] = str(count['action'] - 1)
    act.attrib['session'] = '0'
    act.attrib['user'] = 'translate'

    add = ElementTree.SubElement(act, 'add')
    add.attrib['id'] = str(count['add'])
    add.attrib['objectId'] = str(count['module'])
    add.attrib['parentObjId'] = ''
    add.attrib['parentObjType'] = ''
    add.attrib['what'] = 'module'

    inner = ElementTree.SubElement(add, 'module')
    inner.attrib['cache'] = '1'
    inner.attrib['id'] = str(count['module'])
    inner.attrib['name'] = mod.type
    inner.attrib['namespace'] = ''
    inner.attrib['package'] = get_package(mod.type)
    inner.attrib['version'] = get_version(mod.type)

    mod.vt_id = count['module']
    mod.package = get_package(mod.type)
    count['add'] += 1
    count['action'] += 1
    count['module'] += 1

    add2 = ElementTree.SubElement(act, 'add')
    add2.attrib['id'] = str(count['add'])
    add2.attrib['objectId'] = str(count['module'] - 1)
    add2.attrib['parentObjId'] = str(count['module'] - 1)
    add2.attrib['parentObjType'] = 'module'
    add2.attrib['what'] = 'location'

    loc = ElementTree.SubElement(add2, 'location')
    loc.attrib['id'] = str(count['location'])
    loc.attrib['x'] = str(mod.x)
    loc.attrib['y'] = str(mod.y)

    addport = [None]*(len(inportname))
    innerport = [None]*(len(inportname))
    addport2 = [None]*(len(outportname))
    outterport = [None]*(len(outportname))

    if mod.type == 'PythonSource':
        j = 0
        for i in range(0, len(inportname)):

            count['add'] += 1
            count['location'] += 1

            addport[i] = ElementTree.SubElement(act, 'add')
            addport[i].attrib['id'] = str(count['add'])
            addport[i].attrib['objectId'] = str(j)
            addport[i].attrib['parentObjId'] = str(count['module'] - 1)
            addport[i].attrib['parentObjType'] = 'module'
            addport[i].attrib['what'] = 'portSpec'


            innerport[i] = ElementTree.SubElement(addport[i], 'portSpec')
            innerport[i].attrib['id'] = str(i)
            innerport[i].attrib['maxConns'] = '-1' #dont know
            innerport[i].attrib['minConns'] = '0'
            innerport[i].attrib['name'] = str(inportname[i])
            innerport[i].attrib['optional'] = '0'
            innerport[i].attrib['sortKey'] = str(i)
            innerport[i].attrib['type'] = 'input'

            portspec = ElementTree.SubElement(innerport[i], 'portSpecItem')
            portspec.attrib['default'] = ''
            portspec.attrib['entryType'] = ''
            portspec.attrib['id'] = str(i)
            portspec.attrib['label'] = ''
            portspec.attrib['module'] = str(inporttype[i])
            portspec.attrib['namespace'] = ''
            portspec.attrib['package'] = str(get_package(inporttype[i]))#'org.vistrails.vistrails.basic'#get_package(inporttype[i+1])
            portspec.attrib['pos'] = '0'
            portspec.attrib['value'] = ''

            j += 1

        for i in range(0, len(outportname)):
            count['add'] += 1
            count['location'] += 1

            addport2[i] = ElementTree.SubElement(act, 'add')
            addport2[i].attrib['id'] = str(count['add'])
            addport2[i].attrib['objectId'] = str(j)
            addport2[i].attrib['parentObjId'] = str(count['module'] - 1)
            addport2[i].attrib['parentObjType'] = 'module'
            addport2[i].attrib['what'] = 'portSpec'


            outterport[i] = ElementTree.SubElement(addport2[i], 'portSpec')
            outterport[i].attrib['id'] = str(i)
            outterport[i].attrib['maxConns'] = '-1' #dont know
            outterport[i].attrib['minConns'] = '0'
            outterport[i].attrib['name'] = str(outportname[i])
            outterport[i].attrib['optional'] = '0'
            outterport[i].attrib['sortKey'] = str(i)
            outterport[i].attrib['type'] = 'output'

            portspec = ElementTree.SubElement(outterport[i], 'portSpecItem')
            portspec.attrib['default'] = ''
            portspec.attrib['entryType'] = ''
            portspec.attrib['id'] = str(i)
            portspec.attrib['label'] = ''
            portspec.attrib['module'] = str(outporttype[i])
            portspec.attrib['namespace'] = ''
            portspec.attrib['package'] = str(get_package(outporttype[i]))#'org.vistrails.vistrails.basic'#get_package(inporttype[i+1])
            portspec.attrib['pos'] = '0'
            portspec.attrib['value'] = ''

            j += 1
            


    count['add'] += 1
    count['location'] += 1

    add_value = False

    if mod.type == 'String' and mod.value != '':
        add_value = True
        add_type = 'org.vistrails.vistrails.basic:String'
        add_name = 'value'

    if mod.type == 'FileSink':
        # Location is hard coded for now
        mod.value = '/Users/yinlin/Desktop/s15/ga/download/nodes-to-vt-test/result.txt'#'/media/sdb/falcone/nodes-to-vt/result.txt'
        add_value = True
        add_type = 'org.vistrails.vistrails.basic:OutputPath'
        add_name = 'outputPath'

        # ignore integer nodes which occur inbetween workflow
    if mod.type == 'Integer' and  mod.id != ignoreValueIntegerNode:
        add_value = True
        add_type = 'org.vistrails.vistrails.basic:Integer'
        add_name = 'value'
            
    if mod.type == 'PythonSource' and mod.value != '':
        add_value = True
        add_type = 'org.vistrails.vistrails.basic:String'
        add_name = 'source'
        
    if add_value == True:
        in_act = ElementTree.SubElement(vt, 'action')
        in_act.attrib['date'] = '2014-01-01 00:00:00'
        in_act.attrib['id'] = str(count['action'])
        in_act.attrib['prevId'] = str(count['action'] - 1)
        in_act.attrib['session'] = '0'
        in_act.attrib['user'] = 'translate'

        in_add = ElementTree.SubElement(in_act, 'add')
        in_add.attrib['id'] = str(count['add'])
        in_add.attrib['objectId'] = str(count['function'])
        in_add.attrib['parentObjId'] = str(count['module'] - 1)
        in_add.attrib['parentObjType'] = 'module'
        in_add.attrib['what'] = 'function'

        in_func = ElementTree.SubElement(in_add, 'function')
        in_func.attrib['id'] = str(count['function'])
        in_func.attrib['name'] = add_name
        in_func.attrib['pos'] = '0'

        count['add'] += 1
        count['action'] += 1
        count['function'] += 1

        in_add2 = ElementTree.SubElement(in_act, 'add')
        in_add2.attrib['id'] = str(count['add'])
        in_add2.attrib['objectId'] = str(count['parameter'])
        in_add2.attrib['parentObjId'] = str(count['parameter'])
        in_add2.attrib['parentObjType'] = 'function'
        in_add2.attrib['what'] = 'parameter'

        in_param = ElementTree.SubElement(in_add2, 'parameter')
        in_param.attrib['alias'] = ''
        in_param.attrib['id'] = str(count['parameter'])
        in_param.attrib['name'] = '<no description>'
        in_param.attrib['pos'] = '0'
        in_param.attrib['type'] = add_type
        in_param.attrib['val'] = mod.value

        count['add'] += 1
        count['parameter'] += 1
i = 0
# Translate all of the json connections to xml connections
for link in links:
    act = ElementTree.SubElement(vt, 'action')
    act.attrib['date'] = '2014-01-01 00:00:00'
    act.attrib['id'] = str(count['action'])
    act.attrib['prevId'] = str(count['action'] - 1)
    act.attrib['session'] = '0'
    act.attrib['user'] = 'translate'

    add = ElementTree.SubElement(act, 'add')
    add.attrib['id'] = str(count['add'])
    add.attrib['objectId'] = str(count['connection'])
    add.attrib['parentObjId'] = ''
    add.attrib['parentObjType'] = ''
    add.attrib['what'] = 'connection'

    conn = ElementTree.SubElement(add, 'connection')
    conn.attrib['id'] = str(count['connection'])

    count['add'] += 1
    count['action'] += 1

    add2 = ElementTree.SubElement(act, 'add')
    add2.attrib['id'] = str(count['add'])
    add2.attrib['objectId'] = str(count['port'])
    add2.attrib['parentObjId'] = str(count['connection'])
    add2.attrib['parentObjType'] = 'connection'
    add2.attrib['what'] = 'port'

    mod1 = [x for x in modules if x.id == link.parent_a][0]

    port = ElementTree.SubElement(add2, 'port')
    port.attrib['id'] = str(count['port'])
    port.attrib['moduleId'] =  str(mod1.vt_id)
    port.attrib['moduleName'] = mod1.type
    modname1 = mod1.type
    modport1 = link.port_a

    try:
        port.attrib['name'] = get_port_name(mod1.type, link.port_a)
    except KeyError:
        port.attrib['name'] = str(modport1)#inportname[0]
    try:
        port.attrib['signature'] = get_signature(mod1.type, link.port_a)
    except KeyError:
        port.attrib['signature'] = '(org.vistrails.vistrails.basic:String)'
    try:
        port.attrib['type'] = get_port_type(mod1.type, link.port_a)
    except KeyError:
        if modport1 in inportname.values():
            port.attrib['type'] = 'destination'#inporttype[0]
        else:
            port.attrib['type'] = 'source'
    # port.attrib['name'] = get_port_name(mod1.type, link.port_a)
    # port.attrib['signature'] = get_signature(mod1.type, link.port_a)
    # port.attrib['type'] = get_port_type(mod1.type, link.port_a)

    count['add'] += 1
    count['port'] += 1

    add3 = ElementTree.SubElement(act, 'add')
    add3.attrib['id'] = str(count['add'])
    add3.attrib['objectId'] = str(count['port'])
    add3.attrib['parentObjId'] = str(count['connection'])
    add3.attrib['parentObjType'] = 'connection'
    add3.attrib['what'] = 'port'

    mod2 = [x for x in modules if x.id == link.parent_b][0]

    port2 = ElementTree.SubElement(add3, 'port')
    port2.attrib['id'] = str(count['port'])
    port2.attrib['moduleId'] =  str(mod2.vt_id)
    port2.attrib['moduleName'] = mod2.type

    modname2 = mod2.type
    modport2 = link.port_b
    try:
        port2.attrib['name'] = get_port_name(mod2.type, link.port_b)
    except KeyError:
        port2.attrib['name'] = str(modport2)
    try:
        port2.attrib['signature'] = get_signature(mod2.type, link.port_b)
    except KeyError:
        port2.attrib['signature'] = '(org.vistrails.vistrails.basic:String)'
    try:
        port2.attrib['type'] = get_port_type(mod2.type, link.port_b)
    except KeyError:
        if modport2 in inportname.values():
            port2.attrib['type'] = 'destination'#inporttype[0]
        else:
            port2.attrib['type'] = 'source'
    # port2.attrib['name'] = 'dd'
    # port2.attrib['signature'] = '(org.vistrails.vistrails.basic:String)'
    # port2.attrib['type'] = 'destination'#inporttype[0]

    i += 1
    count['add'] += 1
    count['port'] += 1
    count['connection'] += 1

with open('output.xml', 'wr+') as out_file:
    out_file.write(ElementTree.tostring(vt))
