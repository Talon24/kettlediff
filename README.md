[![Build Status](https://travis-ci.com/Talon24/kettlediff.svg?branch=master)](https://travis-ci.com/Talon24/kettlediff)
[![Updates](https://pyup.io/repos/github/Talon24/kettlediff/shield.svg)](https://pyup.io/repos/github/Talon24/kettlediff/)
[![Python 3](https://pyup.io/repos/github/Talon24/kettlediff/python-3-shield.svg)](https://pyup.io/repos/github/Talon24/kettlediff/)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)]()

# Kettlediff
Diff library for git (or other version control systems or standalone) to view changes in Pentaho Data Integration and Pentaho Report Designer files.

## Description
Kettlediff is a python tool that takes a .ktr- or a .kjb-file as input and outputs them in a way that they are easy to _diff_. Files from Pentaho Report designer are supported as well.

The original file will not be altered.

It will change the order of elements in the XML to be more static and counteract Kettle reorganizing them on save.
Also, it will remove some values that some Kettle versions handle differently as implicit or explicit default values and might trigger *git diff* to see a change although there is no functional difference.
For Report files, it will unzip them and list all their lines with the path of origin.

## Usage
When diffing .ktr-, .kjb- and .prpt-files, git will apply *kettlediff* to both files you want to compare and looks for differences in the output.
There differences in the files that originate from version differences and re-ordering of XML elements should be ignored and you should only see differences that functionally change the file.
When in steps, the hunk header will show the name of the step written in the **name** tag to locate the changes easily.

The line numbers found by git diff won't match the lines in the files as the XML will be changed to keep steps, etc. in a diffable order.

### Requirements
*Kettlediff* will run on python versions 3, but there is a python2-compatible release `py2_1.0.0`.

There are no external modules needed for it to run. However, if you have **lxml** installed on your machine, it will use that instead of the built-in **xml** module.

## Setup

Add the following lines to your gitconfig file.<br>
Linux: default path is `~/.gitconfig`<br>
Windows: default path is `%HOMEPATH%/.gitconfig`
```
[diff "kettle"]
        textconv = /path/to/this/kettlediff.py
        xfuncname = <name>(.*)</name>|<order>|<hops>
[diff "prpt"]
        textconv = /path/to/this/kettlediff.py
        xfuncname = .*name=.*
```
If you want to use *kettlediff* on all your repositories, you might want to add the reference to
your profile settings. If you haven't already, add a path to your gitconfig, for example in your home directory:
```
[core]
        attributesfile = ~/.gitattributes
```

If the file does not exist create it and add the following lines.
```
*.ktr diff=kettle
*.kjb diff=kettle
*.prpt diff=prpt
```
If you want to use *kettlediff* on a single repository, add them instead to "<your repo>/.git/info/attributes".

Now every time you call git diff on one of the above file types *kettlediff* will be automatically used.

## Usage with other other tools
### TortoiseGit
1. Open your TortoiseGit settings
2. Navigate to "Diff Viewer"
3. Click the "Advanced..."-Button
4. Add entry for each file extension:
  - .prpt
  - .ktr
  - .kjb
5. Fill in `cmd /K git diff --textconv %base %mine` as "External Program"

This will open a command prompt with the git diff view.

### TortoiseSVN
The tool will also work for TortoiseSVN. If you have git installed and properly set up, you can simply follow the instructions for TortoiseGit above. If no git is available, *kettlediff* provides a small git diff-like tool for that.
1. Open your TortoiseSVN settings
2. Navigate to "Diff Viewer"
3. Click the "Advanced..."-Button
4. Add entry for each file extension:
  - .prpt
  - .ktr
  - .kjb
5. Fill in `cmd /K python path/to/file.py %base %mine` as "External Program"

This will give you a command prompt that shows you a git diff-like output powered by pythons difflib function "unified_diff".

### Github Desktop
Should work out-of-the-box if gitconfig and gitattributes were set up as it uses the diff function provided by git.
