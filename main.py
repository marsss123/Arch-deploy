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
    #make the program chroot /mnt and continue the installation
    PostBaseInstall.chroot()

if __name__ == "__main__":
    main()


