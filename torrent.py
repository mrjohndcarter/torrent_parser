'''
file: torrent.py
author: jcarter
description: 
  - parses a bit torrent file
  - provides access to all attributes of the torrent meta, and contained files.
  - provides iterator over the contained files
notes:
  - assumes single file/multifile is 'well formed'  i.e. -- a single file is not 
  represented as a multifile representation of len 1.
  - doesn't parse pieces/piece hashes.
'''

from bencode_decoder import beparse

# maps between attribute names and dictionary keys parsed from the file

meta_attributes = {
                  'announce' : 'announce',
                  'announce_list' : 'announce-list',
                  'comment' : 'comment',
                  'created_by' : 'created by',
                  'creation_date' : 'creation date',
                  'encoding' : 'encoding'
                  }
file_attributes = {
                  'name' : 'name',
                  'length' : 'length',
                  'md5sum' : 'md5sum',
                  'path' : 'path'
                  }

# a file contained in a torrent

class TorrentFile:
  def __init__(self,meta_file,index):
    self.meta = meta_file # the torrent meta file that contains this file
    self.index = index # the index of this file within torrent meta file

  # for readabilities sake
  @classmethod
  def __join_path__(klass,l):
    return '/'.join(l)

  # builds a full path to the filename with available components
  def filename(self):
    if self.meta.single_file_mode:
      return self.meta.torrent_dict['info']['name']
    elif len(self.meta.torrent_dict.get('name','')) == 0:
      return TorrentFile.__join_path__(self.__getattr__('path'))
    else:
      return '/'.join([self.meta.torrent_dict.get('name',''),TorrentFile.__join_path__(self.__getattr__('path'))])

  # attribute access
  def __getattr__(self,name):
    if name not in file_attributes:
      raise KeyError
    if self.meta.single_file_mode:
      return self.meta.torrent_dict['info'].get(name,'')
    elif name == 'length':
      return int(self.meta.torrent_dict['info']['files'][self.index].get('length',0))
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

# a torrent meta file

class TorrentMeta:
  def __init__(self,filename):
    self.torrent_dict = beparse(open(filename).read())
    if 'files' in self.torrent_dict['info']:
      self.single_file_mode = False
    else:
      self.single_file_mode = True

  # number of files described in the torrent file
  def __len__(self):
    if not self.torrent_dict:
      return 0;
    if self.single_file_mode:
      return 1
    else:
      return len(self.torrent_dict['info']['files'])

  # attribute access
  def __getattr__(self, name):
    if not self.torrent_dict:
      raise KeyError
    if name == 'announce_list':
      return TorrentMeta.__flatten_list__(self.torrent_dict.get('announce-list',[]))
    elif name == 'creation_date':
      return int(self.torrent_dict.get('creation date',0))
    elif name in meta_attributes:
      return self.torrent_dict.get(meta_attributes[name],'')
    else:
      raise KeyError

  # access to files in torrent
  def __getitem__(self, key):
    if not self.torrent_dict or (key < 0) or (key >= self.__len__()):
      raise KeyError
    return TorrentFile(self,key)

  # returns an iterator for this meta file
  def __iter__(self):
    return TorrentIterator(self.__len__(),self)

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

# torrent meta iterator (iterates over files)

class TorrentIterator:
  def __init__(self,count,meta_file):
    self.count = count
    self.current = 0
    self.meta_file = meta_file

  def next(self):
    if self.current >= self.count:
      raise StopIteration
    else:
      self.current += 1
      return self.meta_file[self.current-1]