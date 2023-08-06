# Makru
[![pipeline status](https://gitlab.com/jinwa/makru/badges/master/pipeline.svg)](https://gitlab.com/jinwa/makru/-/commits/master)
[![coverage report](https://gitlab.com/jinwa/makru/badges/master/coverage.svg)](https://gitlab.com/jinwa/makru/-/commits/master)  
Makru(/ˈmeɪkru/) is a simple, readable way to compile your program.

> Note: This program and planned plugin for c language support are still in work in progress. It may break something without cautions. 

## Installation
Installing sources is only way to install makru for now.
````
git clone https://gitlab.com/jinwa/makru.git
cd makru
pip install .
````

## Basic Usage
Makru does not include any feature to compile something: all the logic of compiling files, linking or running code are held by plugins. Makru is a easy shortcut to collect and call them.

To use makru, you need to place a file (usually called `makru.yaml`) in your project folder:
````
- MyProject
  | - src
  | - makru.yaml
````
The file looks like:
````
name: MyProject # the project name
use: someone-plugin # which plugin you want to use
type: executable # described by plugin, which type the project is
dependencies: # optional, makru itself does not care about this field
  - match # <name>
  - random 2.* # <name> <version regex>
  - "@(./hiddenfolder)" # @(path) , path is relative to the path of this file
````
> Note: Our makru plugin for c language support is still in developing

Your config file for makru must contain `name`, `use` and `type`. After that, run command `makru`:
````
> makru
panic: could not found plugin someone-plugin requested in ..., all plugins: [...], searched paths: [...]
````
That's done! The message means makru run correctly. For more details, please look at `example/simple` in this project.


### How to place plugins
For now, you can put your plugins to `<folder with config file>/makru/plugins` or define `plugin_paths` in your config, like this: 
````
...
plugin_paths:
  - ./buildtools/makru_plugins
...
````

## License
The MIT License. See `LICENSE` for details.
This project is owned by all contributors, see `CONTRIBUTORS` for full list.

## Contributing Guide
//TODO

