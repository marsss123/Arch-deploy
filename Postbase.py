import os

class PostBaseInstall:
    #add user
    def add_user():
        print("Enter username: ")
        username = input("Username: ")
        os.system('useradd -m' + username)
        os.system('passwd'+ username)
        os.system('usermod -aG wheel,audio,video,optical,storage' + username)
        #enable sudo on wheel group
        os.system('sed -i'+ "'s/# %wheel ALL=(ALL) ALL/%wheel ALL=(ALL) ALL/g'"+ '/etc/sudoers')

    def PacmanInst():
        #install 
        PKGS='zip','zsh','zsh-completions','wget','unrar','unzip','bashtop','hardinfo','neofetch','numlockx','xfce4-power-manager','xfce4-appfinder','rofi','xorg-fonts-type1','ttf-liberation','ttf-dejavu','ttf-bitstream-vera','sdl_ttf','gsfonts','font-bh-ttf','autofs','exfat-utils','ntfs-3g','terminator','catfish','nemo','variety','feh','network-manager-applet','xfce4-settings-manager','scrot','xfce4-screenshooter','lxappearance','gst-plugins-base','gst-plugins-good','gst-plugins-ugly','gst-plugins-bad','gst-libav','obs-studio','git','vlc','xfce4-screenshooter','xpdf','vim','i3-gaps','sddm'
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
        os.system('pacman -S yay*')
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
        os.system('pacman -S trizen*')
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
        os.chdir('..')
        os.system('rm -rf paru')
        os.system('exit')

    def installAurPackages():
        PKGS1='visual-studio-code-bin','spotify','discord','telegram-desktop','zoom','google-chrome','polybar','networkmanager-dmenu-git','arc-gtk-theme','arc-icon-theme','papirus-icon-theme','papirus-folders','papirus-maia-icon-theme','papirus-maia-folders','papirus-maia-git','papirus-maia-icon-theme-git','nerd-fonts-iosevka','ttf-icomoon-feather','ttf-material-icons-git','siji-git','ttf-font-awesome','ttf-joypixels','ttf-nerd-fonts-symbols','ttf-ms-fonts'
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