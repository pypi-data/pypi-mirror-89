Emoji
=====

Emoji for Python.  This project was inspired by `kyokomi <https://github.com/kyokomi/emoji>`__.


Example
-------

The entire set of Emoji codes as defined by the `unicode consortium <http://www.unicode.org/Public/emoji/1.0/full-emoji-list.html>`__
is supported in addition to a bunch of `aliases <http://www.emoji-cheat-sheet.com/>`__.  By
default, only the official list is enabled but doing ``emoji.emojize(use_aliases=True)`` enables
both the full list and aliases.

.. code-block:: python

    >> import emoji_vietnamese

    >> print(emoji_vietnamese.demojize('Dịu dàng chiếm cả thế gian Càng khôn ngoan lắm càng ngang trái nhiều 😉😂'))
    >> Dịu dàng chiếm cả thế gian Càng khôn ngoan lắm càng ngang trái nhiều icon mặt nháy mắt icon icon khuôn mặt với những giọt nước mắt của niềm vui icon


Installation
------------

Via pip:

.. code-block:: console

    $ pip install emoji --upgrade

From master branch:

.. code-block:: console

    $ git clone https://github.com/carpedm20/emoji.git
    $ cd emoji
    $ python setup.py install


https://viblo.asia/p/huong-dan-tao-package-python-RnB5pBvDZPG