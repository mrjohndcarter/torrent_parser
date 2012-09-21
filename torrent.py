# file: torrent.def
# author: jcarter
# desciption: class to parse a bit torrent file
#
# Please use Python 2.7 to perform the following task:
# Write a re-usable library to parse BitTorrent files. The library should expose 
# at least the following pieces of information (when available in the file):
# - creation date
# - client that created the file
# - the tracker URL
# - the name, length, and checksum of each file described in the torrent
# 
# No third-party libraries should be used for this project, only the Python standard library.

import string
import re

def beparse_string(matched,stream):
  length = int(string.split(matched,':',1)[0])
  return stream[len(matched):len(matched)+length],stream[len(matched)+length:]

def beparse_int(matched,stream):
  int_pattern = '(i)(\d+)(e)'
  matched = re.search(int_pattern,stream)
  data = int(matched.group(2))
  stream = re.sub(('i%lde' % data),'',stream,1)
  return (data,stream)

def beparse(stream):

  class Parse_State:
    open_dict = 'd'
    open_list = 'l'

  chunk_start_pattern = "(\d+:)|(i\d+e)|(l)|(d)|(e)"
  matched = re.search(chunk_start_pattern,stream)
  build_stack = []
  type_stack = []

  while (matched):
    if (matched.group(1)): # string
      s,stream = beparse_string(matched.group(1),stream)
      print s
      if not build_stack:
        print 'Toplevel variable: ' + str(s)
        system.exit(0)
      build_stack[-1].append(s)

    if (matched.group(2)): # int
      i,stream = beparse_int(matched.group(2),stream)
      print i
      if not build_stack:
        print 'Toplevel variable: ' + str(s)
        system.exit(0)
      build_stack[-1].append(i)

    if (matched.group(3)): # list
      # push a new list on the build stack
      # push the type on the type stack
      stream = stream[1:]
      build_stack.append([])
      type_stack.append(Parse_State.open_list)
    
    if (matched.group(4)): # dict
      # push a new list on the build stack
      # push the type on the type stack
      # we build a dict from the list on closing
      stream = stream[1:]
      build_stack.append([])
      type_stack.append(Parse_State.open_dict)

    if (matched.group(5)):
      stream = stream[1:]
      temp_element = build_stack.pop();
      type_element = type_stack.pop();

      # we need to build a dict from the list
      if type_element is Parse_State.open_dict:
        temp_element = dict(zip(temp_element[::2], temp_element[1::2])) # from python cookbook

      # once we have an empty build stack, we've closed the top level element
      if not build_stack and len(stream) > 0:
        raise SyntaxError('Extrananeous elements in file: ' + stream)
      if not build_stack:
        return temp_element;
        
      build_stack[-1].append(temp_element)

    matched = re.search(chunk_start_pattern,stream)

  # if we're here, there's something we could not parse  
  raise SyntaxError('Malformed file: ' + stream)

def main():

  raw = open('Linux Mint 13 KDE (x86-64) Live USB.torrent').read()
  c = beparse(raw);
  print c
  #beparse('8:announce')

if __name__ == '__main__':
    main()
    #unittest.main()