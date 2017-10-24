olgaming
********

**olgaming is a collection of shell games, and tools to implement your own games**.


.. contents:: **Contents of this document**
   :depth: 2


Installation
============



.. code:: shell

    git clone https://github.com/OctaveLauby/olgaming.git
    cd olutils
    pip install -e .


Use
===

.. code:: python3

    from gaming.games import Dummy

    game = Dummy(
        bots=[1],  # You are player 1 (index 0)
        loglvl='ERROR',
    )
    game.play()
