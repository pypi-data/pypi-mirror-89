import os
import glob
import tarfile
import tempfile

class tarball:
    """
    Manage tar balls accepting a manifest[] whose links we will resolve.
    """
    def __init__(self, manifest=[], VERBOSE=False):
        if VERBOSE:
            self.inputmanifest = manifest
        self.manifest = []
        list(map(lambda x: self.manifest.extend(glob.glob(x)), manifest))
        self.manifst = list(filter(os.path.exists, self.manifest))
        self.nameset()
        self.handleset()
        self.addcontent()

    def handleset(self):
        """
        tempfile.mktemp() is unsafe, so we will wrap it a little
        """
        while os.path.exists(self.tarname):
            self.nameset()
        self.tarhandle = tarfile.open(self.tarname, mode='w')

    def nameset(self):
        """
        Pick a name, any name, as long as it ends in '.tar'
        """
        self.tarname = tempfile.mktemp(suffix='.tar')

    def addcontent(self):
        """
        Add files then directories to our tarball.
        """
        list(map(lambda x: taradd(self.tarhandle, x), self.manifest))
        self.tarhandle.close()

def taradd(tarhandle, item):
    """
    Add items to the tarfile keeping only the outermost directory name.
    """
    startdir = os.path.abspath(os.getcwd())
    sourcedir = os.path.abspath(os.path.dirname(item))
    try:
        os.chdir(sourcedir)
        tarhandle.add(os.path.basename(item))
    except:
        pass
    os.chdir(startdir)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        manifest = sys.argv[1:]
    else:
        manifest = ['*.py', '../tests', '/not/a/real/file.txt']
    t = tarball(manifest=manifest, VERBOSE=True)
    print("%s described \n%s \n...and is in %s" % \
        (t.inputmanifest, str(t.manifest), t.tarname))
