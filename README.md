# zero-paper

pi zero paper station

## components

* pi zero w /w headers
* wavesahre epaper display hat 264x176

Example 

![Sample screen](img/output_image_with_text.png)

## Installation

* sudo apt-get install libfreetype6-dev swig
* python3 -m venv acme-venv --system-site-packages
* pip install -r requirements.txt

In **this exact order**.  Failure to do so will build PIL without
freetype support
