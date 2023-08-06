##Name

 jjcli - python module for command-line filter

##Synopsys

    jjcli skel     ## for a initial filter skeleton
    jjcli          ## for manual

   -- 

    from jjcli import *       ## re.* functions also imported
    c=clfilter(opt="do:")     ## options in c.opt;
                              ##    autostrip         (def=True)
                              ##    inplace           (def=False) 
                              ##    fs (for csvrow()) (def=",")

    for line in c.input():...    ## process one rstriped line at the time
    for txt in c.slurp():...     ## process one striped text at the time
       ## process txt            ##   (end of line spaces and \r also removed)
    for par in c.paragraph():... ## process one striped paragraph at the time
    for tup in c.csvrow():...    ## process one csv row at the time
    for tup in c.tsvrow():...    ## process one tsv row at the time

    c.lineno()                ## line number
    c.filelineno()
    c.parno()                 ## paragraph number
    c.fileparno()
    c.filename()              ## filename or "<stdin>"
    c.nextfile()
    c.isfirstline()

##Description

jjcli is a python module that tries to simplify the creation of
__unix__ filters by importing:

- getopt  (for command line options ans args)
- fileinput (for [files/stdin] arguments)
- re (regular expressions)
- csv  (for csv and tsv inputs)
- urllib.request (to deal with input argumens that are url)
- subprocess 

### regular expressions

    imports all functions from re.*
    Use re.I re.X re.S   for regexp flags

### subprocesses   (qx, qxlines, qxsystem)

    a=qx( "ls" )
    for x in qxlines("find | grep '\.jpg$'"): 
      ...
    qxsystem("vim myfile")

#### execute command return its stdout
    def qx(*x)      : return subprocess.getoutput(x)

#### execute command return its stdout lines
    def qxlines(*x) : return subprocess.getoutput(x).splitlines()

#### execute command -- system
    def qxsystem(*x): subprocess.call(x,shell=True)

### Other functions

    def slurpurlutf8(self,f):

    filename    = lambda s : F.filename()      # inherited from fileinput
    filelineno  = lambda s : F.filelineno()
    lineno      = lambda s : F.lineno()
    fileparno   = lambda s : s.fileparno_
    parno       = lambda s : s.parno_
    nextfile    = lambda s : F.nextfile()
    isfirstline = lambda s : F.isfirstline()
    close       = lambda s : F.close()

