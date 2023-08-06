Makeprompt
==========

Advanced shell prompts for ZSH.

.. image:: https://img.shields.io/pypi/v/makeprompt
    :target: https://pypi.org/project/makeprompt/
    :alt: PyPI

.. image:: https://img.shields.io/pypi/l/makeprompt?color=%234CAF50
    :target: https://pypi.org/project/makeprompt/
    :alt: PyPI - License


Usage
-----

Install it::

    pip install --user makeprompt

Put this in your ``~/.zshrc``::

    autoload -Uz promptinit
    promptinit
    prompt off
    setopt PROMPT_SUBST

    PROMPT='$( ~/.local/bin/makeprompt )'


Features
--------

- Display user/hostname/path using truecolor (24-bit) colors
- 8-bit color fallbacks, for terminals that don't support truecolor
- git repository status information (branch, dirty)
- Python enabled virtualenv information
- Background (stopped) jobs count


Customize
---------

The ``MAKEPROMPT_COLORS`` environment variable can be used to change
colors of different parts of the prompt.

Format is similar to ``LS_COLORS``, for example::

    export MAKEPROMPT_COLORS='user=38;2;56;142;60:host=38;2;198;255;0'

A utility script is provided to conveniently generate TrueColor
paletters from HTML hex colors.

For example::

    python -m makeprompt.utils.make_truecolor_palette user='#808' host='#f0f' path='#ff0'


you can also use this in your shell configuration::

    eval $( python -m makeprompt.utils.make_truecolor_palette ... )
    export MAKEPROMPT_COLORS


Development
-----------

To test a development version, checked out in ``~/Projects/makeprompt``:

    PROMPT='$( PYTHONPATH="$HOME"/Projects/makeprompt python -m makeprompt )'
