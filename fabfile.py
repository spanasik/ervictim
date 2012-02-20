from __future__ import with_statement
from fabric.api import *

env.user = 'ervictim'
env.hosts = ['ervictim.ru',]
project_path = '/home/ervictim/website'
domain = 'ervictim.ru'
program = "ervictim"

def deploy():
    with settings(warn_only=True):
	if run("test -d %s" % project_path).failed:
            run("mkdir %s" % project_path)
            with cd(project_path):
                run("git clone git://github.com/spanasik/ervictim.git %s" % project_path)
                run("python %s/bootstrap.py" % project_path)
                run("%s/bin/buildout" % project_path)
                sudo("/usr/bin/mysql -uroot -e'create database ervictim default character set utf8;'")
                run("%s/bin/python %s/src/website/manage.py syncdb" % (project_path,project_path))
                run("%s/bin/python %s/src/website/manage.py loaddata %s/src/website/flatpages.json" % (project_path,project_path,project_path))
                sudo("/bin/ln -s %s/sys/etc/nginx/production/%s /etc/nginx/sites-enabled/%s" % (project_path,domain,domain))            
                sudo("/bin/ln -s %s/sys/etc/supervisor/conf.d/%s.conf /etc/supervisor/conf.d/%s.conf" % (project_path,program,program))
                sudo("/bin/ln -s %s/sys/etc/cron.hourly/backup_ervictim /etc/cron.hourly/backup_ervictim" % (project_path,))
                sudo("/etc/init.d/nginx restart")
                sudo("/usr/bin/supervisorctl reload")

    with cd(project_path):
        run("git pull")
	sudo("/usr/bin/supervisorctl restart ervictim")
