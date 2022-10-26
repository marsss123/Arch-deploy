import os 
import subprocess
from disks import DISKTOINSTALL

class ArchInstall:

    #ask what kernel the user prefers and save it to a variable as str 
    def choose_kernel():
        print("Choose a kernel: ")
        print("1: linux")
        print("2: linux-lts")
        kernel = input("Kernel: ")
        if kernel == "1":
            return " linux  linux-headers"
        elif kernel == "2":
            return " linux-lts linux-lts-headers"
        else:
            print("Invalid answer")
            ArchInstall.choose_kernel()
        return kernel
        
    #install the base system
    def base_system():
        kernel = ArchInstall.choose_kernel()
        #update pacman keys 
        os.system('pacman -Sy --noconfirm archlinux-keyring')
        #update pacman
        os.system('pacman-keys --init')
        #install base system
        print("Installing base system")
        os.system('pacstrap /mnt base base-devel linux-firmware base-devel vim networkmanager' + kernel )
        #create fstab
        os.system('genfstab -U /mnt >> /mnt/etc/fstab')
        
        