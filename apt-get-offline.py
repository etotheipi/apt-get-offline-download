#! /usr/bin/python
import subprocess
import os
import shutil
from time import sleep
from sys import argv

if len(argv)<2:
   print 'Usage:  python %s <pkg1> [pkg2] [pkg3]...' % argv[0]
   exit(1)

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

dllist  = [out.split()[0][1:-1] for out in output]
filename= [out.split()[1] for out in output]
md5list = [out.split()[-1].split(':')[-1] for out in output]

dlscripttemplate = open('dlscripttemplate.py', 'r').readlines()
newdlcode = []
for line in dlscripttemplate:
   newdlcode.append(line)
   if 'INSERT DOWNLOAD LIST HERE' in line:
      newdlcode.append('dllist = [ \\\n')
      for url,outfile,md5sum in zip(dllist, filename, md5list):
         newdlcode.append('     ["%s", "%s", "%s"], \\\n' % (url,outfile,md5sum))
      newdlcode.append('         ]')
   

dlscript = os.path.join(outDir, 'download_script.py')
with open(dlscript, 'w') as f:
   f.writelines(newdlcode)

os.chmod(dlscript, 0775)


try:
   proc = subprocess.Popen(['python', os.path.basename(dlscript)], cwd=outDir)
   while proc.poll() == None:
      sleep(0.5)
except:
   raise





