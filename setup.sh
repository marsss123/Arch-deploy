echo
echo "========================================="
echo "Installing packages"
echo "========================================="
echo 

sed -i '/\[multilib\]/s/^#//g' /etc/pacman.conf
sed -i '/\[multilib\]/{n;s/^#//g}' /etc/pacman.conf
pacman -Syu

PKGS=(
        # UTILITIES =============================================================
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
        'wine'
        'wine_gecko'
        'wine-mono'
        'zenity'
        'xorg-fonts-type1'
	'ttf-liberation'
	'ttf-dejavu'
        'ttf-bitstream-vera'
        'sdl_ttf'
        'gsfonts'
        'font-bh-ttf'
        # DISK UTILITIES ------------------------------------------------------
        'autofs'                
        'exfat-utils'                          
        'ntfs-3g'               
        # GENERAL UTILITIES ---------------------------------------------------
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
        # DEVELOPMENT ---------------------------------------------------------               
        'git'                   
        # MEDIA --------------------------------------------------------------- 
        'vlc'                   
        'xfce4-screenshooter'               
        # PRODUCTIVITY --------------------------------------------------------    
        'xpdf'                  
        'vim'   
        'i3-gaps'
        'sddm'


)

for PKG in "${PKGS[@]}"; do
    echo "INSTALLING: ${PKG}"
    sudo pacman -S "$PKG" --noconfirm --needed
    done
sudo systemctl enable sddm

mv ".zshrc" "${HOME}/.zshrc"    
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-${HOME}/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-${HOME}/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
mv "${HOME}/Git/ArchPost/config" "${HOME}/.config/i3/config"

echo "========================================="
echo "Done!"
echo "========================================="

echo "Now installing yay AUR helper"
echo "Cloning yay AUR helper"
git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si
cd ..
rm -rf yay
curl -sS https://download.spotify.com/debian/pubkey_0D811D58.gpg | gpg --import -
echo "Now installing AUR software"

PKGS1=(

	# DEVELOPMENT ---------------------------------------------------------
	'visual-studio-code-bin'    
        'android-studio'
	# MEDIA ---------------------------------------------------------------
	'spotify'                   
        # PRODUCTIVITY --------------------------------------------------------
        'discord'
        'telegram-desktop'
        'zoom'

	# BROWSER  -------------------------------------------------------------
	'google-chrome'	    # Google Chrome

	# BAR ------------------------------------------------------------------
	'polybar'
	'networkmanager-dmenu-git'
        # THEMES --------------------------------------------------------------
        'arc-gtk-theme'
        'arc-icon-theme'
        'papirus-icon-theme'
        'papirus-folders'
        'papirus-maia-icon-theme'
        'papirus-maia-folders'
        'papirus-maia-git'
        'papirus-maia-icon-theme-git'
        # FONTS ---------------------------------------------------------------
        'nerd-fonts-iosevka'
        'ttf-icomoon-feather'
        'ttf-material-icons-git'
        'siji-git'
        'ttf-font-awesome'
        'ttf-joypixels'
        'ttf-nerd-fonts-symbols'
        'ttf-ms-fonts'

)


for PKG in "${PKGS1[@]}"; do
	    yay -S --noconfirm $PKG
done

