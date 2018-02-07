#!/bin/python
import subprocess
import fileinput


packages = ['postgresql-9.2', 'postgresql-contrib', 'postgresql-server', 'git']
packages1 = ['epel-release', 'git']
packages2 = ['gcc', 'python-devel', 'systemd-devel', 'python-pip']
fileToSearch = '/var/lib/pgsql/data/pg_hba.conf'
textToSearch = ' ident'
textToReplace = ' md5'
pip_module = 'git+https://github.com/systemd/python-systemd.git#egg=systemd'
service = 'postgresql'


def rpm_qa_package(package):
    args1 = ["rpm", "-qa"]
    args2 = ["grep", "-w", package]
    rpm = subprocess.Popen(args1, stdout=subprocess.PIPE)
    grep = subprocess.Popen(args2, stdin=rpm.stdout, stdout=subprocess.PIPE)
    rpm.stdout.close()
    output = grep.communicate()[0].rstrip()
    rpm.wait()
    output_length = len(output)
    if (output_length != 0):
        return output


def rpm_qa_packages(array):
    qa_list = []
    install_list = []
    return_list = [qa_list, install_list]
    for item in array:
        package = rpm_qa_package(item)
        package_type = type(package)
        if (package_type is str):
            qa_list.append(package)
        else:
            install_list.append(item)
    return return_list


def yum_package_install(package):
    args1 = ["yum", "install", "-y", package]
    yum = subprocess.Popen(args1, stdout=subprocess.PIPE)
    output = yum.communicate()[0]
    return output


def install_packages(packages):
    package_list = rpm_qa_packages(packages)
    un = len(package_list[1])
    if (un != 0):
        for package in package_list[1]:
            yum_package_install(package)
    return package_list[1]


def init_database():
    args1 = ["postgresql-setup", "initdb"]
    postgresql_setup = subprocess.Popen(args1, stdout=subprocess.PIPE)
    output = postgresql_setup.communicate()[0]
    return output


def search_and_replace_file(fileToSearch, textToSearch, textToReplace):
    f = fileinput.input(fileToSearch, inplace=True, backup='.bak')
    for line in f:
        print(line.replace(textToSearch, textToReplace))
    f.close()


def systemctyl_start(service):
    args1 = ["systemctl", "start", service]
    systemctl = subprocess.Popen(args1, stdout=subprocess.PIPE)
    output = systemctl.communicate()[0]
    return output


def systemctyl_enable(service):
    args1 = ["systemctl", "enable", service]
    systemctl = subprocess.Popen(args1, stdout=subprocess.PIPE)
    output = systemctl.communicate()[0]
    return output


def main(packages, packages1, packages2, fileToSearch, textToSearch,
         textToReplace, service):
    install_packages(packages)
    init_database()
    search_and_replace_file(fileToSearch, textToSearch, textToReplace)
    install_packages(packages1)
    install_packages(packages2)
    systemctyl_start(service)
    systemctyl_enable(service)


main(packages, packages1, packages2, fileToSearch, textToSearch, textToReplace,
     service)
