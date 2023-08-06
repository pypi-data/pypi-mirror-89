RAW Light Simulation reader/converter package
=============================================

![](https://img.shields.io/github/workflow/status/prise-3d/rawls/build?style=flat-square) ![](https://img.shields.io/pypi/v/rawls?style=flat-square) ![](https://img.shields.io/pypi/dm/rawls?style=flat-square)

<p align="center">
    <img src="https://github.com/prise-3d/rawls/blob/master/rawls_logo.png" alt="" width="50%">
</p>

Description
-----------

Global illumination methods based on stochastic techniques provide photo-realistic images. These methods are generally based on path tracing theory in which stochastic paths are generated from the camera point of view through each pixel toward the 3D scene. 

<p align="center">
    <img src="https://github.com/prise-3d/rawls/blob/master/docs/source/_static/path_tracing.png" alt="" width="60%">
</p>


`rawls` is a Python package developed during a thesis project. It enables to manage `.rawls` image file extension. The image extension `.rawls` is used to store all samples values of images obtained during rendering of synthesis images. This output extension is available in a custom version of [pbrt-v3](https://github.com/prise-3d/pbrt-v3) details.

Installation
------------

```bash
pip install rawls
```

How to use ?
------------

To use, simply do:
```python
from rawls.rawls import Rawls
path = 'images/example_1.rawls'
rawls_img = Rawls.load(path)
rawls_img.save('output.png')
```

Classes
-------

This project contains usefull classes.

- **Rawls** : *Manage `.rawls` file date*
- **RawlsStats** : *Enables to merge `.rawls` image files and extract statistics*

All these classes will be enhanced during development of the package. Documentation is available [here](https://prise-3d.github.io/rawls/).

How to contribute
-----------------

Please refer to the [guidelines](CONTRIBUTING.md) file if you want to contribute!

## Contributors

* [jbuisine](https://github.com/jbuisine)

## License

[MIT](LICENSE)
