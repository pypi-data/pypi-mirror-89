import sys
import subprocess

PIPE = subprocess.PIPE
STDOUT = subprocess.STDOUT
DEVNULL = subprocess.DEVNULL

def run(*args, exit_code=True, multi_command=False, **kwargs):
    if multi_command and (isinstance(args[0], tuple) or isinstance(args[0], list)):
        rets = []
        for arg in args[0]:
            rets.append(command(arg, exit_code, **kwargs))
        return rets
    else:
        return command(*args, exit_code, **kwargs)

def command(*args, exit_code=False, print_out=True, print_err=True, **kwargs):
    if 'shell' not in kwargs:
        kwargs['shell'] = True
    if 'encoding' not in kwargs:
        kwargs['encoding'] = 'utf-8'

    ret = subprocess.run(*args, executable="/bin/bash", **kwargs)
    
    if print_out and ret.stdout is not None and len(ret.stdout) > 0:
        print(ret.stdout)
    if print_err and ret.stderr is not None and len(ret.stderr) > 0:
        print(ret.stderr)
    if exit_code and ret.returncode != 0:
        sys.exit(ret.returncode)
    return ret
