import os 

class DISKTOINSTALL:
    # Get all disks
    def get_disks():
        disks = []
        # strip the output of (fdisk -l) to get the disks
        for line in os.popen("fdisk -l").read().splitlines():
            if "Disk /dev/" in line:
                disks.append(line.split()[1])
            #remove the devices that are not disks
            if "Disk /dev/loop" in line:
                disks.remove(line.split()[1])
            elif "Disk /dev/sr" in line:
                disks.remove(line.split()[1])
            elif "Disk /dev/ram" in line:
              disks.remove(line.split()[1])
            elif "Disk /dev/mapper" in line:
                disks.remove(line.split()[1])
            elif disks == [] :
                print("No disks found")
                exit()
        return disks
       #print(disks)
        print("Disks found: " + str(len(disks)))

    #get disk from the function above and make user choose which disk to install on
    def choose_disk():
        disks = DISKTOINSTALL.get_disks()
        print("Choose a disk to install on: ")
        for i in range(len(disks)):
            print(str(i) + ": " + disks[i])
        disk = disks[int(input("Disk: "))]
        return disk

    #ask user if he wants to make the partitions himself or let the script do it
    def make_partitions():
        print("if you have windows installed on the disk you want to install linux on, you need to make the partitions manually")
        print("else you will lose all your data")
        print("if you have already made partitions, press enter")
        print("Do you want to make the partitions yourself? (y/n)")
        answer = input("Answer: ")
        if answer == "y":
            DISKTOINSTALL.make_partitions_manually()
        elif answer == "n":
            DISKTOINSTALL.make_partitions_automatically()
        else:
            print("Invalid answer")
            DISKTOINSTALL.make_partitions()

    #make partitions manually using cfdisk or fdisk based on user input
    def make_partitions_manually():
        disk = DISKTOINSTALL.choose_disk()
        print("Making partitions manually")
        print("Do you want to use cfdisk or fdisk? (c/f)")
        answer = input("Answer: ")
        if answer == "c":
            os.system("cfdisk " + disk)
        elif answer == "f":
            os.system("fdisk " + disk)
        else:
            print("Invalid answer")
            DISKTOINSTALL.make_partitions_manually()
        
    #make partitions automatically using parted
    def make_partitions_automatically():
        #ask if the user want to user efi or dos
        print("Do you want to use efi or dos? (e/d)")
        answer = input("Answer: ")
        if answer == "e":
            DISKTOINSTALL.make_partitions_automatically_efi()
        elif answer == "d":
            DISKTOINSTALL.make_partitions_automatically_dos()
        else:
            print("Invalid answer")
            DISKTOINSTALL.make_partitions_automatically()

    #make partitions automatically using parted and efi
    def make_partitions_automatically_efi():
        disk = DISKTOINSTALL.choose_disk()
        print("Making partitions automatically with efi")
        #ask for swap size 
        print("Enter swap size in GB")
        print("Swap is a partition that is used as virtual memory")
        swap_size = input("Swap size: ")
        #make the partitions
        os.system("parted " + disk + " mklabel gpt")
        os.system("parted " + disk + " mkpart primary fat32 1MiB 512MiB")
        os.system("parted " + disk + " set 1 esp on")
        os.system("parted " + disk + " mkpart primary ext4 512MiB 100%")
        os.system("parted " + disk + " mkpart primary linux-swap 0 " + swap_size + "G")
        os.system("parted " + disk + " set 3 swap on")
        #format the partitions
        os.system("mkfs.fat -F32 " + disk + "1")
        os.system("mkfs.ext4 " + disk + "2")
        os.system("mkswap " + disk + "3")
        os.system("swapon " + disk + "3")
        #mount the partitions
        os.system("mount " + disk + "2 /mnt")
        os.system("mkdir /mnt/boot")
        os.system("mount " + disk + "1 /mnt/boot")

    #make partitions automatically using parted and dos
    def make_partitions_automatically_dos():
        disk = DISKTOINSTALL.choose_disk()
        print("Making partitions automatically with dos")
        #ask for swap size 
        print("Enter swap size in GB")
        print("Swap is a partition that is used as virtual memory")
        swap_size = input("Swap size: ")
        #make the partitions
        os.system("parted " + disk + " mklabel msdos")
        os.system("parted " + disk + " mkpart primary ext4 1MiB 100%")
        os.system("parted " + disk + " mkpart primary linux-swap 0 " + swap_size + "G")
        os.system("parted " + disk + " set 2 swap on")
        #format the partitions
        os.system("mkfs.ext4 " + disk + "1")
        os.system("mkswap " + disk + "2")
        os.system("swapon " + disk + "2")
        #mount the partitions
        os.system("mount " + disk + "1 /mnt")

class ArchInstall:

    #ask what kernel the user prefers
    def choose_kernel():
        print("Choose a kernel: ")
        print("1: linux")
        print("2: linux-lts")
        print("3: linux-hardened")
        print("4: linux-zen")
        kernel = input("Kernel: ")
        if kernel == "1":
            kernel = "linux"
        elif kernel == "2":
            kernel = "linux-lts"
        elif kernel == "3":
            kernel = "linux-hardened"
        elif kernel == "4":
            kernel = "linux-zen"
        else:
            print("Invalid answer")
            ArchInstall.choose_kernel()
        return kernel

    def headers():
        kernel = ArchInstall.choose_kernel()
        #based on kernel choose kernel headers
        if kernel == "linux":
            kernel_headers = "linux-headers"
        elif kernel == "linux-lts":
            kernel_headers = "linux-lts-headers"
        elif kernel == "linux-hardened":
            kernel_headers = "linux-hardened-headers"
        elif kernel == "linux-zen":
            kernel_headers = "linux-zen-headers"
        return kernel_headers
    
    #install the base system
    def base_system():
        kernel = ArchInstall.choose_kernel()
        kernel_headers = ArchInstall.headers()
        print("Installing base system")
        os.system('pacstrap', '/mnt', 'base' , kernel , 'linux-firmware' ,kernel_headers ,'base-devel','vim','networkmanager')
        #create fstab
        os.system('genfstab', '-U', '/mnt', '>>', '/mnt/etc/fstab')
        #chroot
        os.system('arch-chroot', '/mnt')
        #set timezone based on user input
        print("Choose a timezone: ")
        os.system('ls', '/usr/share/zoneinfo')
        timezone = input("Timezone: ")
        os.system('ln', '-sf', '/usr/share/zoneinfo/' + timezone, '/etc/localtime')
        #set hardware clock
        os.system('hwclock', '--systohc')
        #set locale
        print("Choose a locale: ") 
        os.system('ls', '/etc/locale.gen')
        locale = input("Locale: ")
        os.system('sed', '-i', "'s/#" + locale + "/" + locale + "/g'", '/etc/locale.gen')
        os.system('locale-gen')
        os.system('echo', 'LANG=' + locale, '>', '/etc/locale.conf')
        #set hostname
        print("Enter hostname: ")
        hostname = input("Hostname: ")
        os.system('echo', hostname, '>', '/etc/hostname')
        #set basik hosts
        os.system('echo', '127.0.0.1' + '\t' + 'localhost', '>', '/etc/hosts')
        os.system('echo', '::1' + '\t' + 'localhost', '>>', '/etc/hosts')
        os.system('echo', '127.0.1.1' + '\t' + hostname + '.localdomain' + '\t' + hostname, '>>', '/etc/hosts')
        #set root password
        print("Enter root password: ")
        os.system('passwd')
        #install bootloader
        print("Choose a bootloader: ")
        print("1: grub")
        print("2: systemd-boot")
        bootloader = input("Bootloader: ")
        if bootloader == "1":
            ArchInstall.grub()
        elif bootloader == "2":
            ArchInstall.systemd_boot()
        else:
            print("Invalid answer")
            ArchInstall.bootloader()
        
    #install grub
    def grub():
        disk = DISKTOINSTALL.choose_disk()
        os.system('pacman', '-S', 'grub' , 'efibootmgr', 'os-prober', 'dosfstools', 'mtools')
        os.system('mkdir', '/boot/EFI')
        os.system('mount', disk + '1', '/boot/EFI')
        os.system('grub-install', '--target=x86_64-efi', '--bootloader-id=GRUB', '--efi-directory=/boot/EFI')
        os.system('grub-mkconfig', '-o', '/boot/grub/grub.cfg')
        
    #install systemd-boot
    def systemd_boot():
        disk = DISKTOINSTALL.choose_disk()
        os.system('bootctl', '--path=/boot', 'install')
        os.system('echo', 'default arch', '>', '/boot/loader/loader.conf')
        os.system('echo', 'timeout 4', '>>', '/boot/loader/loader.conf')
        os.system('echo', 'editor 0', '>>', '/boot/loader/loader.conf')
        os.system('echo', 'title Arch Linux', '>', '/boot/loader/entries/arch.conf')
        os.system('echo', 'linux /vmlinuz-linux', '>>', '/boot/loader/entries/arch.conf')
        os.system('echo', 'initrd /initramfs-linux.img', '>>', '/boot/loader/entries/arch.conf')
        os.system('echo', 'options root=' + disk + '2 rw', '>>', '/boot/loader/entries/arch.conf')
    
    #install networkmanager
    def networkmanager():
        os.system('pacman', '-S', 'networkmanager')
        os.system('systemctl', 'enable', 'NetworkManager')
        

        
class PostBaseInstall:
    #add user
    def add_user():
        print("Enter username: ")
        username = input("Username: ")
        os.system('useradd', '-m', username)
        os.system('passwd', username)
        os.system('usermod', '-aG', 'wheel,audio,video,optical,storage', username)
        #enable sudo on wheel group
        os.system('sed', '-i', "'s/# %wheel ALL=(ALL) ALL/%wheel ALL=(ALL) ALL/g'", '/etc/sudoers')
    def FlahShipWM():
        #install 
        PKGS='zip','zsh','zsh-completions','wget','unrar','unzip','bashtop','hardinfo','neofetch','numlockx','xfce4-power-manager','xfce4-appfinder','rofi','xorg-fonts-type1','ttf-liberation','ttf-dejavu','ttf-bitstream-vera','sdl_ttf','gsfonts','font-bh-ttf','autofs','exfat-utils','ntfs-3g','terminator','catfish','nemo','variety','feh','network-manager-applet','xfce4-settings-manager','scrot','xfce4-screenshooter','lxappearance','gst-plugins-base','gst-plugins-good','gst-plugins-ugly','gst-plugins-bad','gst-libav','obs-studio','git','vlc','xfce4-screenshooter','xpdf','vim','i3-gaps','sddm'
        os.system('pacman', '-S', PKGS)          
        os.system('systemctl', 'enable', 'sddm')
        os.system('systemctl', 'enable', 'autofs')

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
        os.system('su', username)
        os.system('git', 'clone', 'https://aur.archlinux.org/yay.git')
        os.chdir('yay')
        os.system('makepkg', '-si')
        os.chdir('..')
        os.system('rm', '-rf', 'yay')
        os.system('exit')
    
    def trizen():
        #install trizen
        username = PostBaseInstall.add_user()
        os.system('su', username)
        os.system('git', 'clone', 'https://aur.archlinux.org/trizen.git')
        os.chdir('trizen')
        os.system('makepkg', '-si')
        os.chdir('..')
        os.system('rm', '-rf', 'trizen')
        os.system('exit')
    
    def paru():
        #install paru
        username = PostBaseInstall.add_user()
        os.system('su', username)
        os.system('git', 'clone', 'https://aur.archlinux.org/paru.git')
        os.chdir('paru')
        os.system('makepkg', '-si')
        os.chdir('..')
        os.system('rm', '-rf', 'paru')
        os.system('exit')

    def installAurPackages():
        PKGS1='visual-studio-code-bin','spotify','discord','telegram-desktop','zoom','google-chrome','polybar','networkmanager-dmenu-git','arc-gtk-theme','arc-icon-theme','papirus-icon-theme','papirus-folders','papirus-maia-icon-theme','papirus-maia-folders','papirus-maia-git','papirus-maia-icon-theme-git','nerd-fonts-iosevka','ttf-icomoon-feather','ttf-material-icons-git','siji-git','ttf-font-awesome','ttf-joypixels','ttf-nerd-fonts-symbols','ttf-ms-fonts'
        aur_helper = PostBaseInstall.installAur()
        if aur_helper == "yay":
            os.system('yay', '-S', PKGS1)
        elif aur_helper == "trizen":
            os.system('trizen', '-S', PKGS1)
        elif aur_helper == "paru":
            os.system('paru', '-S', PKGS1)
        elif aur_helper == "no":
            print("Ok")

    def installDotFiles():
        #install dotfiles
        username = PostBaseInstall.add_user()
        os.system('su', username)
        os.system('git', 'clone','--depth=1', 'https://github.com/adi1090x/polybar-themes.git')
        os.chdir('dotfiles')
        os.system('mv', 'config', '~/.config/i3/config')
        #installing polybar themes from github
        os.system('git', 'clone', 'https://github.com/adi1090x/polybar-themes.git')
        os.chdir('polybar-themes')
        os.system('chmod +x setup.sh')
        os.system('./setup.sh')
        os.chdir('..')
        os.system('rm', '-rf', 'polybar-themes')
        #install oh-my-zsh plugins
        os.system('git' ,'clone', 'https://github.com/zsh-users/zsh-autosuggestions' ,'${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions')
        os.system('git' ,'clone', '--depth','https://github.com/marlonrichert/zsh-autocomplete.git' ',${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autocomplete')
        os.system('git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k')
        #add plugins to .zshrc
        os.system('sed', '-i', "'s/plugins=(git)/plugins=(git zsh-autosuggestions)/g'", '~/.zshrc')
        os.system('sed', '-i', "'s/plugins=(git)/plugins=(git zsh-autocomplete)/g'", '~/.zshrc')
        os.system('sed', '-i', "'s/ZSH_THEME=\"robbyrussell\"/ZSH_THEME=\"powerlevel10k\/powerlevel10k\"/g'", '~/.zshrc')
        os.system('exit')

    def installGTK():
        #install nordic gtk theme
        username = PostBaseInstall.add_user()
        os.system('su', username)
        os.system('wget','https://github.com/EliverLara/Nordic-Polar/releases/download/v1.9.0/Nordic-Polar-standard-buttons.tar.xz')
        os.system('tar', '-xf', 'Nordic-Polar-standard-buttons.tar.xz', '-C', '~/.themes/')
        os.system('gsettings set org.gnome.desktop.interface gtk-theme "Nordic-Polar"')
        os.system('gsettings set org.gnome.desktop.wm.preferences theme "Nordic-Polar"')
        os.system('rm', 'Nordic-Polar-standard-buttons.tar.xz')
        os.system('exit')
    
    def installIcons():
        #install nordic icons
        username = PostBaseInstall.add_user()
        os.system('su', username)
        os.system('wget','https://github.com/EliverLara/Nordic/releases/download/v2.2.0/Nordic-darker.tar.xz')
        os.system('tar', '-xf', 'Nordic-darker.tar.xz', '-C', '~/.icons/')
        os.system('gsettings set org.gnome.desktop.interface icon-theme "Nordic-darker"')
        os.system('rm', 'Nordic-darker.tar.xz')
        os.system('exit')

    

#I’m not sure if this is the best way to do this, but it works. I’m open to suggestions on how to improve this.

class main():
    #DISK PARTITIONING
    DISKTOINSTALL()
    #BASE INSTALL
    ArchInstall()
    #POST BASE INSTALL
    PostBaseInstall()

if __name__ == "__main__":
    main()


