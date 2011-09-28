import subprocess

from fabric.api import cd
from fabric.api import env
from fabric.api import local
from fabric.api import require
from fabric.api import run
# from fabric.decorators import runs_once

GIT_SSH = 'ssh://webfaction:webapps/znaflab_git/repos/www.ryanbalfanz.com.git'

def prod():
	env.user = 'znaflab'
	env.hosts = ['znaflab.webfactional.com']
	env.remote_app_dir = '/home/znaflab/webapps/ryanbalfanz_static/'
	
def stage():
	"""docstring for stage"""
	env.user = 'znaflab'
	env.hosts = ['znaflab.webfactional.com']
	env.remote_app_dir = '/home/znaflab/webapps/ryanbalfanz_stage_static/'

def prepare_css(environment=None, style=None):
	"""Prepare the CSS using compass."""
	if not environment: environment = "production" # Environment 'production' may be special, see compass config
	if not style: style = "compressed" # One of: nested, expanded, compact, compressed
	opts = [
		"--environment {env}",
		# "--output-style {style}",
	]
	optStr = " ".join(opts).format(env=environment, style=style)
	compassCmd = "compass compile {options} --force".format(options=optStr)
	local(compassCmd)

def get_git_tag():
	"""docstring for get_git_tag"""
	return subprocess.Popen(["git", "describe", "--always"], stdout=subprocess.PIPE).communicate()[0]

def write_version_files():
	"""docstring for write_version_file"""
	currentTag = get_git_tag().strip()
	
	with open("./VERSION", "w") as f:
		f.write("{version}\n".format(version=currentTag))
		
	with open("./version.js", "w") as f:
		f.write("var version='{version}';\n".format(version=currentTag))

def deploy(branch="master"):
	"""Deploy the site."""
	require('hosts', provided_by = [prod,])
	with open("./VERSION", "rb") as f:
		s = f.read()
		print s, get_git_tag()
		# assert f.read() == get_git_tag()
	# assert False
	local("git push origin {branch}".format(branch=branch))
	with cd(env.remote_app_dir):
		# run("git pull origin".format(branch=branch))
		# run("git checkout {branch}".format(branch=branch))
		
		run("rm -i ./version.js")
		run("""echo 'var version="' > ./version.js""")
		run("echo `git describe --always --tag >> ./version.js`")
		run("""echo '";' > ./version.js""")
