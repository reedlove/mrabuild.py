#!/usr/bin/python3
import os, shutil, sys, zipfile

# Boiler plate
def bye(msg):
    print(msg)
    quit()

def hexfmt(item):
    item = int(item)
    item = hex(item)[2:]
    while len(item) < 8:
        item = '0' + item
    return item

usage = 'mrabuild.py *mra file* *src path* *dst path*'

if len(sys.argv) != 4:
    bye(usage)

mrafile = sys.argv[1]
srcpath = sys.argv[2]
dstpath = sys.argv[3]

# Command Checks
if not os.path.isfile(mrafile):
    bye('Invalid MRA file.')

if not os.path.isdir(srcpath):
    bye('Invalid SRC path.')

if not os.path.isdir(dstpath):
    bye('Invalid DST path.')

if srcpath == dstpath:
    bye('*src path* and *dst path* must not match.')

# MRA Processing
inmra = open(mrafile)

ismra = False
zipnames = False

for line in inmra:
    line = line.strip()
    if line == '':
        continue
    if ismra:
        if 'zip=' in line:
            idx1 = line.index('zip=') + 5
            esc = line[idx1 - 1]
            idx2 = line.index(esc, idx1)
            zipnames = line[idx1:idx2]
            if '|' in zipnames:
                zipnames = zipnames.split('|')
            else:
                zipnames = [zipnames]
        elif '<part ' in line and 'name=' in line and 'crc=' in line:
            idx1 = line.index('name=') + 6
            esc = line[idx1 - 1]
            idx2 = line.index(esc, idx1)
            name = line[idx1:idx2]
            idx1 = line.index('crc=') + 5
            esc = line[idx1 - 1]
            idx2 = line.index(esc, idx1)
            crc = line[idx1:idx2]
            if crc not in mracrcs:
                mracrcs[crc] = name
    elif '<misterromdescription>' in line:
        ismra = True
        mracrcs = {}
        print('Processing:', mrafile)

inmra.close()

if not ismra:
    bye('Invalid MRA file.')

if not zipnames:
    bye('No zip files in MRA.')

# Start checking stuff
if srcpath[-1] != '/':
    srcpath += '/'

if dstpath[-1] != '/':
    dstpath += '/'

check = True

for zipname in zipnames:
    fullpath = srcpath + zipname
    if os.path.isfile(fullpath):
        if not zipfile.is_zipfile(fullpath):
            print('Corrupted:', fullpath)
            check = False
        else:
            print('Found:', fullpath)
    else:
        print('Missing:', fullpath)
        check = False

if not check:
    bye('Zipfiles are missing or corrupted.')

zipcrcs = {}

for zipname in zipnames:
    fullpath = srcpath + zipname
    inzip = zipfile.ZipFile(fullpath)
    for info in inzip.infolist():
        crc = hexfmt(info.CRC)
        name = info.filename
        if crc not in zipcrcs:
            zipcrcs[crc] = name
    inzip.close()

# Verify that all CRCs have been found.
for crc in mracrcs:
    if crc not in zipcrcs:
        print('Missing:', mracrcs[crc], crc)
        check = False

if not check:
    bye('Failed: ' + mrafile)

for zipname in zipnames:
    fullpath = dstpath + zipname
    if os.path.isfile(fullpath):
        print('Exists: ', fullpath)
        if not zipfile.is_zipfile(fullpath):
            print('Corrupted:', fullpath)
            print('Deleting:', fullpath)
            os.remove(fullpath)
            print('Creating:', fullpath)
            outzip = zipfile.ZipFile(fullpath, 'w') 
        else:
            print('Appending to:', fullpath)
            outzip = zipfile.ZipFile(fullpath, 'a')
    else:
        print('Creating:', fullpath)
        outzip = zipfile.ZipFile(fullpath, 'w')
    fullpath = srcpath + zipname
    print('Reading from:', fullpath)
    inzip = zipfile.ZipFile(fullpath)
    for info in inzip.infolist():
        crc = hexfmt(info.CRC)
        if crc in mracrcs:
            if mracrcs[crc] not in outzip.namelist():
                print('Adding:', mracrcs[crc])
                outzip.writestr(mracrcs[crc], inzip.read(info.filename))
            else:
                print('Contains:', mracrcs[crc])
    inzip.close()
    outzip.close()

print('Done.')
