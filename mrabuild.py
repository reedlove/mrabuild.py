#!/usr/bin/python3
import os, zipfile, sys

def bye(msg):
    print(msg)
    print('Exiting...')
    quit()

def crchex(num):
    num = int(num)
    num = hex(num)[2:]
    while len(num) < 8:
        num = '0' + num
    return num

usetext = 'Usage: mrabuild.py *file.mra* *rom path*'

if len(sys.argv) != 3:
    bye(usetext)

try:
    inmra = open(sys.argv[1])
except IOError:
    bye('Invalid MRA file path')

if not os.path.isdir(sys.argv[2]):
    bye('Invalid ROM path.')
else:
    zipdir = sys.argv[2]
    if zipdir[-1] != '/':
        zipdir += '/'

## Main Logic ##
# Check for valid markup.
run = False

for line in inmra:
    if '<misterromdescription' in line:
        run = True
        inmra.seek(0)
        break

if not run:
    inmra.close()
    bye('Invalid MRA file.')

# Process the MRA file.
zipfiles = []
mracrcs = {}
zipcrcs = {}

while run:
    line = inmra.readline()
    line = line.strip()
    if line == '':
        continue
    if line == '</misterromdescription>':
        run = False
        continue
    if '<rom' in line and 'zip=' in line:
        idx1 = line.index('zip=') + 5
        esc = line[idx1 - 1]
        idx2 = line.index(esc, idx1)
        zipname = line[idx1:idx2]
        if '|' in zipname:
            for item in zipname.split('|'):
                zipfiles.append(item)
        else:
            zipfiles.append(zipname)
    elif '<part' in line and 'crc=' in line and 'name=' in line:
        idx1 = line.index('crc=') + 5
        esc = line[idx1 - 1]
        idx2 = line.index(esc, idx1)
        crc = line[idx1:idx2]
        idx1 = line.index('name=') + 6
        esc = line[idx1 - 1]
        idx2 = line.index(esc, idx1)
        name = line[idx1:idx2]
        mracrcs[crc] = name

inmra.close()

# Record zip file crcs and names.
outfile = open('invalid.txt', 'a')

for zipname in zipfiles:
    if not os.path.isfile(zipdir + zipname):
        bye('Could not find: ' + zipname)
    try:
        infile = zipfile.ZipFile(zipdir + zipname)
    except zipfile.BadZipFile:
        outfile.write(zipname + '\n')
        bye(zipname + ' *INVALID ZIP FILE*')
    for item in infile.infolist():
        name = item.filename
        crc = crchex(item.CRC)
        zipcrcs[crc] = name
    infile.close()

outfile.close()

# Verify that all needed files exist.
for crc in mracrcs:
    if crc in zipcrcs:
        print(crc, '*FOUND*')
    else:
        bye(crc + ' *NOT FOUND*')

# Rebuild ZIP files.
for zipname in zipfiles:
    if os.path.isfile(zipname):
        print(zipname, '*EXISTS*')
        continue
    print('Building:', zipname)
    outzip = zipfile.ZipFile(zipname, mode='w')
    inzip = zipfile.ZipFile(zipdir + zipname)
    for item in inzip.infolist():
        crc = crchex(item.CRC)
        if crc in mracrcs:
            outzip.writestr(mracrcs[crc], inzip.read(item.filename))
    inzip.close()
    outzip.close()

bye('Done.')
