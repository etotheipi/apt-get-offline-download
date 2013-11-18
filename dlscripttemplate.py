#! /usr/bin/python
import subprocess
import os
import shutil
import urllib2
import hashlib
from sys import argv

# dllist = [ [url, outfile, md5], [url, outfile, md5], ... ]
##### INSERT DOWNLOAD LIST HERE #####


def md5file(fn):
   f = open(fn, 'rb')
   filecontents = f.read()
   f.close()
   return hashlib.md5(filecontents).hexdigest()
   


try: 
   for url,dlfile,md5 in dllist:

      urlobj = urllib2.urlopen(url, timeout=10)
      
      with open(dlfile,'wb') as downloadingFile:
         downloadingFile.write(urlobj.read())
      

      hashedfile = md5file(dlfile)
      if not md5==hashedfile:
         print '***ERROR: MD5sum does not match!' 
         print '          Downloaded: ', hashedfile
         print '          Expected  : ', md5
         raise
except:

   for f in [row[1] for row in dllist]:
      if os.path.exists(f):
         os.remove(f)

   print '***ERROR: Failed downloading files'
   print 'Reraising previous error'
   raise
