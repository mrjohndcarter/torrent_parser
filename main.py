# demo file for torrent.py
# @todo -- move these into unit tests

from torrent import TorrentMeta

def main():

  # demo
  for filename in ['mint.torrent','multi_1tracker.torrent','multi_2tracker.torrent','multi_2tracker_utorrent.torrent','pear.torrent']:
    t = TorrentMeta('testfiles/' + filename)
    print 'Creation Date: ' + str(t.creation_date)
    print 'Created By: ' + t.created_by
    print 'Tracker:' + t.announce
    print 'Tracker list: (' + str(t.announce_list) +')'
    print 'Files: '
    for f in t:
      print ''.join(['\tName: ',f.name])
      print ''.join(['\tLength: ',str(f.length)])
      if f.md5sum:
        print ''.join(['\tMD5 Hash: ',f.md5sum])
      else:
        print '\t(No MD5 hash for file)'

  # fail:
    try:
      t = TorrentMeta('testfiles/trashed1.torrent')
    except SyntaxError,e:
      print ''.join(['\n\n',str(e)])
  # fail:
    try:
      t = TorrentMeta('testfiles/unbalanced1.torrent')
    except SyntaxError,e:
      print ''.join(['\n\n',str(e)])

if __name__ == "__main__":
    main()