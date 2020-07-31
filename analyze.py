#!/usr/bin/env python3
# Print mean/min/max/error statistics for a directory of fio json output files

import sys
import os
import json

class Result:
    def __init__(self, samples):
        self.samples = samples
        self.min = min(samples)
        self.max = max(samples)
        self.mean = sum(samples) / len(samples)
        self.error = (self.max - self.min) / self.mean / 2 * 100

def process_iops(json_path, rw):
    obj = json.load(open(json_path, 'rt'))
    return sum(j.get(rw, {'iops', 0}).get('iops', 0) for j in obj.get('jobs', [{}]))

def process_run(run_dir):
    '''Return a Result for a run'''
    samples = [process_iops(os.path.join(run_dir, d), 'read') for d in os.listdir(run_dir)]
    return Result(samples)

def process_runs(runs_dir):
    '''Return a dict of Results'''
    runs = {}
    for name in os.listdir(runs_dir):
        run_dir = os.path.join(runs_dir, name)
        runs[name] = process_run(run_dir)
    return runs

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write('usage: {0} <runs-dir>\n'.format(sys.argv[0]))
        sys.exit(1)

    runs_dir = sys.argv[1]
    runs_data = process_runs(runs_dir)

    print('{:<30} {:>12}   {}'.format('Name', 'IOPS', 'Error'))
    for name, result in sorted(runs_data.items(), key=lambda x: x[0]):
        print('{:<30} {:>12.2f} ± {:.2f}%'.format(name, result.mean, result.error))
