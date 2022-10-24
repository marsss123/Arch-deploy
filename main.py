import subprocess
import os
import sys
from subprocess import call

class insdisk:
    def __init__(self,bootselect,rootselect,swapselect):
        self.bootselect = bootselect
        self.rootselect = rootselect
        self.swapselect = swapselect
        
    def root(self):
        os.system(["mkfs.ext4", self.rootselect])
        os.system(["mount", self.rootselect]) 
        os.system(['mount', self.rootselect, '/mnt'])

    def boot(self):
        os.system(["mkfs.fat -F32", self.bootselect])
        os.system(["mount", self.bootselect])
        os.system(["mkdir", "/mnt/boot"])
        os.system(["mount", self.bootselect, "/mnt/boot"])

    def swap(self):
        os.system(["mkswap", self.swapselect])
        os.system(["swapon", self.swapselect])

class install:
    def __init__(self):
        self.install()
        self.postchroot()
    def install(self):
        os.system(['pacstrap', '/mnt', 'base' , 'linux', 'linux-firmware' , 'linux-headers','base-devel','vim','networkmanager'])
        os.system('genfstab', '-U', '/mnt', '>>', '/mnt/etc/fstab')
        os.system('arch-chroot', '/mnt')
    def postchroot(self):
        os.system('arch-chroot', '/mnt')
        os.system('ln -sf', '/usr/share/zoneinfo/Asia/Kolkata', '/etc/localtime')
        os.system('hwclock', '--systohc')
        os.system('vim', '/etc/locale.gen')
        os.system('locale-gen')
        os.system('echo', 'LANG=en_US.UTF-8', '>>', '/etc/locale.conf')
        os.system('echo', 'KEYMAP=us', '>>', '/etc/vconsole.conf')
        os.system('echo', 'ArchBTW', '>>', '/etc/hostname')

class postchroot:
    def __init__(self,settime,hwclock,locale,localegen,localeconf,hostname,rootpass,bootloader,grubinstall,grubmkconfig,useradd,userpass,sudoers,network,wmdeployscript):
        self.settime = settime()
        self.hwclock = hwclock()
        self.locale = locale()
        self.localegen = localegen()
        self.localeconf = localeconf()
        self.hostname = hostname()
        self.rootpass = rootpass()
        self.bootloader = bootloader()
        self.grubinstall = grubinstall()
        self.grubmkconfig = grubmkconfig()
        self.useradd = useradd()
        self.userpass = userpass()
        self.sudoers = sudoers()
        self.network = network()
        self.wmdeployscript = wmdeployscript()
        self.exit = exit()
        self.umount = umount()
        self.reboot = reboot()
    def settime(self):
        os.system('ln', '-sf', '/usr/share/zoneinfo/Asia/Kolkata', '/etc/localtime')
    def hwclock(self):
        os.system('hwclock', '--systohc')
    def locale(self):
        os.system('echo', 'en_US.UTF-8 UTF-8', '>>', '/etc/locale.gen')
    def localegen(self):
        os.system('locale-gen')
    def localeconf(self):
        os.system('echo', 'LANG=en_US.UTF-8', '>>', '/etc/locale.conf')
    def hostname(self):
        os.system('echo', 'archlinux', '>>', '/etc/hostname')
    def rootpass(self):
        os.system('passwd')
    def bootloader(self):
        os.system('pacman', '-S','grub','efibootmgr','os-prober')
    def grubinstall(self):
        os.system('grub-install', '--target=x86_64-efi', '--efi-directory=/boot', '--bootloader-id=GRUB')
    def grubmkconfig(self):
        os.system('grub-mkconfig', '-o', '/boot/grub/grub.cfg')
    def useradd(self):
        os.system('useradd', '-m', '-G', 'wheel', 'ArchBtw')
    def userpass(self):
        os.system('passwd', 'ArchBTW')
    def sudoers(self):
        os.system('echo', '%wheel ALL=(ALL) ALL', '>>', '/etc/sudoers')
    def network(self):
        os.system('systemctl', 'enable', 'NetworkManager')
    def wmdeployscript(self):
        os.system('chmode +x', '~/Arch-deploy/setup.sh')
        os.system('sh', '~/Arch-deploy/setup.sh' )    
    def exit(self):
        os.system('exit')
    def umount(self):
        os.system('umount', '-R', '/mnt')
    def reboot(self):
        os.system('reboot')  

class main:
    def __init__(self,insdisk,install,postchroot):
        self.insdisk = insdisk()
        self.install = install()
        self.postchroot = postchroot()
    def insdisk(self):
        self.insdisk.format()
        self.insdisk.mount()
    def install(self):
        self.install.install()
    def postchroot(self):
        self.postchroot.settime()
        self.postchroot.hwclock()
        self.postchroot.locale()
        self.postchroot.localegen()
        self.postchroot.localeconf()
        self.postchroot.hostname()
        self.postchroot.rootpass()
        self.postchroot.bootloader()
        self.postchroot.grubinstall()
        self.postchroot.grubmkconfig()
        self.postchroot.useradd()
        self.postchroot.userpass()
        self.postchroot.sudoers()
        self.postchroot.network()
        self.postchroot.wmdeployscript()
        self.postchroot.exit()
        self.postchroot.umount()
        self.postchroot.reboot()

if __name__ == '__main__':
    a = insdisk(bootselect=input("Enter the boot partition path: "),rootselect=input("Enter the root partition path: "),swapselect=input("Enter the swap partition path: "))
    install()
    postchroot()