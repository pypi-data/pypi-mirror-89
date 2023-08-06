import os as _os
import platform

from lonely.cmd import command

def lsb_release():
    ret = command("cat /etc/openEuler-release", capture_output=True, print_out=False, print_err=False)
    if ret.returncode == 0:
        #print("success:", ret)
        if ret.stdout.lower().find("openeuler") > -1:
            return "openeuler"
        else:
            return "unknown"
    else:
        #print("failure:", ret)
        return "unknown"

os = platform.system().lower()
arch = platform.machine().lower()
release = lsb_release()

shell = _os.getenv('SHELL')
home = _os.getenv('HOME')

base = "/usr/local"
temp = "/tmp"

env_file = {
    "linux": "%s/.bashrc" % home,
    "darwin": "%s/.bash_profile" % home,
}
source_file = {
    "/bin/bash": env_file.get(os),
    "/bin/zsh": "%s/.zshrc" % home,
}

def source(file=None):
    if file is not None and isinstance(file, str) and len(file) > 0:
        return command("source %s" % file)
    else:
        sf = source_file.get(shell)
        if sf is not None:
            return command("source %s" % sf)
        else:
            return None

# todo: 优化空行间隔
def env_add(conf):
    if conf is None or type(conf) not in (type(()), type([])) or len(conf) < 2:
        return False
    
    if os not in env_file:
        print("Unsupported os: %s" % os)
        return False

    env_file_path = env_file[os]
    temp_file = env_file_path + ".tmp"
    start = conf[0]
    end = conf[len(conf)-1]
    flag = 0

    with open(env_file_path, "r", encoding="utf-8") as f1, open(temp_file, "w", encoding="utf-8") as f2:
        for line in f1:
            if flag == 0 and start in line:
                flag = 1
                continue
            if flag == 1 and end in line:
                flag = 2
                f2.write("\n")
                f2.writelines(conf)
                f2.write("\n")
                continue
            if flag in (0, 2):
                f2.write(line)
        if flag == 0:
            f2.write("\n")
            f2.writelines(conf)
            f2.write("\n")
        elif flag == 1:
            raise("env file syntax error, missing end. %s" % env_file_path)
        
    _os.remove(env_file_path)
    _os.rename(temp_file, env_file_path)
    command("source %s" % env_file_path)
    return True

# todo: 优化空行间隔
def env_del(conf):
    if conf is None or type(conf) not in (type(()), type([])) or len(conf) < 2:
        return False
    
    if os not in env_file:
        print("Unsupported os: %s" % os)
        return False

    env_file_path = env_file[os]
    temp_file = env_file_path + ".tmp"
    start = conf[0]
    end = conf[len(conf)-1]
    flag = 0

    with open(env_file_path, "r", encoding="utf-8") as f1, open(temp_file, "w", encoding="utf-8") as f2:
        for line in f1:
            if flag == 0 and start in line:
                flag = 1
                continue
            if flag == 1 and end in line:
                flag = 2
                continue
            if flag in (0, 2):
                f2.write(line)
        if flag == 1:
            raise("env file syntax error, missing end. %s" % env_file_path)
        
    _os.remove(env_file_path)
    _os.rename(temp_file, env_file_path)
    command("source %s" % env_file_path)
    return True
