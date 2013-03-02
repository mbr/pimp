Python Install Magic Package
============================

Python packaging is complicated and often clashes with distro package managers.
To make things worse, now there's ``pimp``. It uses `pip
<https://pypi.python.org/pypi/pip>`_ and `distutils
http://docs.python.org/2/library/distutils.html`_ to download packages from
PyPI and build RPMs out of them, which it installs using the system's package
management.

Requirements and Installation
-----------------------------

Every self-respecting ``pimp`` needs a `Fedora <http://fedoraproject.org/>`_
(purple color recommended), no other distributions have even been tested. To
install ``pimp``, first install pip and virtualenv using yum::

  yum install python-pip virtualenv

After that, we'll bootstrap pimp with itself::

  TMPDIR=`mktemp -d` && virtualenv --distribute $TMPDIR && $TMPDIR/bin/pip install pimp -U && $TMPDIR/bin/pimp --python /usr/bin/python install pimp -U && rm -rf $TMPDIR

This will create temporary directory and a new virtual environment in it,
install ``pimp`` from PyPI, use ``pimp`` to package itself, install that
package and remove the temporary directory.

The good parts
--------------

``/usr/local`` aside, there shouldn't be any files in your ``/usr`` directory
that aren't managed by the package manager (and even then I'm not even fond of
installing stuff into ``/usr/local``). When you use ``pip`` to install packages
system-wide, they end up ``/usr``, without the ``local``-part.

``pimp`` tries to remedy this situation, by giving you a way to install
packages through auto-generated rpm-packages that can be uninstalled cleanly.

The bad parts
-------------

As of spring 2013, Python packaging is a complete mess (just google distutils,
distutils2, setuptools, distlib, packaging, pip, easy_install or any other
crazy piece of software messing with packages). Since ``pimp`` largely relies
on some of these, there are a few issues described below. The general message
here is though, only use ``pimp`` for the one thing it is intended: Installing
the occasional script system-wide. [1]_

Only use PyPI-packages
~~~~~~~~~~~~~~~~~~~~~~

``pip`` does not support local filesystem packages or checkouts using
``git+git://``-urls in the same way it does PyPI downloads. This makes it hard
to support these, so for now[2]_, only PyPI packages are
supported.

RPM-names
~~~~~~~~~

For reasons unknown, distutils' ``bdist_rpm`` command allows a lot of
customization - but not the RPM name. Your best is hoping that you do not run
into a naming conflict with another package. On the bright side, you'll be
warned by ``rpm`` beforehand and nothing should break.

Useful things
-------------------

``pimp`` sets the release-version of every package it creates to ``pimp``. This
means that you can list all packages installed by it using::

  rpm -qa release="pimp"

Uninstalling all these is just as simple::

  sudo rpm -ve `rpm -qa release="pimp"`

.. [1]: A good use case is if you have command-line tools from PyPI (e.g.
   `hitnrun <https://pypi.python.org/pypi/hitnrun>`_) that you run in many
   projects, but don't want to reinstall for every virtualenv.

.. [2]: And possibly a long, long time...
