import gpustat as gp

def monitor():
    c = gp.new_query()
    processes_per_gpu = [ len(x['processes']) for x in  c.jsonify()['gpus']]
    return processes_per_gpu

def submit(job):
    while True:
        ppgpu = monitor()
        if sum(ppgpu)>1:
            print('Still busy.')
