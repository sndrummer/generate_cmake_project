#!/usr/bin/env python3

'''Create a C++ Cmake Project from a template'''
import argparse
import os
import subprocess
from git.repo import Repo
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('project_name', help='The project name')
parser.add_argument('--gcc-version',
                    dest='gcc_version',
                    help='specify the gcc version that should be used',)
args = parser.parse_args()

cwd = os.getcwd()
project_name = args.project_name.lower()
gcc_version = '-' + args.gcc_version if args.gcc_version else ''

# Replace '-' with underscores to make compatible with CMake
project_name = project_name.replace(' ', '-')
project_name = project_name.replace('_', '-')
repo_dir = os.path.join(cwd, project_name)
TEMPLATE_URL = 'https://github.com/sndrummer/cmake_cpp_basic_template.git'


def pull_template():
    print(f'Getting template from {TEMPLATE_URL}...')
    if os.path.isdir(repo_dir):
        exit(f'FAILURE: Directory {project_name} already exists, exiting...')
    Repo.clone_from(TEMPLATE_URL, repo_dir)
    if not os.path.isdir(repo_dir):
        exit('FAILURE: failed to clone cmake template')


def add_correct_project_name(filename, old, new):
    '''Replace all occurrences of template project name with new project name

    Args:
        filename (str): Name of the file to replace text
        old (str): text to replace
        new (str): replacement text
    '''
    with open(filename) as f:
        replaced = f.read().replace(old, new)
    with open(filename, 'w') as f:
        f.write(replaced)


def update_project_name():
    print('Configuring project for CMake...')
    print('-' * 94)
    cmake_lists_file = os.path.join(repo_dir, 'CMakeLists.txt')
    launch_json = os.path.join(repo_dir, '.vscode', 'launch.json')
    good_project_name = project_name.replace('-', '_')

    # Fill in correct project name
    add_correct_project_name(
        cmake_lists_file, '@PROJECT_NAME@', good_project_name)
    add_correct_project_name(launch_json, '@PROJECT_NAME@', good_project_name)

    # Remove the .git/ of the template
    git_dir = os.path.join(repo_dir, '.git')
    if os.path.isdir(git_dir):
        shutil.rmtree(git_dir)


def clean_template():
    '''Remove .git/ folder of the template'''
    git_dir = os.path.join(repo_dir, '.git')
    if os.path.isdir(git_dir):
        shutil.rmtree(git_dir)


def setup_project():
    '''Build the CMake Project to make sure it worked'''
    os.chdir(repo_dir)
    build_dir_path = os.path.join(repo_dir, 'build')
    if not os.path.isdir(build_dir_path):
        exit(f'FAILURE: no build directory at {build_dir_path}')
    os.chdir(build_dir_path)
    return_code = subprocess.run(
        [
            'cmake',
            f'-DCMAKE_C_COMPILER=gcc{gcc_version}',
            f'-DCMAKE_CXX_COMPILER=g++{gcc_version}',
            '..',
        ]
    ).returncode

    if return_code != 0:
        exit('FAILURE: CMake configuration failed, exiting...')
    os.chdir(repo_dir)
    # Now git init the repo
    Repo.init(repo_dir)


def main():
    pull_template()
    update_project_name()
    clean_template()
    setup_project()
    print('-' * 92)
    print(f'Success! Project created at {repo_dir}')


if __name__ == '__main__':
    main()
