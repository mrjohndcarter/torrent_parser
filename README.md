torrent_parser
==============

*Coding Exercise*

Please use Python 2.7 to perform the following task:
Write a re-usable library to parse BitTorrent files. The library should expose 
at least the following pieces of information (when available in the file):
- creation date
- client that created the file
- the tracker URL
- the name, length, and checksum of each file described in the torrent
 
No third-party libraries should be used for this project, only the Python standard library.

references
--
- http://wiki.theory.org/BitTorrentSpecification
- http://www.bittorrent.org/beps/bep_0003.html