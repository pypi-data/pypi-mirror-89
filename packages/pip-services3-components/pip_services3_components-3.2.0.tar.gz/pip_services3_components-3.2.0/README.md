# <img src="https://github.com/pip-services/pip-services/raw/master/design/Logo.png" alt="Pip.Services Logo" style="max-width:30%"> <br/> Component definitions for Python

This framework is a part of [Pip.Services](https://github.com/pip-services/pip-services) project.
It provides basic building blocks that can be used to implement non-trivial business logic in applications and services.

The key difference of this framework is a portable implementation across variety of different languages. 
Currently it supports Java, .NET, Python, Node.js, Golang. The code provides reasonably thin abstraction layer 
over most fundamental functions and delivers symmetric implementation that can be quickly ported between different platforms.

All functionality is decomposed into several packages:

- **Auth** - authentication credential stores
- **Build** - component factories framework
- **Cache** - distributed cache
- **Config** - configuration framework
- **Connect** - connection discovery services
- **Count** - performance counters components
- **Info** - context info
- **Log** - logging components

Quick Links:

* [Downloads](https://github.com/pip-services3-python/pip-services3-components-python/blob/master/doc/Downloads.md)
* [API Reference](https://pip-services3-python.github.io/pip-services3-components-python/index.html)
* [Building and Testing](https://github.com/pip-services3-python/pip-services3-components-python/blob/master/doc/Development.md)
* [Contributing](https://github.com/pip-services3-python/pip-services3-components-python/blob/master/doc/Development.md/#contrib)

## Acknowledgements

The initial implementation is done by **Sergey Seroukhov**. Pip.Services team is looking for volunteers to 
take ownership over Python implementation in the project.
