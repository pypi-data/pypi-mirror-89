# jlab-enhanced-launcher

![Github Actions Status](https://github.com/fcollonval/jlab-enhanced-launcher/workflows/Build/badge.svg) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/fcollonval/jlab-enhanced-launcher/master?urlpath=lab) [![npm](https://img.shields.io/npm/v/@jlab-enhanced/launcher)](https://www.npmjs.com/package/@jlab-enhanced/launcher) [![PyPI](https://img.shields.io/pypi/v/jlab-enhanced-launcher)](https://pypi.org/project/jlab-enhanced-launcher)

A enhanced launcher for JupyterLab.

![Demo](https://raw.githubusercontent.com/fcollonval/jlab-enhanced-launcher/master/enh_launcher.gif)

This codes started from https://github.com/jupyterlab/jupyterlab/pull/5953.

## Requirements

- JupyterLab >= 3.0

## Install

```bash
pip install jlab-enhanced-launcher
jupyter labextension disable @jupyterlab/launcher-extension
```

or

```bash
conda install jlab-enhanced-launcher
jupyter labextension disable @jupyterlab/launcher-extension
```

### Uninstall

```bash
pip uninstall jlab-enhanced-launcher
jupyter labextension enable @jupyterlab/launcher-extension
```

or

```bash
conda remove jlab-enhanced-launcher
jupyter labextension enable @jupyterlab/launcher-extension
```

## Contributing

### Development install

Note: You will need NodeJS to build the extension package.

The `jlpm` command is JupyterLab's pinned version of
[yarn](https://yarnpkg.com/) that is installed with JupyterLab. You may use
`yarn` or `npm` in lieu of `jlpm` below.

```bash
# Clone the repo to your local environment
# Change directory to the jlab_enhanced_launcher directory
# Install package in development mode
pip install -e .
jupyter labextension disable @jupyterlab/launcher-extension
# Link your development version of the extension with JupyterLab
jupyter labextension develop . --overwrite
# Rebuild extension Typescript source after making changes
jlpm run build
```

You can watch the source directory and run JupyterLab at the same time in different terminals to watch for changes in the extension's source and automatically rebuild the extension.

```bash
# Watch the source directory in one terminal, automatically rebuilding when needed
jlpm run watch
# Run JupyterLab in another terminal
jupyter lab
```

With the watch command running, every saved change will immediately be built locally and available in your running JupyterLab. Refresh JupyterLab to load the change in your browser (you may need to wait several seconds for the extension to be rebuilt).

By default, the `jlpm run build` command generates the source maps for this extension to make it easier to debug using the browser dev tools. To also generate source maps for the JupyterLab core extensions, you can run the following command:

```bash
jupyter lab build --minimize=False
```
