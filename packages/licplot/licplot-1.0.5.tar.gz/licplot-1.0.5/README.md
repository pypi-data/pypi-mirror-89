# Line Integral Convolution

![Demo](https://raw.githubusercontent.com/alexus37/licplot/master/demo.png)

The Line Integral Convolution (LIC) is an algorithm used to image a vector
field. Its main advantage is to show in intricate detail the fine
structure of the vector field. It does not display the direction or
magnitude of the vectors, although this information can be color coded
in a postprocessing step.

The result of course depends on the shape of the kernel and the length  
of the streamline. If it is too small, the texture is not sufficiently
filtered and the motion is not clear. If it is too large, the image is
smoothed and details of the motion are lost. For an image of size
(256, 256), a value of 20 provides acceptable results.

## Install

If you want to install LIC you can clone the repo and run.

```bash
    pip install -e .
```

or install from pypi

```bash
    pip install licplot
```

## Usage

The basic usage is shown in and a runnable example can be found under `examples/lic_demo.py`

```python
    from lic import lic_internal
    import numpy as np
    import matplotlib.pyplot as plt
    # create vector field and kernel
    size = 500
    u = np.zeros((size, size), dtype=np.float32)
    v = np.zeros((size, size), dtype=np.float32)
    texture = np.random.rand(size, size).astype(np.float32)

    # create a kernel
    kernel_length = 31
    kernel = np.sin(np.arange(kernel_length) * np.pi / kernel_length).astype(np.float32)

    # compute the lic
    image = lic_internal.line_integral_convolution(u, v, texture, kernel)

    plt.imshow(image, cmap="hot")
    plt.show()
```

### Forked from https://github.com/aarchiba/scikits-vectorplot

by Anne Archibald
