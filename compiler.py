import os,sys,subprocess
from subprocess import PIPE
def compile_it(code,inp):
    os.open('./output/Try.c',os.O_CREAT)
    fd = os.open('./output/Try.c',os.O_WRONLY)
    code = code.encode()
    os.truncate(fd,0)
    os.write(fd,code)
    os.close(fd)
    # sr0 = subprocess.run('cd output',stdout = PIPE,shell = True)
    sr1= subprocess.run('gcc ./output/Try.c',stdout = PIPE,shell = True)
    sr2 = subprocess.run('a.exe',input = inp.encode(),stdout = PIPE,shell = True)
    sr3 = subprocess.run('rm a.exe',stdout = PIPE,shell = True)
    return sr2.stdout.decode('utf-8')