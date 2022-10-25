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
       

    #get disk from the function above and make user choose which disk to install on
    def choose_disk():
        disks = DISKTOINSTALL.get_disks()
        print("Choose a disk to install on: ")
        for i in range(len(disks)):
            print(str(i) + ": " + disks[i])
        disk = disks[int(input("Disk: "))]
        

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