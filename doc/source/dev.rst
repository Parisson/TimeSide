Development
===========

For versions >=0.5 on Debian 7 Wheezy:

.. code-block:: bash

 $ echo "deb http://debian.parisson.com/debian/ stable main" | sudo tee -a /etc/apt/sources.list
 $ echo "deb-src http://debian.parisson.com/debian/ stable main" | sudo tee -a /etc/apt/sources.list
 $ sudo apt-get update
 $ sudo apt-get install git
 $ sudo apt-get build-dep python-timeside

 $ git clone https://github.com/yomguy/TimeSide.git
 $ cd TimeSide
 $ git checkout dev
 $ sudo pip install -e .
 $ python tests/run_all_tests

