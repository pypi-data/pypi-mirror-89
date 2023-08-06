# rtcg

Run-time code generation for python. If a method requires special parameter sequence or names, it might be better to create a small dynamic wrapper.

This library will not create function at run-time. It is not intended to create functions. This is considered as rather unsecure. It will merely generate a trampoline function using named arguments, nothing more.

## Licensing

This library is published under BSD-3-Clause license.

## Versioning

This library follows semantic versioning 2.0. Any breaking change will produce a new major release. Versions below 1.0 are considered to have a unstable interface.
