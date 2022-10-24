import os
import sys   

def archinstalldisk():
    # Get the disk to install to
    print(os.system("lsblk"))
    print("Please enter the disk you want to install to")
    getdisk=input()
    print("You have selected", getdisk)
    print("Is this correct? (y/n)")
    getdiskconfirm=input()
    if getdiskconfirm == "y":
        print("Continuing...")
    else:  
        print("Please restart the installer")
        exit()
    print("making partitions")
    print("do you want a swap space")
    getswap=input()
    if getswap == "y":
        print("making swap")
        os.system("mkswap /dev/" + getdisk + "2")
        os.system("swapon /dev/" + getdisk + "2")
    else:
        print("continuing")
    print("making root and boot partitions")

    os.system("parted -s /dev/" + getdisk + " mklabel gpt")
    os.system("parted -s /dev/" + getdisk + " mkpart primary fat32 1MiB 513MiB")
    os.system("parted -s /dev/" + getdisk + " set 1 esp on")
    print("please seleft file system for root partition")
    print("1.ext4")
    print("2.btrfs")
    print("3.xfs")
    print("4.f2fs")
    print("5.jfs")
    print("6.reiserfs")
    print("7.ntfs")
    print("8.exfat")
    print("9.fat32")
    getrootfs=input()
    if getrootfs == "1":
        os.system("parted -s /dev/" + getdisk + " mkpart primary ext4 513MiB 100%")
    elif getrootfs == "2":
        os.system("parted -s /dev/" + getdisk + " mkpart primary btrfs 513MiB 100%")
    elif getrootfs == "3":
        os.system("parted -s /dev/" + getdisk + " mkpart primary xfs 513MiB 100%")
    elif getrootfs == "4":
        os.system("parted -s /dev/" + getdisk + " mkpart primary f2fs 513MiB 100%")
    elif getrootfs == "5":
        os.system("parted -s /dev/" + getdisk + " mkpart primary jfs 513MiB 100%")
    elif getrootfs == "6":
        os.system("parted -s /dev/" + getdisk + " mkpart primary reiserfs 513MiB 100%")
    elif getrootfs == "7":
        os.system("parted -s /dev/" + getdisk + " mkpart primary ntfs 513MiB 100%")
    elif getrootfs == "8":
        os.system("parted -s /dev/" + getdisk + " mkpart primary exfat 513MiB 100%")
    elif getrootfs == "9":
        os.system("parted -s /dev/" + getdisk + " mkpart primary fat32 513MiB 100%")
    else:
        print("invalid input")
        exit()
    print("formatting partitions")
    os.system("mkfs.fat -F32 /dev/" + getdisk + "1")
    if getrootfs == "1":
        os.system("mkfs.ext4 /dev/" + getdisk + "2")
    elif getrootfs == "2":
        os.system("mkfs.btrfs /dev/" + getdisk + "2")
    elif getrootfs == "3":
        os.system("mkfs.xfs /dev/" + getdisk + "2")
    elif getrootfs == "4":
        os.system("mkfs.f2fs /dev/" + getdisk + "2")
    elif getrootfs == "5":
        os.system("mkfs.jfs /dev/" + getdisk + "2")
    elif getrootfs == "6":
        os.system("mkfs.reiserfs /dev/" + getdisk + "2")
    elif getrootfs == "7":
        os.system("mkfs.ntfs /dev/" + getdisk + "2")
    elif getrootfs == "8":
        os.system("mkfs.exfat /dev/" + getdisk + "2")
    elif getrootfs == "9":
        os.system("mkfs.fat -F32 /dev/" + getdisk + "2")
    else:
        print("invalid input")
        exit()
    print("mounting partitions")
    os.system("mount /dev/" + getdisk + "2 /mnt")
    os.system("mkdir /mnt/boot")
    os.system("mount /dev/" + getdisk + "1 /mnt/boot")
    print("installing base system")
    os.system('pacstrap', '/mnt', 'base' , 'linux', 'linux-firmware' , 'linux-headers','base-devel','vim','networkmanager')
    print("generating fstab")
    os.system("genfstab -U /mnt >> /mnt/etc/fstab")
    print("chrooting into new system")
    os.system("arch-chroot /mnt")
    print("setting up time")
    os.system("ln -sf /usr/share/zoneinfo/Europe/Athens /etc/localtime")
    print("setting up new system")
    print("setting up locale")
    os.system("echo LANG=en_US.UTF-8 > /etc/locale.conf")
    os.system("echo en_US.UTF-8 UTF-8 > /etc/locale.gen")
    os.system("echo en_US ISO-8859-1 >> /etc/locale.gen")
    os.system("locale-gen")
    print("setting up hostname")
    gethostname=input()
    os.system("echo " + gethostname + " > /etc/hostname")
    print("setting up initramfs")
    os.system("mkinitcpio -P")
    print("setting up root password")
    get_password=input()
    os.system("echo root:" + get_password + " | chpasswd")
    print ("do you want to add a user?")
    getuser=input()
    if getuser == "y":
        print("enter username")
        getusername=input()
        os.system("useradd -m -g users -G wheel -s /bin/bash " + getusername)
        print("setting up user password")
        get_password2=input()
        os.system("echo " + getusername + ":" + get_password2 + " | chpasswd")
        print("adding user to sudoers")
        os.system("echo '%wheel ALL=(ALL) ALL' >> /etc/sudoers")
    else:
        print("continuing")
    print("setting up bootloader")
    os.system("pacman -S grub efibootmgr os-prober")
    os.system("grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB")
    os.system("grub-mkconfig -o /boot/grub/grub.cfg")
    print("setting up network")
    os.system("systemctl enable NetworkManager")
    print("do you want to continue with extra post install script?")
    getpost=input()
    if getpost == "y":
        print("continuing")   
    else:
        print("exiting")
        exit()
    os.system("su " + getusername)
    print("do you want to install a desktop environment?")
    getdesktop=input()
    if getdesktop == "y":
        print("please select a desktop environment")
        print("1.kde")
        print("2.gnome")
        print("3.xfce")
        print("4.i3-gaps")
        getdesktop=input()
        if getdesktop == "1":
            os.system("pacman -S plasma-meta")
        elif getdesktop == "2":
            os.system("pacman -S gnome")
        elif getdesktop == "3":
            os.system("pacman -S xfce4")
        elif getdesktop == "4":
            print("flagship")
            os.system("pacman -S i3-gaps")
    else:
        print("ok")
    print("do you want to install a display manager?")
    getdm=input()
    if getdm == "y":
        print("please select a display manager")
        print("1.sddm")
        print("2.gdm")
        print("3.lightdm")
        getdm=input()
        if getdm == "1":
            os.system("pacman -S sddm")
            os.system("systemctl enable sddm")
        elif getdm == "2":
            os.system("pacman -S gdm")
            os.system("systemctl enable gdm")
        elif getdm == "3":
            os.system("pacman -S lightdm")
            os.system("systemctl enable lightdm")
    else:
        print("ok")
    print("do you want to install a aur helper?")
    getaur=input()
    if getaur == "y":
        print("please select a aur helper")
        print("1.yay")
        print("2.pikaur")
        print("3.paru")
        getaur=input()
        if getaur == "1":
            os.system("pacman -S git")
            os.system("git clone https://aur.archlinux.org/yay.git")
            os.system("cd yay")
            os.system("makepkg -si")
        elif getaur == "2":
            os.system("pacman -S git")
            os.system("git clone https://aur.archlinux.org/pikaur.git")
            os.system("cd pikaur")
            os.system("makepkg -si")
        elif getaur == "3":
            os.system("pacman -S git")
            os.system("git clone https://aur.archlinux.org/paru.git")
            os.system("cd paru")
            os.system("makepkg -si")
    else:
        print("ok") 

    print("do you want to install a browser?")
    getbrowser=input()
    if getbrowser == "y":
        print("please select a browser")
        print("1.firefox")
        print("2.google chrome")
        getbrowser=input()
        if getbrowser == "1":
            os.system("pacman -S firefox")
        elif getbrowser == "2":
            os.system(getaur + "-S google-chrome")
    else:
        print("ok")
    print("tank you for using my script")
    print("exiting")
    exit()

    

