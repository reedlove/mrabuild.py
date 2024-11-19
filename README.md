# mrabuild.py
This is a simple and crude, yet effective, MiSTer MRA file scanner/rebuilder writter in pure python. No need to compile anything or mess with dependencies, you just need a typical python3 environment.
Using this will parse out the file names and checksums from the mra file, scan the rom path you specify, and rebuild the proper zip files in the current directory.
Warnings will be issued if the proper files cannot be located. This program will not override existing files as well.

Usage:
mrabuild.py *file.mra* *rompath*
