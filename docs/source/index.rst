.. service-image-colorization documentation master file, created by
   sphinx-quickstart on Sat Dec 22 17:25:32 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to service-image-colorization's documentation!
======================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Overview
========

This web service is created as a pet project for learning Vue.js.
The code might be of interest to those who want to colorize some pictures with peeking in the internals.

Installation
=============

The easiest way to run the service is with docker:

.. code-block:: shell

  make dockerrun

Web page will be at http://localhost:8080/

Or you can build the docker image by yourself:

.. code-block:: shell

  docker build -t service-image-colorization .


If you want to build code from scratch without docker container, you should do the following:

#. Get the Python3. Versions 3.6 and 3.7 will do
#. Install caffe as written in `their instructions <http://caffe.berkeleyvision.org/installation.html>`_.
#. Install node.js and npm
#. Install npm packages as

   .. code-block:: shell

      make vendorjs

#. Build vue.js pages as

   .. code-block:: shell

     make buildjs

#. Install python requirements as

   .. code-block:: shell

     pip install -r requirements.txt

#. And finally, run the python application as

   .. code-block:: shell

     make run

Usage
=====

Service can colorize any png or jpg image.

Gallery
-------

Gallery is basically the viewer of your colorization history.

