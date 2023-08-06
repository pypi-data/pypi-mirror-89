# qtemplate
A command line tool for managing and generating files or scripts from templates

## Overview

`qtemplate` is a linux command line tool that helps generate files from templates, settings/datafiles, and command line prompts. A common task is creating new scripts or files that follow a convention you want to adhere to. You want access to create these base scripts but don't want to have to copy files and manually replace tags.

qtempalte is meant to have the feel of shell aliases, where defining a new template is easy and instantiating a new template is easy. By creating a simple directory structure for storing templates, default data, and plugins, we can ensure templates are available at a your fingertips, without pausing.

## Structure

qtemplate supports system level configurations under `/etc/qtemplate` that are overwritten by user level configurations under `~/.qtemplate/`

```
.qtemplate/
├── conf.yaml
└── templates
    └── example_template
        ├── example.jinja
        ├── example.json
        └── example.yaml
```

Under the conf.yaml, you can configure your template stores. Default template stores are localhost directories. 

#### template_stores

The template stores config is the ordering in which templates are looked up. This is a cascading list in the conf.yaml:

```yaml
template_stores:
    - https://www.qsonlabs.com/qtemplate/registry/templates/
    - file://user@remote-host/etc/qtemplate/templates
    - file://localhost/~/.qtemplate/templates/
    - file://localhost/etc/qtemplate/templates
```

Each store should be a valid URI and `qtemplate` will handle pulling the data using the appropriate connector. If a given template is not found, it will check the next template store in the list. This enables remote template repositories

### Templates

A template should have at most 3 files:

- *.jinja - Mandatory file for a template. There should only be one .jinja file and that will be the template used
- template.conf - a file used to specify any template level configurations. All of these configs can be overwritten with command line params
- *.data  - any default data that should be supplied to the jinja template. Default data can be provided directly in the jinja file but a separate .data file is more explicit. the *.data file can be json or yaml

