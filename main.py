import os 
import subprocess
from disks import DISKTOINSTALL
from baseinstall import ArchInstall
from Postbase import PostBaseInstall

class main():
    #DISK PARTITIONING
    DISKTOINSTALL()
    DISKTOINSTALL.make_partitions()
    
    #BASE INSTALL
    ArchInstall()
    ArchInstall.base_system()
    #POST BASE INSTALL
    PostBaseInstall()
    #chroot
    subprocess.check_call(f"/usr/bin/arch-chroot /mnt", shell=True)
    PostBaseInstall.add_user()
    PostBaseInstall.PacmanInst()
    PostBaseInstall.installAur()
    PostBaseInstall.installAurPackages()
    PostBaseInstall.installDotFiles()
    PostBaseInstall.installGTK()
    PostBaseInstall.installIcons()

if __name__ == "__main__":
    main()


