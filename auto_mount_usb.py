import subprocess
# ASSUMED THAT THIS COMMAND HAS ALREADY BEEN RUN
# sudo mkdir /mnt/usb_stick

MOUNT_DIR = "/media/usb"

def run_command(command):
    # start = time.time()
    try:
        output = subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as ex:
        return None
        raise Exception("FAILED: %s" % command)
    # end = time.time()
    # print "Finished in %s seconds" % (end - start)
    print(output)
    return output.splitlines() 


def uuid_from_line(line):
    start_str = "UUID=\""
    example_uuid = "6784-3407"
    uuid_start = line.index(start_str) + len(start_str)
    uuid_end = uuid_start + len(example_uuid)
    return line[uuid_start: uuid_end]

def mount_usb():
    output = run_command("blkid | grep sda")
    if None==output:
        return
    # ['/dev/sda1: LABEL="KINGSTON" UUID="6784-3407" TYPE="vfat" PARTUUID="459720e1-01"']
    for usb_device in output:
        command = "sudo mount /dev/sda1 %s" % (MOUNT_DIR)
        run_command(command)
        break

def umount_usb():
    command = "sudo umount %s" % (MOUNT_DIR)
    run_command(command)
    
mount_usb()

umount_usb()    
