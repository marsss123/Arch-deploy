import os 

from disks import DISKTOINSTALL
from baseinstall import ArchInstall
from Postbase import PostBaseInstall

class main():
    #DISK PARTITIONING
    DISKTOINSTALL()
    DISKTOINSTALL.get_disks()
    DISKTOINSTALL.choose_disk()
    DISKTOINSTALL.make_partitions()
    
    #BASE INSTALL
    ArchInstall()
    ArchInstall.choose_kernel()
    ArchInstall.base_system()
    ArchInstall.choose_bootloader()
    ArchInstall.networkmanager()
    #POST BASE INSTALL
    PostBaseInstall()
    PostBaseInstall.add_user()
    PostBaseInstall.PacmanInst()
    PostBaseInstall.installAur()
    PostBaseInstall.installAurPackages()
    PostBaseInstall.installDotFiles()
    PostBaseInstall.installGTK()
    PostBaseInstall.installIcons()

if __name__ == "__main__":
    main()


