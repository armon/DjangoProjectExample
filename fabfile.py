# Fabric configuration file for automated deployment
# Mostly from: http://lethain.com/entry/2008/nov/04/deploying-django-with-fabric/
#
import subprocess
from fabric.api import run, sudo, put, env, require, local, settings

# The git origin is where we the repo is.
# Use the user@host syntax
GIT_ORIGIN = "git@github.com"

# The git repo is the repo we should clone
GIT_REPO = "armon/DjangoProjectExample.git"

# The hosts we need to configure
HOSTS = ["ec2-107-20-11-199.compute-1.amazonaws.com"]

# These are the packages we need to install using APT
INSTALL_PACKAGES = [
            "ntp",
            "python2.6",
            "python2.6-dev",
            "libxml2-dev",
            "libxslt1-dev",
            "python-libxml2",
            "python-setuptools",
            "git-core",
            "build-essential",
            "libxml2-dev",
            "libpcre3-dev",
            "libpcrecpp0",
            "libssl-dev",
            "zlib1g-dev",
            "libgeoip-dev",
            "memcached",
            "libmemcached-dev",
            "python-mysqldb",
            "libmysqlclient16-dev"
           ]

#### Environments

def production():
  "Setup production settings"
  env.hosts = HOSTS
  env.repo = ("env.example.com", "origin", "release")
  env.virtualenv, env.parent, env.branch = env.repo
  env.base = "/server"
  env.user = "ubuntu"
  env.git_origin = GIT_ORIGIN
  env.git_repo = GIT_REPO
  env.dev_mode = False
  env.key_filename = "config/aws/testdjango.pem"


def staging():
  "Setup staging settings"
  env.hosts = HOSTS
  env.repo = ("env.stage.example.com", "origin", "stage")
  env.base = "/server"
  env.virtualenv, env.parent, env.branch = env.repo
  env.user = "ubuntu"
  env.git_origin = GIT_ORIGIN
  env.git_repo = GIT_REPO
  env.dev_mode = False
  env.key_filename = "config/aws/testdjango.pem"


def vagrant():
  "Setup local vagrant instance"
  raw_ssh_config = subprocess.Popen(["vagrant", "ssh-config"], stdout=subprocess.PIPE).communicate()[0]
  ssh_config = dict([l.strip().split() for l in raw_ssh_config.split("\n") if l])
  env.repo = ("env.example.com", "origin", "master")
  env.virtualenv, env.parent, env.branch = env.repo
  env.base = "/server"
  env.user = ssh_config["User"]
  env.hosts = ["127.0.0.1:%s" % (ssh_config["Port"])]
  env.key_filename = ssh_config["IdentityFile"]
  env.git_origin = GIT_ORIGIN
  env.git_repo = GIT_REPO
  env.dev_mode = True


#### Vagrant

def setup_vagrant():
  "Bootstraps the Vagrant environment"
  require('hosts', provided_by=[vagrant])
  sub_stop_processes()   # Stop everything
  sub_install_packages() # Get the installed packages
  sub_build_packages()   # Build some stuff
  sub_get_virtualenv()   # Download virtualenv
  sub_make_virtualenv()  # Build the virtualenv
  sub_vagrant_link_project() # Links the project in
  sub_get_requirements() # Get the requirements (pip install)
  sub_get_admin_media()  # Copy Django admin media over
  sudo("usermod -aG vagrant www-data") # Add www-data to the vagrant group
  sub_copy_memcached_config() # Copies the memcache config
  sub_start_processes()  # Start everything


def dev_server():
  "Initializes the django development server (Vagrant)"
  require('hosts', provided_by=[vagrant])

  # Kill all the screen sessions
  with settings(warn_only=True):
    run("ps auxH | grep python | grep runserver | awk '{ print $2 }' | xargs kill")

  # Make manage executable
  run("chmod +x %(base)s/%(virtualenv)s/project/project/manage.py" % env)

  # Run the Django runserver
  run("source %(base)s/%(virtualenv)s/bin/activate; %(base)s/%(virtualenv)s/project/project/manage.py runserver 0.0.0.0:8000" % env)


def sub_vagrant_link_project():
  "Links the project into the virtual env"
  run("if [ ! -d %(base)s/%(virtualenv)s/project ]; then ln -f -s /project %(base)s/%(virtualenv)s/project; fi" % env)


def default_project():
  "For the purposes of our example project, we will initialize a blank django project"
  run("source %(base)s/%(virtualenv)s/bin/activate; cd %(base)s/%(virtualenv)s/project/; django-admin.py startproject project" % env)


### End Vagrant


#### Cutting releases

def cut_staging():
  "Cuts the staging branch"
  local("git checkout stage; git merge master; git push; git checkout master;")

def cut_release():
  "Cuts the release branch"
  local("git checkout release; git merge stage; git push; git checkout master;")


####


#### Host Bootstrapping

def bootstrap():
  "Bootstraps the dreamhost environment"
  require('hosts', provided_by=[staging, production])
  sub_stop_processes() # Stop everything
  sub_install_packages() # Get the installed packages
  sub_build_packages()   # Build some stuff
  sub_get_virtualenv()   # Download virtualenv
  sub_make_virtualenv()  # Build the virtualenv
  sub_setup_ssh()        # Copy the SSH keys over
  sub_git_clone()        # Checkout the repo
  sub_get_requirements() # Get the requirements (pip install)
  sub_get_admin_media()  # Copy Django admin media over
  sub_copy_memcached_config() # Copies the memcache config
  sub_start_processes()  # Start everything


def sub_install_packages():
  "Installs necessary packages on host"
  sudo("apt-get update")
  package_str = " ".join(INSTALL_PACKAGES)
  sudo("apt-get -y install "+package_str)
  sudo("easy_install pip")

def sub_build_packages():
  "Build some of the packages we need"
  sub_build_uwsgi()
  sub_build_nginx()

def sub_build_uwsgi():
  "Builds uWSGI"
  sudo("mkdir -p /usr/src/uwsgi")
  sudo("""cd /usr/src/uwsgi; if [ ! -e uwsgi-1.2.3.tar.gz ]; then \
       wget 'http://projects.unbit.it/downloads/uwsgi-1.2.3.tar.gz'; \
       tar xfz uwsgi-1.2.3.tar.gz; \
       cd uwsgi-1.2.3; \
       make; \
       cp uwsgi /usr/local/sbin;
       fi""")
  put("config/uwsgi.conf","/etc/init/uwsgi.conf",use_sudo=True)

def sub_build_nginx():
  "Builds NginX"
  sudo("mkdir -p /usr/src/nginx")
  sudo("""cd /usr/src/nginx; if [ ! -e nginx-1.2.0.tar.gz ]; then
       wget 'http://nginx.org/download/nginx-1.2.0.tar.gz' ; \
       tar xfz nginx-1.2.0.tar.gz; \
       cd nginx-1.2.0/; \
       ./configure --pid-path=/var/run/nginx.pid \
       --conf-path=/etc/nginx/nginx.conf \
       --sbin-path=/usr/local/sbin \
       --user=www-data \
       --group=www-data \
       --http-log-path=/var/log/nginx/access.log \
       --error-log-path=/var/log/nginx/error.log \
       --with-http_stub_status_module \
       --with-http_ssl_module \
       --with-http_realip_module \
       --with-sha1-asm \
       --with-sha1=/usr/lib \
       --http-fastcgi-temp-path=/var/tmp/nginx/fcgi/ \
       --http-proxy-temp-path=/var/tmp/nginx/proxy/ \
       --http-client-body-temp-path=/var/tmp/nginx/client/ \
       --with-http_geoip_module \
       --with-http_gzip_static_module \
       --with-http_sub_module \
       --with-http_addition_module \
       --with-file-aio \
       --without-mail_smtp_module; make ; make install;
       fi
       """)
  sudo("mkdir -p /var/tmp/nginx; chown www-data /var/tmp/nginx")
  put("config/nginx.conf","/etc/init/nginx.conf",use_sudo=True)
  sudo("cd /etc/nginx; mkdir -p sites-available sites-disabled sites-enabled")
  copy_nginx_config()


def copy_nginx_config():
  "Copies the NginX config over"
  put("config/nginx/backends.conf","/etc/nginx/backends.conf",use_sudo=True)
  put("config/nginx/nginx.conf","/etc/nginx/nginx.conf",use_sudo=True)
  put("config/nginx/example.com","/etc/nginx/sites-available/",use_sudo=True)
  sudo("ln -f -s /etc/nginx/sites-available/example.com /etc/nginx/sites-enabled/example.com")
  if env.dev_mode:
    put("config/nginx/dev.example.com","/etc/nginx/sites-available/",use_sudo=True)
    sudo("ln -f -s /etc/nginx/sites-available/dev.example.com /etc/nginx/sites-enabled/dev.example.com")


def sub_get_virtualenv():
  "Fetches the virtualenv package"
  run("if [ ! -e virtualenv-1.7.1.2.tar.gz ]; then wget http://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.7.1.2.tar.gz; fi")
  run("if [ ! -d virtualenv-1.7.1.2 ]; then tar xzf virtualenv-1.7.1.2.tar.gz; fi")
  run("rm -f virtualenv")
  run("ln -s virtualenv-1.7.1.2 virtualenv")


def sub_make_virtualenv():
  "Makes the virtualenv"
  sudo("if [ ! -d %(base)s ]; then mkdir -p %(base)s; chmod 777 %(base)s; fi" % env)
  run("if [ ! -d %(base)s/%(virtualenv)s ]; then python ~/virtualenv/virtualenv.py --no-site-packages %(base)s/%(virtualenv)s; fi" % env)
  sudo("chmod 777 %(base)s/%(virtualenv)s" % env)


def sub_setup_ssh():
  "Setup the ssh hosts file and keys"
  run("mkdir -p ~/.ssh/")
  put("config/id_rsa", "/home/%(user)s/.ssh/id_rsa" % env, mode=0600)
  put("config/id_rsa.pub", "/home/%(user)s/.ssh/id_rsa.pub" % env, mode=0600)
  put("config/known_hosts", "/home/%(user)s/.ssh/known_hosts" % env, mode=0600)



def sub_git_clone():
  "Clones a repository into the virtualenv at /project"
  run("cd %(base)s/%(virtualenv)s; git clone %(git_origin)s:%(git_repo)s project; cd project; git checkout %(branch)s; git pull %(parent)s %(branch)s" % env)

def sub_get_requirements():
  "Gets the requirements for the project"
  sudo("cd %(base)s/%(virtualenv)s; source bin/activate; pip install -r project/requirements.txt" % env)


def sub_get_admin_media():
  "Copies over the required admin media files"
  run("cd %(base)s/%(virtualenv)s/project/public/media; if [ ! -d admin-media ]; then cp -R %(base)s/%(virtualenv)s/lib/python2.6/site-packages/django/contrib/admin/media admin-media; fi" % env)

def sub_copy_memcached_config():
  "Copies the memcached config files over"
  put("config/memcached.conf","/etc/memcached.conf",use_sudo=True)

def sub_start_processes():
  "Starts NginX and uWSGI"
  sudo("start nginx")
  sudo("start uwsgi")
  sudo("nohup /etc/init.d/memcached restart")

def sub_stop_processes():
  "Stops Nginx and uWSGI"
  with settings(warn_only=True):
    sudo("stop nginx")
    sudo("stop uwsgi")
    sudo("/etc/init.d/memcached stop")


####

#### Deploying new version

def syncdb():
  "Does a synbdb and a migrate"
  require('hosts', provided_by=[vagrant, staging, production])
  sudo("chmod -R 777 %(base)s/%(virtualenv)s/tmp" % env)
  run("cd %(base)s/%(virtualenv)s; source bin/activate; cd project/project; python manage.py syncdb --noinput; python manage.py migrate --noinput;" % env)
  if env.dev_mode:
    sudo("chmod 777 /server/env.example.com/tmp/django.sqlite") # Enable group write


def pull():
  "Does a git pull on all the repositories"
  require('hosts', provided_by=[staging, production])
  run("cd %(base)s/%(virtualenv)s/project; git pull %(parent)s %(branch)s" % env)


####

#### Reloading Python files

def reload():
  "Forces uwsgi/nginx to reload the project"
  require('hosts', provided_by=[vagrant, staging, production])
  sudo("killall -HUP uwsgi")
  sudo("killall -HUP nginx")


#####

##### Version roll back

def rollback(hash):
  """
  Rollback git repositories to specified hash.
  Usage:
  fab rollback:hash=etcetc123
  """
  require('hosts', provided_by=[staging, production])
  env.hash = hash
  run("cd %(base)s/%(virtualenv)s/project; git reset --hard %(hash)s" % env)

####

