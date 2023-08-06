import os, sys
import shutil

from lonely import cmd, system
from lonely.core import lonely

class Go(object):
    def __init__(self):
        self.oss = ("linux", "darwin")
        self.archs = {"x86_64":"amd64", "aarch64":"arm64"}
        self.home = "%s/go" % lonely.home
        self.conf = [
            "# start:lonely:go\n",
            "export GOROOT=%s/go\n" % lonely.home,
            "export GOPATH=%s/.go\n" % system.home,
            "export GOBIN=$GOPATH/bin\n",
            "export PATH=$PATH:$GOROOT/bin\n",
            "export PATH=$PATH:$GOPATH/bin\n",
            "export GOPROXY=https://goproxy.cn,direct\n",
            "#export GOPROXY=https://goproxy.io,direct #spare-备用\n",
            "# end:lonely:go\n",
        ]
    
    def check(self):
        if system.os not in self.oss:
            print("Unsupported os: %s" % system.os)
            sys.exit(1)
        if system.arch not in self.archs:
            print("Unsupported arch: %s" % system.arch)
            sys.exit(1)

    def install(self):
        self.check()
        if cmd.command("go version", stderr=cmd.DEVNULL).returncode == 0:
            print("go has been installed, please delete it first.")
            sys.exit(1)

        version = "1.15.6"
        go_file_name = "go%s.%s-%s.tar.gz" % (version, system.os, self.archs[system.arch])
        go_file = system.temp + "/" + go_file_name
        url = "https://golang.google.cn/dl/" + go_file_name

        lonely.mkdir()
        cmd.run([
            "wget -O %s %s" % (go_file, url),
            "tar -C %s -xzf %s" % (lonely.home, go_file),
        ], multi_command=True)
        self.env_add()
    
    def update(self):
        self.check()
        lonely.access()
        if not os.path.exists(self.home):
            print("Directory does not exist:1 %s" % self.home)
        shutil.rmtree(self.home, ignore_errors=True)
        self.install()

    def remove(self):
        self.check()
        lonely.access()
        if not os.path.exists(self.home):
            print("Directory does not exist: %s" % self.home)
        shutil.rmtree(self.home, ignore_errors=True)
        self.env_del()
        
    def env_add(self):
        if not system.env_add(self.conf):
            sys.exit(1)
        
    def env_del(self):
        if not system.env_del(self.conf):
            sys.exit(1)
