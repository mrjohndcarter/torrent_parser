# file: torrent.def
# author: jcarter
# desciption: class to parse a bit torrent file

# notes:
# - assumes single file/multifile is 'well formed'
#   i.e. -- a single file is not represented as a multifile representation of len 1.

from bencode_decoder import beparse
from pprint import pprint
from itertools import chain

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
  def __init__(self,meta_file,index):
    self.meta = meta_file
    self.index = index
    #print self.meta.torrent_dict['info']['files'][index]

  @classmethod
  def __join_path__(klass,l):
    return '/'.join(l)

  def filename(self):
    if self.meta.single_file_mode:
      return self.meta.torrent_dict['info']['name']
    elif len(self.meta.torrent_dict.get('name','')) == 0:
      return TorrentFile.__join_path__(self.__getattr__('path'))
    else:
      return '/'.join([self.meta.torrent_dict.get('name',''),TorrentFile.__join_path__(self.__getattr__('path'))])

  def __getattr__(self,name):
    if name not in file_attributes:
      raise KeyError
    if self.meta.single_file_mode:
      return self.meta.torrent_dict['info'].get(name,'')
    else:
      return self.meta.torrent_dict['info']['files'][self.index].get(name,'')

  def __str__(self):
    return ''.join(['TorrentFile:',
      TorrentMeta.__separator__(),
      'File: ',
      self.filename(),
      TorrentMeta.__separator__(),
      'md5: ',
      self.__getattr__('md5sum'),
      TorrentMeta.__separator__(),
      'length: ',
      str(self.__getattr__('length'))])

class TorrentMeta:
  def __init__(self,filename):
    self.torrent_dict = beparse(open(filename).read())
    if 'files' in self.torrent_dict['info']:
      self.single_file_mode = False
    else:
      self.single_file_mode = True

  def __len__(self):
    if not self.torrent_dict:
      return 0;
    if self.single_file_mode:
      return 1
    else:
      return len(self.torrent_dict['info']['files'])

  def __getattr__(self, name):
    if not self.torrent_dict:
      raise KeyError
    if name in meta_attributes:
      return self.torrent_dict[meta_attributes[name]]

  def __getitem__(self, key):
    if not self.torrent_dict or (key < 0) or (key >= self.__len__()):
      raise KeyError
    return TorrentFile(self,key)

  # utility method -- parsed as a list of lists, each containing one string
  # this turns that into a list of strings
  @classmethod
  def __flatten_list__(klass,l):
    return [s[0] for s in l]

  # used for hierarchical printing
  @classmethod
  def __separator__(klass,indent_level=1):
    return ''.join(['\n','\t'*indent_level])

  def __str__(self):
    return ''.join(['Bit Torrent Metainfo:',
      TorrentMeta.__separator__(),
      'Announce URL: ',
      self.__getattr__('announce'),
      TorrentMeta.__separator__(),
      'Announce List: ',
      TorrentMeta.__separator__(2),
      TorrentMeta.__separator__(2).join(TorrentMeta.__flatten_list__(self.__getattr__('announce_list'))),
      TorrentMeta.__separator__(),
      'Comment: ',
      self.__getattr__('comment'),
      TorrentMeta.__separator__(),
      'Encoding: ',
      self.__getattr__('encoding'),
      TorrentMeta.__separator__(),
      'Creation Date: ',
      str(self.__getattr__('creation_date')),
      TorrentMeta.__separator__(),
      'Created By: ',
      self.__getattr__('created_by')])

def main():

  t = TorrentMeta('./testfiles/mint.torrent')
  print t
  # print len(t)
  # print t.announce
  # print t.announce_list
  # print t.comment
  # print t.encoding
  # print t.creation_date
  # print t.created_by
  # print t[0]

  print '-------'

  # t = TorrentMeta('./testfiles/thriller.torrent')
  # print t
  # print len(t)
  # print t.announce
  # print t.announce_list
  # print t.comment
  # print t.encoding
  # print t.creation_date
  # print t.created_by

  # print '-------'

  for i in range(0,len(t)):
    print t[i]

if __name__ == '__main__':
    main()
    #unittest.main()