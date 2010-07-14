#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

import af
import services.service

def usage_exit():
   print '\n\
examples:\n\
\n\
afjob path/scene.shk 1 100\n\
\n\
afjob path/scene.hip 1 100 -fpr 3 -pwd projects/test -node /out/mantra1 -take back -name my_job\n\
\n\
arguments:\n\
\n\
path/scene.shk       -   (R) scene, which file extension determinate run command and task type\n\
1                    -   (R) first frame to render\n\
100                  -   (R) last frame to render\n\
-by 1                -   frames increment\n\
-fpr 3               -   frames per render\n\
-pwd projects/test   -   working wirectory\n\
-name my_job         -   job name\n\
-node                -   node to render ( houdini driver or nuke write )\n\
-type                -   service type\n\
-take                -   take to use ( houdini render with take, xsi pass )\n\
-ignoreinputs        -   not to render input nodes ( houdini ignore inputs ROP parameter )\n\
-deletescene         -   delete scene when job deleted\n\
-pause               -   start job paused ( offline afanasy state )\n\
-os                  -   OS needed mask, "any" to render on any platform\n\
-hostsmask           -   job render hosts mask\n\
-hostsexcl           -   job render hosts to exclude mask\n\
-maxhosts            -   maximum number of hosts to use\n\
-maxruntime          -   maximum run time for task in seconds\n\
-priority            -   job priority\n\
-capacity            -   tasks capacity\n\
-capmin              -   tasks minimum capacity coefficient\n\
-capmax              -   tasks maximum capacity coefficient\n\
-depmask             -   wait untill other jobs of the same user, satisfying this mask\n\
-depglbl             -   wait untill other jobs of any user, satisfying this mask\n\
-images              -   images to preview\n\
-varirender attr start step count - variate parameter\n\
-simulate            -   enable simulation\n\
(R)                  -   REQUIRED arguments\n\
\n\
'
   sys.exit(1)

def error_exit( error_str):
   print error_str
   sys.exit(1)

argsv = sys.argv
argsl = len( argsv)

if argsl < 4:
   usage_exit()

scene = argsv[1]
ext   = scene.rpartition('.')[2]
name  = scene.rpartition('/')[2]

#
# initial arguments values

s = int( argsv[2])
e = int( argsv[3])
fpr = 1
by  = 1
pwd = os.getenv('PWD', os.getcwd())
file           = ''
node           = ''
ignoreinputs   = False
take           = ''
deletescene    = False
startpaused    = False
hostsmask      = ''
hostsexcl      = ''
maxruntime     = 0
maxhosts       = -1
priority       = -1
capacity       = -1
capmin         = -1
capmax         = -1
dependmask     = ''
dependglobal   = ''
images         = ''
blocktype      = ''
platform       = ''
varirender     = False
simulate       = False

cmd = ''
cmds = []
blocknames = []

#
# checking some critical argumens values

if s < 0:
   error_exit( 'invalid start frame')
if e < 0:
   error_exit( 'invalid end frame')

#
# getting arguments

for i in range( argsl):
   arg = argsv[i]

   if arg == '-s':
      i += 1
      if i == argsl: break
      s = int(argsv[i])
      continue

   if arg == '-e':
      i += 1
      if i == argsl: break
      e = int(argsv[i])
      continue

   if arg == '-by':
      i += 1
      if i == argsl: break
      by = int(argsv[i])
      continue

   if arg == '-fpr':
      i += 1
      if i == argsl: break
      fpr = int(argsv[i])
      continue

   if arg == '-pwd':
      i += 1
      if i == argsl: break
      pwd = argsv[i]
      continue

   if arg == '-file':
      i += 1
      if i == argsl: break
      file = argsv[i]
      continue

   if arg == '-name':
      i += 1
      if i == argsl: break
      name = argsv[i]
      continue

   if arg == '-node':
      i += 1
      if i == argsl: break
      node = argsv[i]
      continue

   if arg == '-take':
      i += 1
      if i == argsl: break
      take = argsv[i]
      continue

   if arg == '-deletescene':
      deletescene = True
      continue

   if arg == '-ignoreinputs':
      ignoreinputs = True
      continue

   if arg == '-pause':
      startpaused = True

   if arg == '-hostsmask':
      i += 1
      if i == argsl: break
      hostsmask = argsv[i]
      continue

   if arg == '-hostsexcl':
      i += 1
      if i == argsl: break
      hostsexcl = argsv[i]
      continue

   if arg == '-maxhosts':
      i += 1
      if i == argsl: break
      maxhosts = int(argsv[i])
      continue

   if arg == '-maxruntime':
      i += 1
      if i == argsl: break
      maxruntime = int(argsv[i])
      continue

   if arg == '-priority':
      i += 1
      if i == argsl: break
      priority = int(argsv[i])
      continue

   if arg == '-capacity':
      i += 1
      if i == argsl: break
      capacity = int(argsv[i])
      continue

   if arg == '-capmin':
      i += 1
      if i == argsl: break
      capmin = int(argsv[i])
      continue

   if arg == '-capmax':
      i += 1
      if i == argsl: break
      capmax = int(argsv[i])
      continue

   if arg == '-depmask':
      i += 1
      if i == argsl: break
      dependmask = argsv[i]
      continue

   if arg == '-depglbl':
      i += 1
      if i == argsl: break
      dependglobal = argsv[i]
      continue

   if arg == '-images':
      i += 1
      if i == argsl: break
      images = argsv[i]
      continue

   if arg == '-type':
      i += 1
      if i == argsl: break
      blocktype = argsv[i]
      continue

   if arg == '-os':
      i += 1
      if i == argsl: break
      platform = argsv[i]
      continue

   if arg == '-varirender':
      i += 1
      if i == argsl: break
      varirender_attr = argsv[i]
      i += 1
      if i == argsl: break
      varirender_start = int(argsv[i])
      i += 1
      if i == argsl: break
      varirender_step = int(argsv[i])
      i += 1
      if i == argsl: break
      varirender_count = int(argsv[i])
      varirender = True
      continue

   if arg == '-simulate':
      simulate = True
      continue
#
# command construction:
cmdextension = os.getenv('AF_CMDEXTENSION', '')

# Shake:
if   ext == 'shk':
   scenetype = 'shake'
   cmd = 'shake' + cmdextension + ' -exec ' + scene + ' -vv -t %1-%2'

# Nuke:
elif ext == 'nk':
   scenetype = 'nuke'
   cmd = 'nuke' + cmdextension + ' -i'
   if capmin != -1 or capmax != -1: cmd += ' -m '+ services.service.str_capacity
   if node != '':
      cmd += ' -X ' + node
   cmd += ' -x ' + scene + ' %1,%2'

# Houdini:
elif ext == 'hip':
   if node == '':
      error_exit( 'no houdini driver to render specified')
   scenetype = 'hbatch'
   cmd = 'hrender_af' + cmdextension
   if capmin != -1 or capmax != -1: cmd += ' --numcpus '+ services.service.str_capacity
   if ignoreinputs: cmd += ' -i'
   cmd += ' -s %%1 -e %%2 -b %(by)d -t %(take)s %(scene)s %(node)s' % vars()

# Maya:
elif ext == 'mb':
   scenetype = 'maya'
   cmd = 'maya' + cmdextension + ' -batch -file "' + scene + '" -command "afanasyBatch(%1,%2,1,1)"'

# XSI:
elif ext == 'scn':
   scenetype = 'xsi'
   cmd = os.environ['XSI_CGRU_PATH']
   cmd = os.path.join( cmd, 'afrender.py')
   cmd = 'xsibatch' + cmdextension + ' -script %s' % cmd
   cmd += ' -lang Python -main afRender -args'
   cmd += ' -scene %s' % scene
   cmd += ' -start %1 -end %2 -step ' + str(by)
   cmd += ' -simulate'
   if simulate:   cmd += ' 1'
   else:          cmd += ' 0'
   if take != '': cmd += ' -renderPass ' + take
   if varirender:
      cmd += ' -attr ' + varirender_attr + ' -value '
      value = varirender_start
      for i in range( 0, varirender_count):
         cmds.append( cmd + str(value))
         blocknames.append( 'variant[%d]' % value)
         value += varirender_step
      cmd = ''

#xsibatch -script "%XSI_CGRU_PATH%\afrender.py" -lang Python -main afRenderCurPass -args
#-scenePath "%CD%\project\Scenes\scene.scn" -startFrame 1 -endFrame 2 -step 1 -simulate 0 -setAttr torus.polymsh.geom.enduangle -setValue 120

# simple generic:
else:
   scenetype = 'generic'
   cmd = scene + ' %1 %2'

if fpr < 1:
  print 'fpr - frames per render - must be > 0 ( setting to 1)'
  fpr = 1;

#
# Creating a Job:

# Create a Block(s) af first:
blocks = []
blockname = node
if blockname == '': blockname = scenetype
if blocktype == '': blocktype = scenetype
if len( cmds) == 0:
   cmds.append( cmd)
   blocknames.append( blockname)
i = 0   
for cmd in cmds:
   block = af.Block( blocknames[i], blocktype)
   block.setWorkingDirectory( pwd )
   block.setNumeric( s, e, fpr)
   block.setCommand( cmd )
   block.setCapacity( capacity)
   block.setVariableCapacity( capmin, capmax)
   if maxruntime != 0: block.setTasksMaxRunTime( maxruntime)
   if images != '': block.setFiles( images)
   blocks.append( block)
   i += 1

# Create a Job:
job = af.Job( name)
job.setPriority( priority)
if maxhosts       != -1: job.setMaxHosts( maxhosts)
if hostsmask      != '': job.setHostsMask( hostsmask)
if hostsexcl      != '': job.setHostsMaskExclude( hostsexcl)
if dependmask     != '': job.setDependMask( dependmask)
if dependglobal   != '': job.setDependMaskGlobal( dependglobal)
if deletescene         : job.setCmdPost('rm ' + scene)
if startpaused         : job.offLine()
if platform != '':
   if platform == 'any': job.setNeedOS('')
   else: job.setNeedOS( platform)

# Add a Block to a Job:
job.blocks.extend( blocks)

# Send Job to server:
job.send()
