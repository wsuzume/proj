import os
import sys
import json
import argparse

script_content = """\
#!/bin/sh

gpython=${PYENV_ROOT}/versions/$(pyenv global)/bin/python
gproj=${PYENV_ROOT}/versions/$(pyenv global)/bin/proj

if test $# -eq 1 && [[ $1 =~ ^[^\-] ]] ; then
    result=(exec $gpython $gproj --echo $1)
    exit_code=$?
    if test $exit_code -eq 0 ; then
        cd $result ; pwd
    elif test $exit_code -eq 1 ; then
        echo $result
    fi
else
    (exec $gpython $gproj "$@")
fi
"""

projrc_content ="""\
alias proj='source ~/.config/proj/proj'
"""

conf_dir = os.path.expanduser('~/.config/proj')
proj_script = os.path.join(conf_dir, 'proj')
projrc = os.path.join(conf_dir, 'projrc')
project_settings = os.path.join(conf_dir, 'projects.json')

local_conf_dir = os.path.expanduser('./.proj')

def check_config():
    if not os.path.exists(conf_dir):
        print('proj config directory does not exists.')
        print(f'Creating at \'{conf_dir}\'')
        os.makedirs(conf_dir)

    if not os.path.exists(proj_script):
        with open(proj_script, 'w') as f:
            f.write(script_content)

    if not os.path.exists(projrc):
        with open(projrc, 'w') as f:
            f.write(projrc_content)

def load_config():
    if not os.path.exists(project_settings):
        return {}
    with open(project_settings, 'r') as f:
        projects = json.load(f)
    return projects

def main():
    check_config()
    projects = load_config()

    parser = argparse.ArgumentParser()
    # echo project path
    parser.add_argument('--echo', nargs='?', default=None, const='', metavar='project_name')
    # register current directory as [project_name]
    parser.add_argument('--init', nargs='?', default=None, const='', metavar='project_name')
    # remove registered project from list
    parser.add_argument('--remove', nargs='?', default=None, const='', metavar='project_name')
    # register startup script for the current project
    ## startup script is executed when you enter the project by proj command
    parser.add_argument('--startwith', nargs='?', default=None, const='', metavar='file_name')
    parser.add_argument('--echo-startwith', nargs='?', default=None, const='', metavar='file_name')
    # register leaving script for the current project
    ## leaving script is executed when you leave the project by proj command
    parser.add_argument('--endwith', nargs='?', default=None, const='', metavar='file_name')
    parser.add_argument('--echo-endwith', nargs='?', default=None, const='', metavar='file_name')
    # set alias
    ## if local alias;
    ##     this alias is automatically activated when you enter the project by proj command,
    ##     and automatically unaliased when you leave the project by proj command.
    ##     the configuration is saved in '.proj/aliases'
    ## if global alias;
    ##     this alias is always activated automatically.
    ##     the configuration is saved in '~/.config/proj/aliases'
    parser.add_argument('--alias')
    # remove alias
    parser.add_argument('--unalias')
    # activate local project settings
    ## 1. activate local aliases
    ## 2. run the script file which registered as --startwith
    parser.add_argument('--activate', action='store_true')
    # deactivate local project settings
    ## 1. run the script file which registered as --endwith
    ## 2. deactivate local aliases
    parser.add_argument('--deactivate', action='store_true')
    # backup local setting to the directory which registered as --set-origin
    parser.add_argument('--backup')
    # restore local setting from the directory which registered as --set-origin
    parser.add_argument('--restore')
    # set backup directory
    parser.add_argument('--set-origin')
    # set remote backup
    parser.add_argument('--remote-backup')
    # show config and status of the project
    parser.add_argument('--show')
    #parser.add_argument('--global') #globalで設定

    args = parser.parse_args()

    if args.echo is not None:
        if args.echo in projects:
            print(projects[args.echo])
            sys.exit(0)
        else:
            print(f'Error: project \'{args.echo}\' is not registered.')
            sys.exit(1)

    local_conf = {
        'start': '',
        'end': '',
    }

    if args.activate:
        if os.path.exists(os.path.join(local_conf_dir, 'config.json')):
            with open(os.path.join(local_conf_dir, 'config.json'), 'r') as f:
                local_conf = json.load(f)

        if 'start' in local_conf and local_conf['start'] != '':
            abspath = os.path.abspath(local_conf_dir)
            print(os.path.join(abspath, 'scripts', local_conf['start']))

        sys.exit(0)

    if args.deactivate:
        if os.path.exists(os.path.join(local_conf_dir, 'config.json')):
            with open(os.path.join(local_conf_dir, 'config.json'), 'r') as f:
                local_conf = json.load(f)

        if 'end' in local_conf and local_conf['end'] != '':
            abspath = os.path.abspath(local_conf_dir)
            print(os.path.join(abspath, 'scripts', local_conf['start']))

        sys.exit(0)

    if args.init is not None:
        if os.path.exists(os.path.join(local_conf_dir, 'config.json')):
            print('already registered')
            sys.exit(0)
        if args.init == '':
            print(f'Error: project name required.')
            sys.exit(1)
        elif args.init in projects:
            print(f'Error: project \'{args.init}\' is already registered.')
            print(f'project directory -> {projects[args.init]}')
            sys.exit(1)
        else:
            print('OK:', os.getcwd())
            projects[args.init] = os.getcwd()
            with open(project_settings, 'w') as f:
                json.dump(projects, f, indent=2)
            with open(os.path.join(local_conf_dir, 'config.json'), 'w') as f:
                json.dump(local_conf, f, indent=2)
            sys.exit(0)

    if args.remove is not None:
        if args.remove in projects:
            path = projects[args.remove]
            projects.pop(args.remove)
            with open(project_settings, 'w') as f:
                json.dump(projects, f, indent=2)
            print('removed:', args.remove, path)
            sys.exit(0)
        else:
            print(f'Error: project \'{args.echo}\' is not registered.')
            sys.exit(1)

    #if args.set_startup is not None:
    #    if args.set_startup

    for k, v in projects.items():
        print(k, ':', v)
    sys.exit(0)


    #print(projects)
    alias = []
    for k, v in projects.items():
        #print(k, v)
        alias.append(f'alias {k}="cd \'{v}\' ; pwd"')

    with open(os.path.join(conf_dir, 'config'), 'w') as f:
        for line in alias:
            f.write(line + '\n')

if __name__ == '__main__':
    main()
