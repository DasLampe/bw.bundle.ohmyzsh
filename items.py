directories = {}
git_deploy = {}
actions = {}

for user in {key: value for (key, value) in node.metadata.get('users', {}).items()
             if value.get('shell', "")[-3:] == 'zsh'}:
    dirname = '/home/{}/.oh-my-zsh'.format(user)

    directories[dirname] = {
        'owner': user,
    }

    git_deploy[dirname] = {
        'repo': 'https://github.com/ohmyzsh/ohmyzsh',
        'rev': 'master',
        'needs': [
            'user:{}'.format(user),
        ],
    }

    actions['chown_ohmyzsh_dir_for_{}'.format(user)] = {
        'command': 'chown -R {user} {dirname}'.format(user=user, dirname=dirname),
        'needs': [
            'git_deploy:{}'.format(dirname)
        ],
        'interactive': False,
    }

    actions['chmod_ohmyzsh_for_{}'.format(user)] = {
        'command': 'chmod -R g-w,o-w {}'.format(dirname),
        'needs': [
            'git_deploy:{}'.format(dirname)
        ],
        'interactive': False,
    }
