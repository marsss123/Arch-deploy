import os
import subprocess
import sys

class main:
    def __init__(self, disk):
        self.disk = disk

    def archinstalldisk(self):
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
            print("invalid option")
            exit()
        print("making filesystems")
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
            print("invalid option")
            exit()
        
        def mountparts():
            print("mounting root")
            os.system("mount /dev/" + getdisk + "2 /mnt")
            print("mounting boot")
            os.system("mkdir /mnt/boot")
            os.system("mount /dev/" + getdisk + "1 /mnt/boot")

        def archinstall():
            print("installing arch")
            os.system("pacstrap /mnt base linux linux-firmware")
            print("generating fstab")
            os.system('pacstrap', '/mnt', 'base' , 'linux', 'linux-firmware' , 'linux-headers','base-devel','vim','networkmanager')
            print("chrooting")
            os.system("arch-chroot /mnt")
            print("setting up system")
            print("please enter a hostname")
            gethostname=input()
            os.system("echo " + gethostname + " > /etc/hostname")
            print("setting up time")
            os.system("ln -sf /usr/share/zoneinfo/America/New_York /etc/localtime")
            os.system("hwclock --systohc")
            print("setting up locale")
            os.system("sed -i 's/#en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen")
            os.system("locale-gen")
            os.system("echo LANG=en_US.UTF-8 > /etc/locale.conf")
            print("setting up keyboard")
            os.system("echo KEYMAP=us > /etc/vconsole.conf")
            print("setting up network")
            os.system("systemctl enable NetworkManager")
            print("making initramfs")
            os.system("mkinitcpio -P")
            print("setting up root password")
            os.system("passwd")
            print("setting up bootloader")
            os.system("pacman -S grub efibootmgr os-prober")
            os.system("grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB")
            os.system("grub-mkconfig -o /boot/grub/grub.cfg")
            print("base install complete")
        def postinstall():
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
            
            
            print("do you want to enable multilib?")
            getmultilib=input()
            if getmultilib == "y":
                os.system("echo [multilib] >> /etc/pacman.conf")
                os.system("echo Include = /etc/pacman.d/mirrorlist >> /etc/pacman.conf")
            else:
                print("continuing")

            PKGS=[
            'zip'                    
            'zsh'                   
            'zsh-completions'        
            'wget'                   
            'unrar'                  
            'unzip'                  
            'bashtop'               
            'hardinfo'               
            'neofetch'               
            'numlockx'              
            'xfce4-power-manager'
	        'xfce4-appfinder'
	        'rofi'
            'xorg-fonts-type1'
	        'ttf-liberation'
	        'ttf-dejavu'
            'ttf-bitstream-vera'
            'sdl_ttf'
            'gsfonts'
            'font-bh-ttf'
            'autofs'                
            'exfat-utils'                          
            'ntfs-3g'               
            'terminator'
            'catfish'               
            'nemo'                  
            'variety'               
            'feh'
	        'network-manager-applet'
	        'xfce4-settings-manager'
	        'scrot'
	        'xfce4-screenshooter'
            'lxappearance'
            'gst-plugins-base'
            'gst-plugins-good'
            'gst-plugins-ugly'
            'gst-plugins-bad'
            'gst-libav'
            'obs-studio'               
            'git'                   
            'vlc'                   
            'xfce4-screenshooter'                   
            'xpdf'                  
            'vim'   
            'i3-gaps'
            'sddm'


            ]

            os.system("pacman -Syu --noconfirm ",PKGS)  
            print("enabling sddm")
            os.system("systemctl enable sddm")  
            print("do you want to install a aur helper?")
            getaur=input()
            if getaur == "y":
                os.system("su " + getusername)
                os.system("cd /home/" + getusername)
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
            PKGS1=[

	        'visual-studio-code-bin'    
	        'spotify'                   
            'discord'
            'telegram-desktop'
            'zoom'
	        'google-chrome'	    
	        'polybar'
	        'networkmanager-dmenu-git'
            'arc-gtk-theme'
            'arc-icon-theme'
            'papirus-icon-theme'
            'papirus-folders'
            'papirus-maia-icon-theme'
            'papirus-maia-folders'
            'papirus-maia-git'
            'papirus-maia-icon-theme-git'
            'nerd-fonts-iosevka'
            'ttf-icomoon-feather'
            'ttf-material-icons-git'
            'siji-git'
            'ttf-font-awesome'
            'ttf-joypixels'
            'ttf-nerd-fonts-symbols'
            'ttf-ms-fonts'
            ]
            print("installing aur packages and themes")
            os.system(getaur + " -S --noconfirm " + PKGS1)
            os.system("exit")
            print("are you a hacker ?")
            gethacker=input()
            if gethacker == "y":
                print("do you want to install blackarch?")
                getblackarch=input()
                if getblackarch == "y":
                    os.system("curl -O https://blackarch.org/strap.sh")
                    os.system("chmod +x strap.sh")
                    os.system("./strap.sh")
                    os.system("pacman -Syu ")
                    print("blackarch repository added")
                    print("do you want to install black arch packages now ?")
                    getblackarch1=input()
                    if getblackarch1 == "y":
                        os.system("pacman -S blackarch")
                        print("blackarch packages installed")
                    else:
                        print("ok")


    print("tank you for using my script")
    print("exiting")
    os.system("exit")
    os.system("umount -R /mnt")
    os.system("reboot")


if __name__ == "__main__":
    main()