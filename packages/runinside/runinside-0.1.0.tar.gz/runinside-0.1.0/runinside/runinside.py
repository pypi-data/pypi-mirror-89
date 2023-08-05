"""Main module."""

import sys
import docker
import docker.errors
import os
try:
    import runinside.tarprep as tarprep
except:
    import tarprep
import warnings
warnings.filterwarnings("ignore")

DOCKER = docker.client.DockerClient(base_url=os.environ.get("DOCKER_API"))

class runinside:
    def __init__(self, container=None, manifest=None, destination='/', command=None):
        self.healthy = False
        if 'containers.Container' in str(type(container)):
            self.container = container
        elif type(container) == str:
            try:
                self.container = DOCKER.containers.get(container)
            except:
                print("No such container as %s !" % (str(container)))
                self.container = None
        else:
            self.container = None
        if manifest:
            self.t = tarprep.tarball(manifest)
        else:
            self.t = None
        if self.t and self.container:
            if cp(self.container, destination, self.t.tarname):
                os.unlink(self.t.tarname)
                self.healthy = True
            else:
                self.healthy = False
        else:
            self.healthy = True
        if self.healthy and self.container and command:
            self.out = self.container.exec_run(['sh', '-c', command])
        else:
            self.out = ''
        

def cp(container, destination, tarname):
    """
    The Docker people said they would not implement "cp" at the API level.
    So, we live with what we have.
    """
    try:
        with open(tarname, 'rb') as tarhandle:
            container.put_archive(destination, tarhandle)
        return(True)
    except Exception as e:
        print(e)
        return(False)

if __name__ == '__main__':
    container = DOCKER.containers.list()[0]
    manifest = ['*.py', '../tests', '/not/a/real/file.txt']
    command="date | grep ':'; ls /"
    r = runinside(container=container, manifest=manifest, command=command)
    try:
        o = r.out.output.decode('utf-8')
        print(o)
    except:
        print("No output.")
    print("Done.")
