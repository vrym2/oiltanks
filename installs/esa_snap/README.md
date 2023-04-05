# [ESA SNAP application](https://earth.esa.int/eogateway/tools/snap)

This folder consists of instructions and shell scripts to install ESA's SNAP with `snappy` python configuration in a Linux (Ubuntu) distribution. [ESA STEP FORUM](https://forum.step.esa.int/t/snappy-installation-in-ubuntu/37788) is a good place to for techincal discussions concenring ESA data and applications. The instructions are taken from there.

## Instructions to install ESA SNAP and configure `snappy` in Ubuntu x86_64 system

* Create a conda environment with `python3.9`. Later versions such as `python3.10` are not compatable with ESA SNAP yet.

*  Install GDAL in Ubuntu by running the following commands.
```
$ sudo add-apt-repository ppa:ubuntugis/ppa && sudo apt-get update
$ sudo apt-get install gdal-bin
$ sudo apt-get install libgdal-dev
$ export CPLUS_INCLUDE_PATH=/usr/include/gdal
$ export C_INCLUDE_PATH=/usr/include/gdal
$ pip install GDAL
```
If you encounter an error while running `pip install GDAL`, try the following.
```
$ ogrinfo --version # Copy the version number to the command below
$ pip install GDAL==<version-number>
```
Make sure to check that you can import `gdal` from `osgeo`. Run the following.
```
# Activate the conda environemnt
$ python -c 'from osgeo import gdal' # If there is an error saying 'version `GLIBCXX_3.4.30' not found'
# Run the following
$ ln -sf /usr/lib/x86_64-linux-gnu/libstdc++.so.6 /home/<user>/anaconda3/envs/<conda env>/lib/libstdc++.so.6 # Making a sym link
```

* Make sure JAVA is installed in the system by runnig the below command. Specifically JDK8.```diff - Note: Download the JDK8 that fits the system specifications exactly```
```
# JDK8 Installation
$ sudo chmod +x $HOME/oiltanks/installs/esa_snap/jdk.sh
$ bash $HOME/oiltanks/installs/esa_snap/jdk.sh
```
Add the following to the `$HOME/.profile`
```
# Set PATH to the JAVA
JAVA_HOME='/opt/jdk1.8.0_351'
if [ -d $JAVA_HOME ]; then
        PATH="$JAVA_HOME/bin:$PATH"
fi
```
Add this to the `$HOME/.bashrc`
```
# JAVA HOME
export JAVA_HOME="/usr/lib/jvm/jdk1.8.0_351" # With the specific version
```

* Type `java -version` to confirm the installation of JAVA in the system. Now install `Maven` by running the following commands. And also add the path to `$HOME/.profile`
```
$ sudo chmod +x $HOME/oiltanks/installs/esa_snap/maven.sh
$ bash $HOME/oiltanks/installs/esa_snap/maven.sh
```
```
# Set PATH to the MAVEN
M2_HOME='/opt/apache-maven-3.9.1'
if [ -d $M2_HOME ]; then
        PATH="$M2_HOME/bin:$PATH"
fi
```

* Run the following commands to download ESA SNAP application with their shell script, and follow the instructions.
```
$ wget -P $HOME/apps/tmp https://download.esa.int/step/snap/9.0/installers/esa-snap_sentinel_unix_9_0_0.sh
$ sudo chmod +x $HOME/apps/tmp/esa-snap_sentinel_unix_9_0_0.sh
$ bash $HOME/apps/tmp/esa-snap_sentinel_unix_9_0_0.sh
```

* Install `jpy`, a bi-direction java-python package by running the follwing commands.
```
$ git -C $HOME/apps/tmp clone https://github.com/jpy-consortium/jpy.git
$ python $HOME/apps/tmp/jpy setup.py build maven bdist_wheel 
# If there is any error, seacrh for solutions in the STEP forum, add `LD_LIBRARY_PATH` tp point out JDK8 in .bashrc
$ cp $HOME/apps/tmp/jpy/dist/jpy-0.9.0-cp39-cp39-linux_x86_64.whl $HOME/.snap/snap-python/snappy
```

* Configuring ESA SNAP for `snappy` and add the snappy package to `PYTHONPATH` in `.bashrc`
```
$ which python # Copy current conda env executable python
$ ./snap/bin/snappy-conf <paste python executable path>
```
```
# ESA snappy
export PYTHONPATH="${PYTHONPATH}:${HOME}/.snap/snap-python/"
```
* Check out the `snappy` python package 
```
$ python -c "from snappy import ProductIO" # If no error, installation is successful
```