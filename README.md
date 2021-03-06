-**Table of Contents**  *generated with [DocToc](http://doctoc.herokuapp.com/)*
 -
 - [Gists.cli](#gistscli)
 - [For the Casual User](#for-the-casual-user)
   - [Installation](#installation)
   - [Authentication](#authentication)
   - [Usage](#usage)
 - [For The Advanced User](#for-the-advanced-user)
   - [Tips](#tips)
   - [Usage](#usage-1)
 - [For the Developer](#for-the-developer)
   - [Installation](#installation-1)
   - [Non-Mac/OS X System Testing](#non-macos-x-system-testing)
 - [In Development](#in-development)
 - [Issues and Roadmap](#issues-and-roadmap)

# Gists.cli


> I'm a Developer who uses VI and the like. iPad and iPhone apps are great, but when I really need a Gist i'm at the command line. 

An easy to use CLI to manage *your* GitHub Gists. Create, edit, append, view, search and backup your Gists. 

- Github - https://github.com/khilnani/gists.cli 
- Python Package - https://pypi.python.org/pypi/gists.cli

# For the Casual User

## Installation

- Install the Python package manager PIP (http://www.pip-installer.org/)
  - Run `yum install python-setuptools` If you are on a fresh Linux server/VM
  - Run `sudo easy_install pip`
- Once PIP is installed, 
  - Run `sudo pip install gists.cli`
  - Run `sudo pip install gists.cli --upgrade` if upgrading.

## Authentication


- By default the application will attempt to use Basic Auth to authenticate i.e. will prompt for username/password each time it is run.
- If the file `~/.git-credentials` is available, it will use the first OAuth token entry. 
- If the file  `~/.gists` with a Github OAuth token is found, it will be given preference over the above two mechanisms.
- Run `./gists token|t` to avoid the username/password prompt and to use an OAuth Token other than `~/.git-credentials`. Saves to `~/.gists`.

## Usage

> *All the commands below are interactive and will prompt for user input (eg. public/private, descriptions) and confirmations (eg. directory creation).*

*Each Action/Command has multiple alias e.g. Create can be invoked not only by `gists new|create`, but also  `gists c|n|new|create|--new|--create|-n|-c` Run `gists help|--help|-h|h` for more info.*

**List all your Gists**

- `gists`

**View a Gist**

- `gists ID` - View Gist with ID on the console.
- `gists ID PATH` - Download Gist files with ID to PATH. Will prompt for confirmation.


**Create a Gist**

We'll prompt for stuff like Gist type (public/private), Description and Gist Content as needed.

- `gists new` or `./gists create`.
- `gists FILE` - Create a Gist using the contents of FILE
- `gists "Content"` - Create a Gist using the string "Content"

To avoid the Public/private Gist type prompt -

> Bool should be `true` for Public, `false` for Private

- `gists Bool FILE`
- `gists Bool "Content"`



# For The Advanced User

## Tips

- Each Action/Command has multiple alias e.g. Create can be invoked not only by `gists new|create`, but also  `gists c|n|new|create|--new|--create|-n|-c` Run `gists help|--help|-h|h` for more info
- Add `debug|--debug` to the end of any execution to view low level details. eg. `./gists debug`. *NOTE - This will reveal your OAuth ID but not your Basic Auth password.*
- Add `supress|silent|--supress|--silient` at the end of any execution to supress any prompts of confirmations if you like to live dangerously. 
- eg. `./gists -n FILE --supress --debug`. 

## Usage

*All the commands below are interactive and will prompt for user input.*

**List all your Gists**

- `gists` - list your Gists.

**View a Gist**

- `gists ID` - view Gist with ID on the console.
- `gists ID PATH` - download Gist files with ID to PATH. Will prompt for confirmation.

**Setup OAuth token**

- `gists token|t` - setup to use OAuth Token other than `~/.git-credentials`. Saves to `~/.gists`.

**Create a Gist**

> - FILE - is a file path, relative or absolute.
> - Bool - True for Public, False for Private. Supports True, False, 1, 0, Yes, No, y, n. Case-insensitive
> - Description and Content - Text content within quotes


Without specifying a command (eg. create, new), the application will trying to figure it out. However, this supports fewer combinations of arguments.

- `gists FILE`
- `gists "Content"`
- `gists Bool FILE`
- `gists Bool "Content"`
- `gists "Description" FILE`
- `gists "Description" "Content"`
- `gists Bool "Description" FILE`
- `gists Bool "Description" "Content"`


If you like to type, or be specific (will prompt for stuff like Gist type, Description and Gist Content etc as needed).

- `gists new|n|create|c`
- `gists new|n|create|c FILE`
- `gists new|n|create|c "Content"`
- `gists new|n|create|c Bool FILE`
- `gists new|n|create|c Bool "Content"`
- `gists new|n|create|c "Description" FILE`
- `gists new|n|create|c "Description" "Content"`
- `gists new|n|create|c Bool "Description" FILE`
- `gists new|n|create|c Bool "Description" "Content"`

# In Development

**Update**

- `gists update|u ID [PARAMS]` - Update a Gist. Content sent via Console, Clipboard or File.
- `gists append|a ID [PARAMS]` - Append to a Gist. Content sent via Console, Clipboard or File.

**Delete**

- `gists delete|del|d ID` - Delete a Gist.

**Export/Backup**

- `gists backup|b [DIR]` - Backup all Gists in the user's account.

**Search**

- `gists search|query|q QUERY` - Search Gists.

**Misc**

- `gists star` - List starred Gists


# For the Developer

## Installation

If you would like to contribute changes to the code base

- Get the code
  - Fork and `git clone` the fork, or ...
  - `git clone https://github.com/khilnani/gists.cli.git`, or ...
  - Download the latest Tag Archive from https://github.com/khilnani/gists.cli  
    - *Downloading the Archive is not recommended, since it won't be easy to merge code back*.
- Install dependencies by running `./dependencies.sh`. 
  - This installs PIP (if not already installed) and then installs the dependencies.
- Run the installer as below. If you get any error run with `sudo ...`
  - `./install.py` with no arguments will install to `/usr/local/bin`.
  - `./install.py INSTALL_PATH` will install to a specific directory.

## Non-Mac/OS X System Testing

- I use http://VagrantUp.com, http://ansibleworks.com and http://www.virtualBox.org to test on CentOS and Ubuntu.
- Prerequisites
  - Vagrant
    - Install Vagrant - http://vagrantup.com/downloads
  - Ansible
    - Install Ansible on Mac OS X or CentOS/RHEL - https://github.com/khilnani/devops/tree/master/ansible
  - Virtual Box
    - Install VirtualBox - https://www.virtualbox.org/wiki/Downloads to download/install
- Run
  -  Change directory to `./_vagrant`
  -  Run `vagrant up` to install both CentOS6.5 and Ubuntu, or`vagrant up centos` or `vagrant up ubuntu` - start the VMs
    - If my Boxes are not already installed, they will be downloaded and installed
  -  Run `vagrant ssh centos` or `vagrant ssh ubuntu` - to ssh over
  -  Once you SSH over, the current directory is available at `/git_data` on the VM
- Debug
  -  Change directory to `./_vagrant`
  -  Run `./debug.ssh up centos` or `./debug.ssh up ubuntu` - This runs Vagrant with Debug Level INFO

# Issues and Roadmap

- Take a look at https://github.com/khilnani/gists.cli/issues to view Issues and Milestones.


