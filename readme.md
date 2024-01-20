Here's a quick-and-dirty tool to decrypt the Ivanti device's initrd. It's mostly academic since there are other ways to extract the (much more useful) LVM keys for the real root device.

To use it, copy the kernel file from the Ivanti, and extract the ELF from the bzImage (I used `binwalk -e`). Throw it into IDA, and look for the function that references the strings "/initrd.image" and also "vaes". The initrd AES key will be there. Add this key to the script, supply your initrd, and you'll get a gz.

Note that I had trouble extracting the gzipped kernel - I ended up using 7zip which was much more forgiving (than `gz`).