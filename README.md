

# OpenAlea Release

## Documentation

Official documentation is available at [openalea.github.io](http://openalea.rtfd.io)

## Install
To install OpenAlea use conda

If you want to retrieve the code from git, use git clone.
Then use this command that will retrieve all the submodules::
    
    git submodule update --init --recursive

## Contribute

To fetch all the modules, use in pkgs.py
>>> submodules()

To update to the latest tags
>>> update_latest_tag()

To also add the latest tag for each package
>>> update_latest_tag(True)
