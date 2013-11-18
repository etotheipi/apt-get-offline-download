#! /usr/bin/python
import subprocess
import os
import shutil
from time import sleep
from sys import argv

if len(argv)<2:
   print 'Usage:  python %s <pkg1> [pkg2] [pkg3]...' % argv[0]
   exit(1)


def execAllDownloads():

   pkgs = argv[1:]
   outDir = 'download'
   for i in range(2):
      if i < len(pkgs):
         outDir += '_' + pkgs[i][:8] 
      else:
         break
         
   print 'Going to put downloaded packages into directory: %s' % outDir
   
   if os.path.exists(outDir):
      doDelete = raw_input('Directory %s already exists; delete it? [Y/n] ' % outDir)
      if doDelete.lower().startswith('y'):
         shutil.rmtree(outDir)
   
   if not os.path.exists(outDir):
      os.makedirs(outDir)
   
   cmd = ['apt-get', 'install', '--yes', '--print-uris']
   cmd.extend(pkgs)
   output = subprocess.check_output(cmd).split('\n')
   output = filter(lambda x: x.startswith("'"), output)
   
   dllist    = [out.split()[0][1:-1] for out in output]
   filenames = [out.split()[1] for out in output]
   md5list   = [out.split()[-1].split(':')[-1] for out in output]
   
      
   newscript = os.path.join(outDir, 'download_script.py')
   writeScriptWithHardcodedPaths(dllist, filenames, md5list, newscript)
   
   
   try:
      proc = subprocess.Popen(['python', os.path.basename(newscript)], cwd=outDir)
      while proc.poll() == None:
         sleep(0.5)
   except:
      raise
   
   
   print 'All packages finished downloading successfully to', outDir


# Write out the complete download script
def writeScriptWithHardcodedPaths(dllist, filenames, md5list, newdlpath):
   
   newdlfile = open(newdlpath, 'w')
   newdlfile.write( """#! /usr/bin/python
import subprocess
import os
import shutil
import urllib2
import hashlib
from sys import argv, stdout
""")
   
   newdlfile.write('dllist = [ \\\n')
   for url,outfile,md5sum in zip(dllist, filenames, md5list):
      newdlfile.write('     ["%s", "%s", "%s"], \\\n' % (url,outfile,md5sum))
   newdlfile.write('         ]\n')


   newdlfile.write( """

def md5file(fn):
   f = open(fn, 'rb')
   filecontents = f.read()
   f.close()
   return hashlib.md5(filecontents).hexdigest()
   


try: 
   for url,dlfile,md5 in dllist:

      print '   Downloading %s...' %dlfile,
      stdout.flush()
      urlobj = urllib2.urlopen(url, timeout=10)
      
      with open(dlfile,'wb') as downloadingFile:
         downloadingFile.write(urlobj.read())
      
      print 'checking MD5 hash...',
      stdout.flush()

      hashedfile = md5file(dlfile)
      if not md5==hashedfile:
         print '***ERROR: MD5sum does not match!' 
         print '          Downloaded: ', hashedfile
         print '          Expected  : ', md5
         raise
      print 'done.'
      stdout.flush()
except:

   for f in [row[1] for row in dllist]:
      if os.path.exists(f):
         os.remove(f)

   print '***ERROR: Failed downloading files'
   print 'Reraising previous error'
   raise

""")

   newdlfile.close()
   os.chmod(newdlpath, 0775)


if __name__ == '__main__':
   execAllDownloads()



