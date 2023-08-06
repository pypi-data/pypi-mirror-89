import json
import os
import pathlib
import platform
import dataclasses

from dataclasses import dataclass, field, asdict
from typing import List
from tabulate import tabulate

def _asdict(obj):
    if isinstance(obj,dict):
        return obj
    elif dataclasses.is_dataclass(obj):
        return asdict(obj)
    elif hasattr(obj,'_asdict'):
        return obj._asdict()
    elif hasattr(obj,'__dict__'):
        return obj.__dict__
    else:
        return obj

def _asdicts(obj):
    if isinstance(obj, List):
        to = []
        for o in obj:
            to.append(_asdicts(o))
        return to
    elif isinstance(obj, dict):
        to = {}
        for k in obj:
            to[k] = _asdicts(obj[k])
        return to
    else:
        return _asdict(obj)

def _allkeys(obj):
    keys = []
    for o in obj:
        for key in o:
            if not key in keys:
                keys.append(key)
    return keys

def vars(objs):
    if not isinstance(objs,dict):
        raise TypeError('objs must be a dictionary')

    to = _asdicts(objs)

    inspectVarsPath = os.environ.get('INSPECT_VARS')
    if inspectVarsPath == None:
        return
    if platform.system() == 'Windows':
        inspectVarsPath = inspectVarsPath.replace("/","\\")
    else:
        inspectVarsPath = inspectVarsPath.replace("\\","/")

    pathlib.Path(os.path.dirname(inspectVarsPath)).mkdir(parents=True, exist_ok=True)

    with open(inspectVarsPath, 'w') as outfile:
        json.dump(to, outfile)

def dump(obj):
    return json.dumps(_asdicts(obj), indent=4).replace('"','').replace(': null', ':')

def printdump(obj):
    print(dump(obj))

def dumptable(objs, headers=None):
    if not isinstance(objs,List):
        raise TypeError('objs must be a list')
    dicts = _asdicts(objs)
    if headers == None:
        headers = _allkeys(dicts)
    rows = []
    for obj in dicts:
        row = []
        for k in headers:
            row.append(obj[k])
        rows.append(row)
    
    return tabulate(rows, headers=headers, tablefmt="github")

def printdumptable(obj, headers=None):
    print(dumptable(obj,headers))