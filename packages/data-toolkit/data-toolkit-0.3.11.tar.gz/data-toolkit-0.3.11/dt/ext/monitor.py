import gpustat as gp
import time, os
import subprocess as sp

def monitor():
    c = gp.new_query()
    processes_per_gpu = [ len(x['processes']) for x in  c.jsonify()['gpus']]
    return processes_per_gpu

def submit(job_text):
    tar_file = job_text.split(' ')[2]

    while True:
        ppgpu = monitor()
        if sum(ppgpu)>1:
            print(f'Still busy. File {tar_file} is in local: {tar_file in os.listdir()}.')
        else:
            print('Done, submitting a new job!')
            sp.run(job_text, shell=True)
            time.sleep(120)
        time.sleep(1)

