import subprocess
import os
import sys
from subprocess import call

class insdisk:
    bootselect = input("Enter the boot partition path: ")
    rootselect = input("Enter the root partition path: ")
    swapselect = input("Enter the swap partition path: ")
    def __init__(self):
        self.bootselect = insdisk.bootselect
        self.rootselect = insdisk.rootselect
        self.swapselect = insdisk.swapselect
    def boot(self):
        subprocess.call(["mkfs.fat -F32", self.bootselect])
        subprocess.call(["mount", self.bootselect, "/mnt/boot"])
    def root(self):
        subprocess.call(["mkfs.ext4", self.rootselect])
        subprocess.call(["mount", self.rootselect, "/mnt"]) 
    def swap(self):
        subprocess.call(["mkswap", self.swapselect])
        subprocess.call(["swapon", self.swapselect])

class install:
    def __init__(self,format,mount,install,postchroot):
        self.format = format()
        self.mount = mount()
        self.install = install()
        self.postchroot = postchroot()
    def format(self):
        self.format.boot()
        self.format.root()
        self.format.swap()
    def mount(self):
        self.mount.boot()
        self.mount.root()
        self.mount.swap()
    def install(self):
        subprocess.call(['pacstrap', '/mnt', 'base' , 'linux', 'linux-firmware' , 'linux-headers','base-devel','vim','networkmanager'])
        subprocess.call('genfstab', '-U', '/mnt', '>>', '/mnt/etc/fstab')
        subprocess.call('arch-chroot', '/mnt')
    def postchroot(self):
        subprocess.call('arch-chroot', '/mnt')
        subprocess.call('ln -sf', '/usr/share/zoneinfo/Asia/Kolkata', '/etc/localtime')
        subprocess.call('hwclock', '--systohc')
        subprocess.call('vim', '/etc/locale.gen')
        subprocess.call('locale-gen')
        subprocess.call('echo', 'LANG=en_US.UTF-8', '>>', '/etc/locale.conf')
        subprocess.call('echo', 'KEYMAP=us', '>>', '/etc/vconsole.conf')
        subprocess.call('echo', 'ArchBTW', '>>', '/etc/hostname')

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
        subprocess.call('ln', '-sf', '/usr/share/zoneinfo/Asia/Kolkata', '/etc/localtime')
    def hwclock(self):
        subprocess.call('hwclock', '--systohc')
    def locale(self):
        subprocess.call('echo', 'en_US.UTF-8 UTF-8', '>>', '/etc/locale.gen')
    def localegen(self):
        subprocess.call('locale-gen')
    def localeconf(self):
        subprocess.call('echo', 'LANG=en_US.UTF-8', '>>', '/etc/locale.conf')
    def hostname(self):
        subprocess.call('echo', 'archlinux', '>>', '/etc/hostname')
    def rootpass(self):
        subprocess.call('passwd')
    def bootloader(self):
        subprocess.call('pacman', '-S','grub','efibootmgr','os-prober')
    def grubinstall(self):
        subprocess.call('grub-install', '--target=x86_64-efi', '--efi-directory=/boot', '--bootloader-id=GRUB')
    def grubmkconfig(self):
        subprocess.call('grub-mkconfig', '-o', '/boot/grub/grub.cfg')
    def useradd(self):
        subprocess.call('useradd', '-m', '-G', 'wheel', 'ArchBtw')
    def userpass(self):
        subprocess.call('passwd', 'ArchBTW')
    def sudoers(self):
        subprocess.call('echo', '%wheel ALL=(ALL) ALL', '>>', '/etc/sudoers')
    def network(self):
        subprocess.call('systemctl', 'enable', 'NetworkManager')
    def wmdeployscript(self):
        subprocess.call('chmode +x', '~/Arch-deploy/ArchPost/setup.sh')
        subprocess.call('sh', '~/Arch-deploy/ArchPost/setup.sh' )    
    def exit(self):
        subprocess.call('exit')
    def umount(self):
        subprocess.call('umount', '-R', '/mnt')
    def reboot(self):
        subprocess.call('reboot')  

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