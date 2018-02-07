import pip

pip_module = 'git+https://github.com/systemd/python-systemd.git#egg=systemd'


def pip_module_install(module):
    pip.main(['install', module])


pip_module_install(pip_module)
