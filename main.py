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
    parser.add_argument('--echo', nargs='?', default=None, const='', metavar='project_name')
    parser.add_argument('--init', nargs='?', default=None, const='')
    parser.add_argument('--remove', nargs='?', default=None, const='', metavar='project_name')
    parser.add_argument('--reset-profile', default=0)
    #parser.add_argument('--continue') #直前のプロジェクトへ移動
    #parser.add_argument('--begin') #現在のディレクトリでスタートスクリプトを実行
    #parser.add_argument('--unsub') #登録解除
    #parser.add_argument('--status') #プロジェクトのステータス
    #parser.add_argument('--todo') #TODO
    #parser.add_argument('--show-todo') #TODOの一覧
    #parser.add_argument('--schedule') #予定
    #parser.add_argument('--show-schedule') #予定の一覧
    #parser.add_argument('--set-origin') #GitHubと連携
    #parser.add_argument('--global') #globalで設定

    args = parser.parse_args()

    if args.echo is not None:
        if args.echo in projects:
            print(projects[args.echo])
            sys.exit(0)
        else:
            print(f'Error: project \'{args.echo}\' is not registered.')
            sys.exit(1)

    if args.init is not None:
        if args.init == '':
            print('init:', args.init)
            sys.exit(0)
        elif args.init in projects:
            print(f'Error: project \'{args.init}\' is already registered.')
            print(f'project directory -> {projects[args.init]}')
            sys.exit(1)
        else:
            print(f'OK:', os.getcwd())
            projects[args.init] = os.getcwd()
            with open(project_settings, 'w') as f:
                json.dump(projects, f, indent=2)
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
