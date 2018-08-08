from fabric.api import local, run, put, lcd, cd, env
'''
    fab deploy_no_build:commit
'''
env.hosts = ['39.107.82.164']
env.user = 'ubuntu'
env.password = 'Zhh12345678'
code_dir='/data/www/CloudStorage/'
def pull():
    local('git pull')
def deploy_no_build():
    cd(code_dir)
    pull()
    run('service mysql restart')
    run('uwsgi --reload uwsgi.pid')

deploy_no_build()