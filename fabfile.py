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

def deploy(branch="master"):
	"""Deploy the site."""
	require('hosts', provided_by = [prod,])
	local("git push origin {branch}".format(branch=branch))
	with cd(env.remote_app_dir):
		run("git pull origin {branch}".format(dir=env.remote_app_dir, branch=branch))
