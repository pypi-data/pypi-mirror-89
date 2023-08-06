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

# todo: 无效的，子进程内 source，不会作用于父进程。
def source(file=None):
    if file is not None and isinstance(file, str) and len(file) > 0:
        return command("source %s" % file)
    else:
        sf = source_file.get(shell)
        if sf is not None:
            return command("source %s" % sf)
        else:
            return None

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
        lines = f1.readlines()
        start_idx = -1
        end_idx = -1
        for i, line in enumerate(lines):
            if flag == 0 and start in line:
                flag = 1
                start_idx = i
            elif flag == 1 and end in line: #已存在，修改
                flag = 2
                end_idx = i
                break

        if flag == 0: #不存在，新增
            new_lines = []
            lines.reverse()
            first_none = True
            for line in lines:
                if first_none:
                    if line != '\n':
                        first_none = False
                        new_lines.append(line)
                else:
                    new_lines.append(line)
            new_lines.reverse()
            f2.writelines(new_lines + ['\n'] + conf)
        elif flag == 2:
            new_lines1 = []
            lines1 = lines[:start_idx]
            lines1.reverse()
            first_none = True
            for line in lines1:
                if first_none:
                    if line != '\n':
                        first_none = False
                        new_lines1.append(line)
                else:
                    new_lines1.append(line)
            new_lines1.reverse()

            new_lines2 = []
            lines2 = lines[end_idx+1:]
            first_none = True
            for line in lines2:
                if first_none:
                    if line != '\n':
                        first_none = False
                        new_lines2.append(line)
                else:
                    new_lines2.append(line)
            
            f2.writelines(new_lines1 + ['\n'] + conf + ['\n'] + new_lines2)
        elif flag == 1:
            raise("env file syntax error, missing end. %s" % env_file_path)
        
    _os.remove(env_file_path)
    _os.rename(temp_file, env_file_path)
    # source()
    return True

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
        lines = f1.readlines()
        start_idx = -1
        end_idx = -1
        for i, line in enumerate(lines):
            if flag == 0 and start in line:
                flag = 1
                start_idx = i
            elif flag == 1 and end in line: #已存在，删除
                flag = 2
                end_idx = i
                break
        
        if flag == 1:
            raise("env file syntax error, missing end. %s" % env_file_path)
        elif flag == 0: #不存在，退出
            return True

        new_lines1 = []
        lines1 = lines[:start_idx]
        lines1.reverse()
        first_none = True
        for line in lines1:
            if first_none:
                if line != '\n':
                    first_none = False
                    new_lines1.append(line)
            else:
                new_lines1.append(line)
        new_lines1.reverse()

        new_lines2 = []
        lines2 = lines[end_idx+1:]
        first_none = True
        for line in lines2:
            if first_none:
                if line != '\n':
                    first_none = False
                    new_lines2.append(line)
            else:
                new_lines2.append(line)
        
        f2.writelines(new_lines1 + ['\n'] + new_lines2)
    
    _os.remove(env_file_path)
    _os.rename(temp_file, env_file_path)
    # source()
    return True
