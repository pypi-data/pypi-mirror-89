import gpustat as gp
import time, os
import subprocess as sp
import sys
import importlib.util

def monitor():
    c = gp.new_query()
    processes_per_gpu = [ len(x['processes']) for x in  c.jsonify()['gpus']]
    return processes_per_gpu

def submit(job_text):
    # TODO: check correct env, but NOT part of the job_text
    # TODO: don't submit again after run once.
    tar_file = [ f for f in job_text.split(' ') if '.py' in f]
    torch = importlib.util.find_spec('torch') is not None
    assert len(tar_file)==1

    while True:
        ppgpu = monitor()
        if sum(ppgpu)>1:
            print(f'Still busy. File {tar_file[0]} is in local: {tar_file[0] in os.listdir()}. \
            Torch present {torch}.')
        else:
            print('Done, submitting a new job!')
            # my_env = os.environ.copy()
            sp.run(job_text)
            time.sleep(120)
            sys.exit(0)
        time.sleep(1)

