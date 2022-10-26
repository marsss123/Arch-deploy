import subprocess
import os
from disks import DISKTOINSTALL
class PostBaseInstall:
    
    #this function is for chrooting into /mnt and continiu the installation
    def chroot():
        os.chdir('/mnt')
        os.system('mount -t proc /proc proc/')
        os.system('mount --rbind /sys sys/')
        os.system('mount --rbind /dev dev/')
        os.system('mount --rbind /run run/')
        os.system('cp /etc/resolv.conf /mnt/etc/resolv.conf')
        os.system('chroot /mnt /bin/bash -c "python3 /Postbase.py"') 
        PostBaseInstall.add_user()
        PostBaseInstall.choose_bootloader()
        PostBaseInstall.networkmanager()
        PostBaseInstall.PacmanInst()
        PostBaseInstall.installAur()
        PostBaseInstall.installAurPackages()
        PostBaseInstall.installDotFiles()
        PostBaseInstall.installGTK()
        PostBaseInstall.installIcons()
        os.system('exit')
    #add user
    def add_user():
        print("Enter username: ")
        username = input("Username: ")
        os.system('useradd -m' + username)
        os.system('passwd'+ username)
        os.system('usermod -aG wheel,audio,video,optical,storage' + username)
        #enable sudo on wheel group
        os.system('sed -i'+ "'s/# %wheel ALL=(ALL) ALL/%wheel ALL=(ALL) ALL/g'"+ '/etc/sudoers')
        os.system('ln -sf /usr/share/zoneinfo/Europe/Athens /etc/localtime')
        #set hardware clock
        os.system('hwclock --systohc')
        #set locale
        print("Choose a locale: ") 
        os.system('ls /etc/locale.gen')
        locale = input("Locale: ")
        os.system('sed -i' + "'s/#" + locale + "/" + locale + "/g'" + '/etc/locale.gen')
        os.system('locale-gen')
        os.system('echo LANG=' + locale + '> /etc/locale.conf')
        #set hostname
        print("Enter hostname: ")
        hostname = input("Hostname: ")
        os.system('echo' + hostname + '> /etc/hostname')
        #set basik hosts
        os.system('echo 127.0.0.1 \t localhost > /etc/hosts')
        os.system('echo ::1 \t localhost >> /etc/hosts')
        os.system('echo 127.0.1.1 \t' + hostname + '.localdomain \t' + hostname + '>> /etc/hosts')
        #set root password
        print("Enter root password: ")
        os.system('passwd')

    def choose_bootloader():
        print("Choose a bootloader: ")
        print("1: grub")
        print("2: systemd-boot")
        bootloader = input("Bootloader: ")
        if bootloader == "1":
            PostBaseInstall.grub()
        elif bootloader == "2":
            PostBaseInstall.systemd_boot()
        else:
            print("Invalid answer")
            PostBaseInstall.choose_bootloader()
        
    #install grub
    def grub():
        disk = DISKTOINSTALL.choose_disk()
        disk_name = disk[:-1]
        os.system('pacman -S grub efibootmgr os-prober dosfstools mtools')
        os.system('mkdir /boot/EFI')
        os.system('mount' + disk_name + '1 /boot/EFI')
        os.system('grub-install --target=x86_64-efi --bootloader-id=GRUB --efi-directory=/boot/EFI')
        os.system('grub-mkconfig -o /boot/grub/grub.cfg')
        
    #install systemd-boot
    def systemd_boot():
        disk = DISKTOINSTALL.choose_disk()
        disk_name = disk[:-1]
        os.system('bootctl --path=/boot install')
        os.system('echo default arch > /boot/loader/loader.conf')
        os.system('echo timeout 4 >> /boot/loader/loader.conf')
        os.system('echo editor 0 >> /boot/loader/loader.conf')
        os.system('echo title Arch Linux > /boot/loader/entries/arch.conf')
        os.system('echo linux /vmlinuz-linux >> /boot/loader/entries/arch.conf')
        os.system('echo initrd /initramfs-linux.img >> /boot/loader/entries/arch.conf')
        os.system('echo options root=' + disk_name + '2 rw >> /boot/loader/entries/arch.conf')
    
    #install networkmanager
    def networkmanager():
        os.system('pacman -S networkmanager')
        os.system('systemctl enable NetworkManager')

    def PacmanInst():
        #install 
        PKGS='zip zsh zsh-completions wget unrar unzip bashtop hardinfo neofetch numlockx xfce4-power-manager xfce4-appfinder rofi xorg-fonts-type1 ttf-liberation ttf-dejavu ttf-bitstream-vera sdl_ttf gsfonts font-bh-ttf autofs exfat-utils ntfs-3g terminator catfish nemo variety feh network-manager-applet xfce4-settings-manager scrot xfce4-screenshooter lxappearance gst-plugins-base gst-plugins-good gst-plugins-ugly gst-plugins-bad gst-libav obs-studio git vlc xfce4-screenshooter xpdf vim i3-gaps sddm'
        os.system('pacman', '-S', PKGS)          
        os.system('systemctl enable sddm')
        os.system('systemctl enable autofs')

    def installAur():
        #do you want a aur helper
        print("Do you want to install a aur helper?")
        print("1: yay")
        print("2: trizen")
        print("3: paru")
        print("4 no")
        aurhelper = input("Aur helper: ")
        if aurhelper == "1":
            PostBaseInstall.yay()
        elif aurhelper == "2":
            PostBaseInstall.trizen()
        elif aurhelper == "3":
            PostBaseInstall.paru()
        elif aurhelper == "4":
            print("Ok")

    def yay():
        #install yay
        username = PostBaseInstall.add_user()
        os.system('su' + username)
        os.system('git clone https://aur.archlinux.org/yay.git')
        os.chdir('yay')
        os.system('makepkg -si')
        os.system('pacman -U yay*')
        os.chdir('..')
        os.system('rm -rf yay')
        os.system('exit')
    
    def trizen():
        #install trizen
        username = PostBaseInstall.add_user()
        os.system('su' + username)
        os.system('git clone https://aur.archlinux.org/trizen.git')
        os.chdir('trizen')
        os.system('makepkg -si')
        os.system('pacman -U trizen*')
        os.chdir('..')
        os.system('rm -rf trizen')
        os.system('exit')
    
    def paru():
        #install paru
        username = PostBaseInstall.add_user()
        os.system('su' + username)
        os.system('git clone https://aur.archlinux.org/paru.git')
        os.chdir('paru')
        os.system('makepkg -si')
        os.system('pacman -U paru*')
        os.chdir('..')
        os.system('rm -rf paru')
        os.system('exit')

    def installAurPackages():
        PKGS1='visual-studio-code-bin  spotify  discord  telegram-desktop  zoom  google-chrome  polybar  networkmanager-dmenu-git  arc-gtk-theme  arc-icon-theme''papirus-icon-theme  papirus-folders  papirus-maia-icon-theme  papirus-maia-folders  papirus-maia-git  papirus-maia-icon-theme-git  nerd-fonts-iosevka  ttf-icomoon-feather  ttf-material-icons-git  siji-git  ttf-font-awesome  ttf-joypixels  ttf-nerd-fonts-symbols  ttf-ms-fonts'
        aur_helper = PostBaseInstall.installAur()
        if aur_helper == "yay":
            os.system('yay -S' + PKGS1)
        elif aur_helper == "trizen":
            os.system('trizen -S' + PKGS1)
        elif aur_helper == "paru":
            os.system('paru -S' + PKGS1)
        elif aur_helper == "no":
            print("Ok")

    def installDotFiles():
        #install dotfiles
        username = PostBaseInstall.add_user()
        os.system('su', username)
        os.system('git clone --depth=1 https://github.com/adi1090x/polybar-themes.git')
        os.chdir('dotfiles')
        os.system('mv config ~/.config/i3/config')
        #installing polybar themes from github
        os.system('git clone https://github.com/adi1090x/polybar-themes.git')
        os.chdir('polybar-themes')
        os.system('chmod +x setup.sh')
        os.system('./setup.sh')
        os.chdir('..')
        os.system('rm -r polybar-themes')
        #install oh-my-zsh plugins
        os.system('git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions')
        os.system('git clone --depth https://github.com/marlonrichert/zsh-autocomplete.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autocomplete')
        os.system('git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k')
        #add plugins to .zshrc
        os.system('sed -i' + "'s/plugins=(git)/plugins=(git zsh-autosuggestions)/g'" + '~/.zshrc')
        os.system('sed -i' + "'s/plugins=(git)/plugins=(git zsh-autocomplete)/g'" + '~/.zshrc')
        os.system('sed -i' + "'s/ZSH_THEME=\"robbyrussell\"/ZSH_THEME=\"powerlevel10k\/powerlevel10k\"/g'" + '~/.zshrc')
        os.system('exit')

    def installGTK():
        #install nordic gtk theme
        username = PostBaseInstall.add_user()
        os.system('su' + username)
        os.system('wget https://github.com/EliverLara/Nordic-Polar/releases/download/v1.9.0/Nordic-Polar-standard-buttons.tar.xz')
        os.system('tar -xf Nordic-Polar-standard-buttons.tar.xz -C ~/.themes/')
        os.system('gsettings set org.gnome.desktop.interface gtk-theme "Nordic-Polar"')
        os.system('gsettings set org.gnome.desktop.wm.preferences theme "Nordic-Polar"')
        os.system('rm Nordic-Polar-standard-buttons.tar.xz')
        os.system('exit')
    
    def installIcons():
        #install nordic icons
        username = PostBaseInstall.add_user()
        os.system('su' + username)
        os.system('wget https://github.com/EliverLara/Nordic/releases/download/v2.2.0/Nordic-darker.tar.xz')
        os.system('tar -xf Nordic-darker.tar.xz -C ~/.icons/')
        os.system('gsettings set org.gnome.desktop.interface icon-theme "Nordic-darker"')
        os.system('rm Nordic-darker.tar.xz')
        os.system('exit')