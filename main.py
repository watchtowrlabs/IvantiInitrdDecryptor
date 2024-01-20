from Crypto.Cipher import AES

# Find this value from the kernel. It's usually straight after the version info in the binary.
# Find it by finding a function which references the string "/initrd.image" and also the string "vaes".
# You'll see a value being XOR'ed with the following constant.
rawkey = [ ... ]
xorKey = [ 0xf2, 0x2b, 0xed, 0x99, 0xfe, 0x41, 0xef, 0xae, 0xc7, 0x58, 0x10, 0x14, 0x0e, 0x18, 0xed, 0xd2 ]
key = b''
for n in range(0, len(rawkey)):
    key += (rawkey[n].to_bytes(1, 'little')[0] ^ xorKey[n].to_bytes(1, 'little')[0]).to_bytes(1, 'little')

aes = AES.new(key, AES.MODE_ECB)

with open('coreboot.img', 'rb') as f:
    encryptedData = bytearray(f.read())

with open('decrypted.gz', 'wb') as f:
    sectorNum = 0
    while sectorNum * 0x200 < len(encryptedData):
        dataStartPos = sectorNum * 0x200
        dataEndPos = dataStartPos + 0x200
        thisBlock = encryptedData[dataStartPos:dataEndPos]
        sectorNumBytes = sectorNum.to_bytes(4, 'little') + bytearray(0x0C)
        decryptedSectorNum = aes.decrypt(sectorNumBytes)

        for chunk in range(0, 0x200, 0x10):
            thisChunk = thisBlock[chunk:chunk+0x10]
            nextSectorNumBytes = b""
            if len(thisChunk) == 10:
                thisChunk += bytearray(0x06)
            if len(thisChunk) == 0:
                break
            for n in range(0, len(decryptedSectorNum)):
                thisChunk[n] = thisChunk[n] ^ decryptedSectorNum[n]
                nextSectorNumBytes += thisChunk[n].to_bytes(1, 'little')

            thisChunk = aes.decrypt(thisChunk)

            for n in range(0, len(sectorNumBytes)):
                f.write((thisChunk[n] ^ sectorNumBytes[n]).to_bytes(1, 'little'))

            sectorNumBytes = nextSectorNumBytes

        sectorNum = sectorNum + 1
