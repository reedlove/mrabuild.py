# mrabuild.py
This is a simple and crude, yet effective, MiSTer MRA file scanner/rebuilder written in pure python.

No need to compile anything or mess with dependencies/modules, you just need a typical python 3 environment.

Using this will parse out the file names and checksums from the mra file, scan the rom path you specify for the needed files, and then rebuild the proper zip files in the current directory.

Warnings will be issued if the proper files cannot be located. This program will not override existing files.

Usage:
mrabuild.py *file.mra* *rompath*
