#!/usr/bin/env python
import glob
import json
import os
import shutil
import sys
import urllib
from functools import reduce
from subprocess import Popen, PIPE

try:
    git_url = 'https://api.github.com/repos/git/git/tags'
    git_tags = json.loads(urllib.urlopen(git_url).read())

    git_versions = [x['name'].split('.') for x in git_tags if x['name'].find('-rc') == -1]

    git_current = '.'.join(reduce(lambda x, y: x if x[0] >= y[0] else x if x[1] >= y[1] else x if x[2] >= y[2] else y, git_versions))

    git_tar = reduce(lambda x, y: x if x['name'] == git_current else y, git_tags)['tarball_url']

    print 'fetching latest git verstion %s' % git_current
    urllib.urlretrieve(git_tar, 'git.tar.gz')

    shutil.rmtree('git', ignore_errors=True)
    os.mkdir('git')

    print 'unpacking git'
    p = Popen(['tar', '-zvxf', 'git.tar.gz', '-C', 'git'], stdout=PIPE, stderr=PIPE)

    (stdout, stderr) = p.communicate()
    print stderr

    print 'configuring git'
    os.chdir(glob.glob('git/*')[0])
    p = Popen(['make', 'configure'], stdout=PIPE, stderr=PIPE)
    (stdout, stderr) = p.communicate()
    p = Popen(['./configure', '--prefix=/usr/local'], stdout=PIPE, stderr=PIPE)
    (stdout, stderr) = p.communicate()
    print stderr

    print 'compiling git'
    p = Popen(['make', '-j8'], stdout=PIPE, stderr=PIPE)
    (stdout, stderr) = p.communicate()
    print stderr

    print 'installing git'
    p = Popen(['make', 'install'], stdout=PIPE, stderr=PIPE)
    (stdout, stderr) = p.communicate()
    print stderr

    version_file = '/version.txt'
    print 'creating %s' % version_file
    with open(version_file, 'w') as fh:
        fh.write(git_current)

except:
    print 'Unexpected error:'
    print sys.exc_info()
