import os
import sys
import hashlib

sampleSize = 16 * 1024
sampleThreshold = 128 * 1024


def hashCore(fstat, fio):
    shasum = hashlib.sha256()
    if fstat.st_size < sampleThreshold:
        shasum.update(fio.read())
    else:
        shasum.update(fio.read(sampleSize))
        fio.seek(int((fstat.st_size if fstat.st_size %
                      2 == 0 else fstat.st_size - 1) / 2))
        shasum.update(fio.read(sampleSize))
        fio.seek(-1*sampleSize, os.SEEK_END)
        shasum.update(fio.read())
    return shasum.hexdigest()


def main():
    if len(sys.argv) > 1:
        fstat = os.stat(sys.argv[1])
        with open(sys.argv[1], 'rb') as fio:
            print(hashCore(fstat, fio))


if __name__ == "__main__":
    main()
