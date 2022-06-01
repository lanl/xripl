# Instructions for installing XRIPL onto your local computer.

## Installing the latest release
[Official releases of XRIPL](https://pypi.org/project/xripl/) are published to pypi.org and can simply be pip installed like so:
```
pip install xripl
```

## Installing the latest development version of XRIPL (for contributors)

### Make sure you have python installed, preferably via Anaconda
Here is where you get Anaconda, and make sure to get the Python 3 version.
https://www.anaconda.com/distribution/

### Setup installation directory
Make a directory called "xripl" in a sensible place on your system. Preferably in a directory where none of the higher level directory names have spaces in them.

### Setup a virtual environment
If you have python installed via Anaconda, then create your virtual environment like this

```
conda create --name xripl
```

### Clone the repository using git
In the xripl directory you created, run the following on the command line

```
git clone https://github.com/lanl/xripl.git
```

### Activate your virtual environment
Still on the command line, run

```
source activate xripl
```

### Install requirements

```
pip install -r requirements.txt
```

### Install XRIPL
If you are a user then do

```
pip install .
```

If you wish to help in developing xripl, then do

```
pip install -e .
```

### Test if install was successful

Open a python and try doing `import xripl`. If all went well then you shouldn't get any error messages.
