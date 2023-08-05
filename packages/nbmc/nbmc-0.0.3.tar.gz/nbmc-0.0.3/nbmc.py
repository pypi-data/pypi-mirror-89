import wavedrom
from pyDigitalWaveTools.vcd.parser import VcdParser
from parse import parse
from nmigen.back import rtlil
from nmigen import *
from nmigen.asserts import Assert, Assume, Cover, Past

import svgwrite
import subprocess
from enum import Enum
import shutil
from math import gcd
from functools import reduce
import json
from tempfile import TemporaryDirectory
import pathlib
from dataclasses import dataclass

def _find_gcd(list):
    x = reduce(gcd, list)
    return x


def _max_time(f):
    rmax = 0
    for line in f:
        r = parse('#{time:d}', line)
        if r and r['time'] > rmax:
            rmax = r['time']
    return rmax


def _find_timestep(vcd_file):
    timelist = set()
    
    for line in vcd_file:
        r = parse('#{time:d}', line)
        if r:
            timelist.add(r['time'])
    timelist = [(t+1 if t % 10 == 9 else t)for t in timelist if t != 0]
    return _find_gcd(timelist)


def _create_wsig(sig, timestep, tmax, ancestry):
    curr_step = 0
    wave_str = ''
    data = []
    last_val = None
    for data_point in sig['data']:
        timepoint, value = data_point
        timepoint = timepoint+1 if timepoint % 10 == 9 else timepoint
        while timepoint > curr_step:
            wave_str += '.'
            curr_step += timestep
        if value.startswith('b'):
            value = int(value[1:], 2)
        if value == last_val:
            wave_str += '.'
        elif sig['type']['width'] == 1:
            wave_str += str(value)
        else:
            wave_str += '='
            data.append(value)
        last_val = value
        curr_step += timestep
    while tmax > curr_step:
        wave_str += '.'
        curr_step += timestep
    return {'wave': wave_str, 'name': sig['name'], 'data': data}


def _process_scope(scope, timestep, tmax, ancestry, wsigs):
    for child in scope['children']:
        if child['type']['name'] == 'wire':
            wsigs.append(_create_wsig(child, timestep, tmax, ancestry))
        elif child['type']['name'] == 'struct':
            _process_scope(child, timestep, tmax,
                          ancestry+[child['name']], wsigs)


def _render_vcd(fname):
    with open(fname) as f:
        vcd = VcdParser()
        vcd.parse(f)
        data = vcd.scope.toJson()
        f.seek(0)
        timestep = _find_timestep(f)
        f.seek(0)
        tmax = _max_time(f)
    wsignals = []
    _process_scope(data, timestep, tmax, [data['name']], wsignals)
    return wavedrom.render(json.dumps(
        {
            'signal': wsignals,
            'head': {
                'text': 'Counterexample'
            },
        }
    ))


class Result(Enum):
    PASS = 0
    ERROR = 1
    FAIL = 2

@dataclass
class BMC_Result:
    result: Result
    stdout: str
    drawing: svgwrite.drawing.Drawing

def check(nmigen_module, ports):
    with TemporaryDirectory() as tmpdirname:
        temp_path = pathlib.Path(tmpdirname)
        with open(temp_path / 'out.il', 'w') as f:
            f.write(rtlil.convert(nmigen_module, ports=ports))
        sby_data = f'''
[options]
mode bmc

[engines]
smtbmc z3

[script]
read_ilang out.il
prep -top top

[files]
{temp_path/'out.il'}'''
        with open(temp_path/'out.sby', 'w') as f:
            f.write(sby_data)
        yosys_path = shutil.which('yowasp-yosys')
        smt_path = shutil.which('yowasp-yosys-smtbmc')
        process = subprocess.run([
            'yowasp-sby',
            '-f',
            '-d', temp_path / 'work',
            '--yosys', yosys_path,
            '--smtbmc', smt_path,
            temp_path/'out.sby'], stdout=subprocess.PIPE)
        if process.returncode in [0, 2]:
            result = Result(process.returncode)
            return BMC_Result(result, process.stdout, None if result == Result.PASS else _render_vcd(temp_path / 'work/engine_0/trace.vcd'))
        else:
            return BMC_Result(Result.ERROR, process.stdout, None)
