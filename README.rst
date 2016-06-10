Misc
========================

Several prototypes for different uses

lastfm
++++++

Generates a m3u playlist with files from your directory based on top plays on last.fm

Music Directory
---------------

Works pretty fine if your music directory structure is :

     MUSICDIR / Artist / Year - Album / Track - Title

I have no clue, if this will work with another structure

Requires
--------

ConfigParser, sys, os, urllib2, json, time, shutil, filecmp, Levenshtein

Configuration
-------------

  * Create config.ini like config.ini.empty
  * execute

  python playlist.py [length [page]]

  - length = number of songs in the playlist (default: 100)
  - page = offset (default: 1)
      example: "python playlist 200 200" retrieves your top played song from 201 to 400)

Music player device
-------------------

If you have a device that support direct file transfer, you have the possibility to automatically transfer the file from the playlist to it

Adaptation
----------

This script is not perfect, feel free to adapt, please drop me an email if you do
