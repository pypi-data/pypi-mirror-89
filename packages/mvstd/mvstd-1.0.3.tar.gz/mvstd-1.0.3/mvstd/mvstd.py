import sys
import os
import re
import argparse
from math import log10

def has_ext(filename, ext):
  """
  >>> has_ext('test.mp3',['opus','mp3','aac'])
  True
  >>> has_ext('test.mp4',['opus','mp3','aac'])
  False
  >>> has_ext('test.opus.gz',['opus','mp3','aac'])
  False
  >>> has_ext('test.1.OPUS',['opus','mp3','aac'])
  True
  """

  return filename.split('.')[-1].lower() in ext

def is_audio(f): return has_ext(f, ['opus','mp3','aac','m4a','ogg'])
def is_video(f): return has_ext(f, ['mp4','avi','mov','mkv'])
def is_image(f): return has_ext(f, ['png','jpeg','jpg'])
def is_media(f): return is_audio(f) or is_video(f) or is_image()

def normalize(filename):
  """
  >>> normalize('Test 1.txt')
  'test-1.txt'
  >>> normalize('another-TEst_file.mp4')
  'another-test-file.mp4'
  >>> normalize('Linkin Park - In the End -.opus')
  'linkin-park-in-the-end.opus'
  >>> normalize('calvin&hobbes.pdf')
  'calvin-hobbes.pdf'
  >>> normalize('2019-10-11 07.08.09[family photo].jpg')
  '2019-10-11T070809-family-photo.jpg'
  >>> normalize('2010-01-12 03.04.05 some nature.jpg')
  '2010-01-12T030405-some-nature.jpg'
  >>> normalize('2010-01-12T030405-some-nature.jpg')
  '2010-01-12T030405-some-nature.jpg'
  >>> normalize('2010-01-12 03.04.05.jpg')
  '2010-01-12T030405.jpg'
  """
  
  path = filename.split('/')[:-1]
  filename = filename.split('/')[-1]

  filename = filename.lower().replace('_','-').replace(' ','-').replace('–','-')

  d = re.search(
    "^"
    "(?P<year>\d{4})[\-]?"
    "(?P<month>\d{2})[\-]?"
    "(?P<day>\d{2})[Tt \-]?"
    "(?P<hour>\d{2})[\.\:\- ]?"
    "(?P<minute>\d{2})[\.\:\- ]?"
    "(?P<second>\d{2})",
    filename)

  if d:
      filename = filename.replace(d.group(0),
        f"{d['year']}-{d['month']}-{d['day']}T{d['hour']}{d['minute']}{d['second']}-")

  if is_audio(filename):
    filename = re.sub(r'[\(\[].*?[\)\]]','', filename) # Remove parentheticals

  filename = re.sub('[\[\(\)\]\-\&]+','-', filename)
  words = filename.split('-')

  filename = '-'.join(words)

  filename = re.sub(r'[\'\!\:\,]','', filename)

  filename = re.sub(r'-+\.+','.', filename)

  filename = re.sub(r'\-+','-', filename)

  return '/'.join(path + [filename])

def zfill(i, maxval):
    """
    Zero fills a number with enough zeroes to ensure all items are the same 
    length

    >>> zfill(1, 299)
    '001'

    >>> zfill(0, 999)
    '000'

    >>> zfill(3, 10)
    '03'

    >>> zfill(101, 48591)
    '00101'
    """
    
    return str(i).zfill(int(log10(maxval)+1))

def get_numeric_name(filename, i, maxval):
    """
    Returns numeric name for a file

    >>> get_numeric_name("test/img.jpg", 13, 356)
    'test/013.jpg'

    >>> get_numeric_name("test/next/photo.jpg", 4, 7)
    'test/next/4.jpg'

    >>> get_numeric_name("test/dir/readme", 113, 9987)
    'test/dir/0113'

    >>> get_numeric_name("test/doc.md", 2, 14)
    'test/02.md'

    >>> get_numeric_name("doc.md", 6, 101)
    '006.md'
    """

    path = filename.split('/')[:-1]
    filename = filename.split('/')[-1]
    extension = filename.split('.')[-1]

    new_name = zfill(i, maxval)

    if extension != filename:
        new_name += '.' + extension

    return '/'.join(path + [new_name])

def main():
    ap = argparse.ArgumentParser(description='Rename files to a standard format')
    ap.add_argument('files', nargs='+', help="List of files")
    ap.add_argument('--numeric', '-n', action="store_true", help="Rename file numerically after sorting alphabetically")
    ap.add_argument('--reverse', '-r', action="store_true", help="Reverse sort order prior to renaming")
    args = ap.parse_args()

    files = sorted(args.files, reverse=args.reverse)

    for i,filename in enumerate(files):
        if args.numeric:
            os.rename(filename, get_numeric_name(filename, i, len(files)))
        else:
            os.rename(filename, normalize(filename))
