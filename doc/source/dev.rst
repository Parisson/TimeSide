Development
===========

First, install TimeSide (see Install).

Then::

 sudo apt-get build-dep python-timeside
 sudo apt-get install git
 git clone https://github.com/yomguy/TimeSide.git
 cd TimeSide
 git checkout dev
 sudo pip install -e .
 echo "export PYTHONPATH=$PYTHONPATH:`pwd`" >> ~/.bashrc
 source ~/.bashrc
 tests/run_all_tests

VirtualBox and Vagrant
-----------------------

We also provide a vagrant box to install a virtual Debian system including TimeSide and all other dependencies.
First, install Vagrant and VirtualVox::

 sudo apt-get install vagrant virtualbox

On other OS, we need to install the packages correponding to your system:

 * Vagrant: https://www.vagrantup.com/downloads.html
 * VirtualBox: https://www.virtualbox.org/wiki/Downloads

Then setup our image box like this in a terminal::

 vagrant box add parisson/timeside-wheezy64 http://files.parisson.com/vagrant/timeside/parisson-timeside-wheezy64.box
 vagrant init parisson/timeside-wheezy64
 vagrant up
 vagrant ssh

To stop the virtual box::

 exit
 vagrant halt


Docker
-------

Docker is a great tool for developping and deploying processing environments! Our docker container includes all the necessary packages and environments for development and production with TimeSide.

First, install Docker: https://docs.docker.com/installation/

Then, simply pull our dev image and run::

  sudo docker pull yomguy/timeside
  sudo docker run -i -t yomguy/timeside bash

More infos: https://registry.hub.docker.com/u/yomguy/timeside/

To start the web server through the container::

  sudo docker run -p 9000:80 yomguy/timeside supervisord -n

Finally browse http://localhost:9000/api/

To start a new development, it is advised to checkout the dev branch and build your own container::

  cd TimeSide
  git checkout dev
  sudo docker build .

