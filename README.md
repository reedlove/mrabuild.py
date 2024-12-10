# mrabuild.py
This is a simple and crude, yet effective, MiSTer MRA file scanner/rebuilder written in pure python.

No need to compile anything or mess with dependencies/modules, you just need a typical python 3 environment.

Using this will parse out the file names and checksums from the mra file, scan the rom path you specify for the needed files, and then build the zip files in the directory you specify.

As long as there aren't multiples of the same file name, mrabuild.py will also combine different versions of roms in to a single zip file.

Warnings will be issued if the proper files cannot be located. This program will not overwrite existing files.

Usage:
mrabuild.py *file.mra* *path to source zip files* *destination*
