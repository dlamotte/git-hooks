'''
githooks.py

Single point of entry and shared library for git-hooks.
'''

import errno
import os
import sys

GIT_COMMIT_TMP_SUFFIX = '.githooks-tmp'

def call_hook(hook):
    method_name = hook.replace('-', '_')
    method = globals().get(method_name)

    if method is not None:
        return method()

    return 0

def commit_msg():
    '''
    Actions:
        - compare commit message body to original and exit non-zero if
          unchanged
        - unlink temporary commit message body
    '''
    try:
        # fn = commit filename
        fn = sys.argv[1]

        with open(fn, 'r+') as fp:
            try:
                with open(fn + GIT_COMMIT_TMP_SUFFIX) as tmpfp:
                    if fp.read() == tmpfp.read():
                        fp.seek(0)
                        fp.truncate(0)
            except IOError as exc:
                if errno.ENOENT != exc.errno:
                    raise
    finally:
        try:
            os.unlink(fn + GIT_COMMIT_TMP_SUFFIX)
        except OSError as exc:
            if exc.errno != errno.ENOENT:
                raise

    return 0

def prepare_commit_msg():
    '''
    Actions:
        - if JIRA_ISSUE is in the environment, it prefixes the commit message
          with the JIRA_ISSUE defined in the environment variable
    '''
    # fn = commit filename
    fn = sys.argv[1]

    # type = commit type
    type = None
    if len(sys.argv) == 3:
        type = sys.argv[2]

    # sha = commit sha-1 (if this is an amended commit)
    sha = None
    if len(sys.argv) == 4:
        sha = sys.argv[3]

    with open(fn, 'r+') as fp:
        body = origbody = open(fn).read()

        if 'JIRA_ISSUE' in os.environ:
            body = os.environ['JIRA_ISSUE'] + ': ' + body

        if body != origbody:
            with open(fn + GIT_COMMIT_TMP_SUFFIX, 'w') as tmpfp:
                tmpfp.write(body)

            fp.seek(0)
            fp.truncate(0)
            fp.write(body)

    return 0
