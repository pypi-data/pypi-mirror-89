import sys

from lonely import cmd, system
from lonely.core import lonely

class YumRepo:
    def install(self):
            if system.os != "linux":
                print("Unsupported os: %s" % system.os)
                sys.exit(1)
            
            if system.arch != "x86_64" and system.arch != "aarch64":
                print("Unsupported arch: %s" % system.arch)
                sys.exit(1)
            
            if system.release != "openeuler":
                print("Unsupported release: %s" % system.release)
                sys.exit(1)
            
            url = ""
            if system.arch == "x86_64":
                url = "https://repo.huaweicloud.com/repository/conf/openeuler_x86_64.repo"
            elif system.arch == "aarch64":
                url = "https://repo.huaweicloud.com/repository/conf/openeuler_aarch64.repo"
            
            cmd.run([
                "wget -O /etc/yum.repos.d/openEulerOS.repo %s" % url,
                "yum clean all",
                "yum makecache",
            ], multi_command=True)
