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
(purple color recommended), no other distributions have even been remotely
tested. To install ``pimp``, first install pip using ``yum`` and
``virtualenv``::

  yum install python-pip virtualenv

After that, we'll bootstrap ``pimp`` with itself::

  TMPDIR=`mktemp -d` && virtualenv --distribute $TMPDIR && $TMPDIR/bin/pip install pimp && $TMPDIR/bin/pimp --python /usr/bin/python install pimp && rm -rf $TMPDIR

This will create temporary directory and a new virtual environment in it,
install ``pimp`` from github, use ``pimp`` to package itself, install that
package and remove the temporary directory.

Other useful things
-------------------

``pimp`` sets the release-version of every package it creates to ``pimp``. This
means that you can list all packages installed by it using::

  rpm -qa release="pimp"

Uninstalling all these is just as simple::

  sudo rpm -ve `rpm -qa release="pimp"`
