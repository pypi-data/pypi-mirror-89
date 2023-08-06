# Textvn CLI

Quick save text


### Installing

To install the tool from pip

```sh
pip install textcli

```

# Usage


To save contents of a file (with path file_path) to https://textvn.com/urlpath

```bash

texcl -o file_path urlpath

```

To watch the file for changes add `--watch` or `-w` flag

Example

```bash

texcl -low file_path urlpath

```


To get the contents of a `urlpath` to a local file run the following command

```
texcl -g file_path urlpath 

```

Note: Using other flags with g flag is redundant

![Usage](./demo.gif)
