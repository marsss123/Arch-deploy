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
        #chroot
        subprocess.check_call('arch-chroot /mnt', shell=True)
        #set timezone based on user input
        print("Choose a timezone: ")
        os.system('ls', '/usr/share/zoneinfo')
        timezone = input("Timezone: ")
        os.system('ln -sf /usr/share/zoneinfo/' + timezone + '/etc/localtime')
        #set hardware clock
        os.system('hwclock --systohc')
        #set locale
        print("Choose a locale: ") 
        os.system('ls /etc/locale.gen')
        locale = input("Locale: ")
        os.system('sed -i' + "'s/#" + locale + "/" + locale + "/g'", '/etc/locale.gen')
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
            ArchInstall.grub()
        elif bootloader == "2":
            ArchInstall.systemd_boot()
        else:
            print("Invalid answer")
            ArchInstall.choose_bootloader()
        
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