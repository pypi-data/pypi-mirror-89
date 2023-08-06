import gpustat as gp
import time, os

def monitor():
    c = gp.new_query()
    processes_per_gpu = [ len(x['processes']) for x in  c.jsonify()['gpus']]
    return processes_per_gpu

def submit(job_text):

    while True:
        ppgpu = monitor()
        if sum(ppgpu)>1:
            print('Still busy.')
        else:
            print('Done, submitting a new job!')
            os.system(job_text)
        time.sleep(1)

