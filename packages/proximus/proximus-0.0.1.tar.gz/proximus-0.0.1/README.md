# BBOX3 API
This API have been written in Python using Selenium, Firefox and Geckodriver. It can works on a server (headless)

## Setting up
1. Install Firefox

```bash
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A6DCF7707EBC211F
sudo apt-add-repository "deb http://ppa.launchpad.net/ubuntu-mozilla-security/ppa/ubuntu bionic main"
sudo apt-get update
sudo apt-get install firefox
```

2. Install Geckodriver

```bash
wget https://github.com/mozilla/geckodriver/releases/download/v0.28.0/geckodriver-v0.28.0-linux64.tar.gz
tar xfvz geckodriver*.tar.gz
sudo mv geckodriver /usr/bin/geckodriver
```

3. Install Python3 and Pip3

```bash
sudo apt-get update
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get install python3 python3-pip
```

4. Install Selenium

```bash
pip3 install selenium
```

## Quickstart

```python
# Load the module, open the browser and login (mandatory at the start)
from proximus import *
b = newInstance(headless=True)
login(b, "yourpassword")

# What you want to execute (you can find all the functions below)
toggleHotspot(b)

# Close the browser (mandatory at the end)
b.close()
```

## Documentation
To get the documentation, simply run:

```python
import proximus
help(proximus)
```
