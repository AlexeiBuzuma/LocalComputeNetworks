***********************
Socket File Transmitter
***********************

Socket File Transmitter (SFT) is written as a set of laboratory works for 'System Software of Local Computer Networks' course. It should transmit files using tcp/udp sockets.

============
Installation
============

.. code-block:: shell

  $ sudo -H pip install -e $SFT_ROOT_DIR

In case of any difficulties with pip:

.. code-block:: shell

  $ sudo python setup.py clean --all
  $ sudo python setup.py install --force


=====
Usage
=====

Multiclient server
==================

.. code-block:: shell

  $ sft-multiclient-server
  $ sft-multiclient-client <server_ip:server_port> &


===========
Development
===========


===========
Future work
===========

* Enrich README filling
