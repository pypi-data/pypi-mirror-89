# altf1be_helpers

Helpers to deal with basic requirements of an application built by www.alt-f1.be. See <https://bitbucket.org/altf1be/altf1be_helpers>

* management of a JSON File: Load, save, save with datetime. 

## usage

* install the package on **pypi.org** : 
    * install : `pip install altf1be_helpers`
    * upgrade : `pip install altf1be_helpers --upgrade`


* install the package on **test.pypi.org** : 
    * install : `pip install -i https://test.pypi.org/simple/altf1be_helpers`
    * upgrade : `pip install -i https://test.pypi.org/simple/altf1be_helpers --upgrade`

## dependencies

* See [requirements.txt](requirements.txt)

## Build the package 

* build the setup.py
    * `python3 setup.py sdist bdist_wheel`
    * `python3 -m pip install --user --upgrade twine`

* upload the library on TEST **pypi.org** 
    * `python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*` 
    * Source : [https://test.pypi.org/project/altf1be_helpers](https://test.pypi.org/project/altf1be_helpers)

* upload the library on PROD **pypi.org** 
    * `python -m twine upload dist/*` 
    * Source : [https://pypi.org/project/altf1be_helpers](https://pypi.org/project/altf1be_helpers)


## test the library altf1be_helpers

* `cd altf1be_helpers`
* `python altf1be_helpers_unittest.py`
* `python altf1be_json_helpers_unittest.py`

* locate the package 
    * `python -c "from altf1be_helpers import AltF1BeHelpers as _; print(_.__path__)"` **does not work yet**

* list functions inside the module
    *  the package `python -c "import altf1be_helpers as _; print(dir(_))"`

* test the package 
    * `python -c "from altf1be_helpers import AltF1BeHelpers; text='éê à iïî'; print(f'{AltF1BeHelpers.unicode_to_ascii(text)}')"`
    * result : `ee a iii`

## test the library altf1be_helpers

* `cd altf1be_helpers`

* `python altf1be_json_helpers_unittest.py`

* locate the package 
    * `python -c "from altf1be_json_helpers import AltF1BeJSONHelpers as _; print(_.__path__)"` **does not work yet**

* list functions inside the module
    *  the package `python -c "import altf1be_helpers as _; print(dir(_))"`

* test the package 
    * `python -c 'import os;from altf1be_helpers import AltF1BeJSONHelpers; altF1BeJSONHelpers = AltF1BeJSONHelpers();data = altF1BeJSONHelpers.load(os.path.join("data", "altf1be_sample.json"));print(data)'`
    * result : `{"name": "altf1be_json_helpers"}`

## Documentation

* Packaging Python Projects <https://packaging.python.org/tutorials/packaging-projects/>
* Managing Application Dependencies <https://packaging.python.org/tutorials/managing-dependencies/#managing-dependencies>
* Packaging and distributing projects <https://packaging.python.org/guides/distributing-packages-using-setuptools/#distributing-packages>

## License

Copyright (c) ALT-F1 SPRL, Abdelkrim Boujraf. All rights reserved.

Licensed under the EUPL License, Version 1.2.

See LICENSE in the project root for license information.
