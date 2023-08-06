
# Spice21 Python 

Python interface to the Spice21 simulator. 

## Installation 

Spice21 is implemented in Rust. 
Spice21py interfaces to Spice21 via two primary tools: 

* Protobuf. Spice21's primary types are generated, both in Python and in Rust, 
from their Protobuf-schema definitions.   
* The [PyO3](https://github.com/PyO3) binding-generation ecosystem, 
including its build and publishing tool [Maturin](https://github.com/PyO3/maturin).

Common development commands:

* `maturin build`
* `maturin develop` 

Note `maturin` is largely a Python-thing; it will be installed via pip or conda, 
and generally associated with a particular Python environment. 
In Maturin terms, `spice21py` is a [mixed Python/Rust project](https://github.com/PyO3/maturin#mixed-rustpython-projects). 
This also dictates much of the `spice21py` file and folder organization. 

* `src` holds the small Rust-module for exposing `spice21` methods to Python, and converting its inputs and outputs 
* `spice21py` is the name of the Python primary Python package
* After builds complete, `spice21py/spice21py.{some_compiled_binary_suffix}` is an internal Python module *also* named `spice21py`, as dictated by Maturin

---

Developing without Maturin is possible in principal, but more difficult, especially on MacOS. 
From the [PyO3 guide](https://pyo3.rs/v0.5.3/print.html): 

```
On Mac Os, you need to set additional linker arguments. One option is to compile with cargo rustc --release -- -C link-arg=-undefined -C link-arg=dynamic_lookup, the other is to create a .cargo/config with the following content:


[target.x86_64-apple-darwin]
rustflags = [
  "-C", "link-arg=-undefined",
  "-C", "link-arg=dynamic_lookup",
]
Also on macOS, you will need to rename the output from *.dylib to *.so. 
```

While this has been used for spice21py briefly and temporarily, 
and should work in principle, it is not used actively. 
