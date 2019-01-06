# fabfile.py

import invoke
import fabric
import time
import hashlib

FRONTEND_LOCAL_DIRECTORY = "./components/frontend/dist"
DEPLOYMENT_TARGET_DIRECTORY = '/srv/http/occubrow'

BACKEND_LOCAL_DIRECTORY = "./components/backend"
BACKEND_TARGET_DIRECTORY = '/usr/local/lib/occubrow'


# because we can't combine rsync and sudo, we have to do this fairly silly
# rigmarole        
def deploy(context, source, target):
    temporary_path = generate_temporary_directory(context, target)
    print("About to run rsync")
    context.local(
        "rsync -avv --delete --exclude-from=exclude.rsf %s/ %s:%s/" \
        % (source, context.host, temporary_path)
    )
    print("Finished rsync")
    context.sudo("mkdir -p %s" % (target,))
    context.sudo("rsync -rtv --delete %s/ %s/" % (temporary_path, target))
    context.run("rm -rf %s" % temporary_path)

@invoke.task
def deploy_frontend(context):
    if not hasattr(context, 'host'):
        raise Exception('need to specify a host please')

    deploy(context, FRONTEND_LOCAL_DIRECTORY, DEPLOYMENT_TARGET_DIRECTORY)

@invoke.task
def deploy_backend(context):
    if not hasattr(context, 'host'):
        raise Exception('need to specify a host please')

    deploy(context, BACKEND_LOCAL_DIRECTORY, BACKEND_TARGET_DIRECTORY)


# algorithm copied from fabric core code for 'put' with 'use_sudo' kwargs
def generate_temporary_directory(context, remote_path):
    hasher = hashlib.sha1()
    hasher.update(context.host.encode('utf-8'))
    hasher.update(remote_path.encode('utf-8'))
    return hasher.hexdigest()