# file: bdecode.py
# author: jcarter
# description: basic bencode decoder

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
      if not build_stack:
        raise SyntaxError('Toplevel string variable:' + s)
      build_stack[-1].append(s)

    if (matched.group(2)): # int
      i,stream = beparse_int(matched.group(2),stream)
      if not build_stack:
        raise SyntaxError('Toplevel int variable:' + str(i))
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