olgaming
********

**olgaming is a python 3 collection of shell games, and tools to implement your own games**. It aims to provide environments (mainly board games) for Machine Learning developpement, and an easy way to implement more.

.. contents:: **Contents of this document**
   :depth: 2



Installation
============

One can install the package following those steps.


Install package
---------------

.. code:: shell

    git clone https://github.com/OctaveLauby/olgaming.git
    cd olgaming
    pip3 install -e .


Install requirements
--------------------

**Warning:** olutils must be install manually, see `documentation <https://github.com/OctaveLauby/olutils>`_.

.. code:: shell

    pip3 install -r requirements.txt



Examples
========

Here is a basic example of how to launch a game:

.. code:: python

    from olgaming.games import Dummy

    game = Dummy(
        bots=[1],           # You are player 1 (index 0)
        loglvl='ERROR',
    )
    game.play()             # Follow instructions


It is possible to launch any game using `play <https://github.com/OctaveLauby/olgaming/blob/master/play.py>`_ script :

.. code:: bash

    python play.py -h
    python play.py Dummy
    python play.py TicTacToe -b 0
