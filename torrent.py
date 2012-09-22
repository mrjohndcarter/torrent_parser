# file: torrent.def
# author: jcarter
# desciption: class to parse a bit torrent file

from bencode_decoder import beparse
from pprint import pprint

meta_attributes = {
                  'announce' : 'announce',
                  'announce_list' : 'announce-list',
                  'comment' : 'comment',
                  'created_by' : 'created by',
                  'creation_date' : 'creation date',
                  'encoding' : 'encoding'
                  }

info_attributes = {
                  'pieces' : 'pieces',
                  'piece_length' : 'piece length',
                  'private' : 'private'
                  }

file_attributes = {
                  'name' : 'name',
                  'length' : 'length',
                  'md5sum' : 'md5sum',
                  'path' : 'path'
                  }

class TorrentFile:
  def __init__(self,meta_file):
    self.meta = meta_file

  def __getattr__(self,name):
    pass


class TorrentMeta:
  def __init__(self,filename):
    self.file_dict = beparse(open(filename).read())

  def __len__(self):
    if not self.file_dict:
      return 0;
    if 'files' in self.file_dict['info']:
      return len(self.file_dict['info']['files'])
    else:
      return 1

  def __getattr__(self, name):
    if not self.file_dict:
      raise KeyError
    if name in meta_attributes:
      return self.file_dict[meta_attributes[name]]

def main():

  t = Torrent('./testfiles/mint.torrent')
  print len(t)
  print t.announce
  print t.announce_list
  print t.comment
  print t.encoding
  print t.creation_date
  print t.created_by

if __name__ == '__main__':
    main()
    #unittest.main()