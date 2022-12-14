from glob import glob
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
       

    #choose the disk to install linux on and return it to a variable
    def choose_disk():
        print("Choose the disk you want to install linux on")
        disks = DISKTOINSTALL.get_disks()
        for i in range(len(disks)):
            print(str(i) + " " + disks[i])
        answer = input("Answer: ")
        if answer == "0":
            return disks[0]
        elif answer == "1":
            return disks[1]
        elif answer == "2":
            return disks[2]
        elif answer == "3":
            return disks[3]
        elif answer == "4":
            return disks[4]
        elif answer == "5":
            return disks[5]
        elif answer == "6":
            return disks[6]
        elif answer == "7":
            return disks[7]
        elif answer == "8":
            return disks[8]
        elif answer == "9":
            return disks[9]
        else:
            print("Invalid answer")
            DISKTOINSTALL.choose_disk()
        
        
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
        disk_name = disk[:-1]

        print("Making partitions manually")
        print("Do you want to use cfdisk or fdisk? (c/f)")
        answer = input("Answer: ")
        if answer == "c":
            os.system("cfdisk " + disk_name)
            #format the partitions
            os.system("mkfs.fat -F32 " + disk_name + "1")
            os.system("mkfs.ext4 " + disk_name + "2")
            os.system("mkswap " + disk_name + "3")
            os.system("swapon " + disk_name + "3")
            #mount the partitions
            os.system("mount " + disk_name + "2 /mnt")
            os.system("mkdir /mnt/boot")
            os.system("mount " + disk_name + "1 /mnt/boot")
        elif answer == "f":
            os.system("fdisk " + disk_name)
            #format the partitions
            os.system("mkfs.fat -F32 " + disk_name + "1")
            os.system("mkfs.ext4 " + disk_name + "2")
            os.system("mkswap " + disk_name + "3")
            os.system("swapon " + disk_name + "3")
            #mount the partitions
            os.system("mount " + disk_name + "2 /mnt")
            os.system("mkdir /mnt/boot")
            os.system("mount " + disk_name + "1 /mnt/boot")

        else:
            print("Invalid answer")
            DISKTOINSTALL.make_partitions_manually()
        
    #make partitions automatically using parted and efi
    def make_partitions_automatically():
        disk = DISKTOINSTALL.choose_disk()
        #save the disk name without the number
        disk_name = disk[:-1]
        print("Making partitions automatically with efi")
        #ask for swap size 
        print("Enter swap size in GB")
        print("Swap is a partition that is used as virtual memory")
        swap_size = input("Swap size: ")
        #make the partitions
        os.system("parted " + disk_name + " mklabel gpt")
        os.system("parted " + disk_name + " mkpart primary fat32 1MiB 512MiB")
        os.system("parted " + disk_name + " set 1 esp on")
        os.system("parted " + disk_name + " mkpart primary ext4 512MiB 100%")
        os.system("parted " + disk_name + " mkpart primary linux-swap 0 " + swap_size + "G")
        os.system("parted " + disk_name + " set 3 swap on")
        #format the partitions
        os.system("mkfs.fat -F32 " + disk_name + "1")
        os.system("mkfs.ext4 " + disk_name + "2")
        os.system("mkswap " + disk_name + "3")
        os.system("swapon " + disk_name + "3")
        #mount the partitions
        os.system("mount " + disk_name + "2 /mnt")
        os.system("mkdir /mnt/boot")
        os.system("mount " + disk_name + "1 /mnt/boot")

    