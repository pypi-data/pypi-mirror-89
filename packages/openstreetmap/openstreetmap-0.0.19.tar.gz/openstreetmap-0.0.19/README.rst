OpenStreetMap
=============

openstreetmap is a pure Python library that provides an easy way to extracting `OpenStreetMap`_ coordinates by name or relation id.

.. _OpenStreetMap: https://www.openstreetmap.org/

Code example
------------

python: ::

    # -*- coding: UTF-8 -*-
    from openstreemap import Crawler

    c = Crawler()
    boundary = c.name_parse('合肥市蜀山区', level='county',coo_order=True)
    # level: country state city county towns
    # coo_order  :False ->lng,lat ; True -> lat,lng  coo_order;
    print(boundary.info)
    boundary = c.id_parse("2458199", csys='wgs84', coo_order=True)
    # csys(Coordinate System): wgs84 gcj02 bd09
    print(boundary.info)

boundary.info: ::

    {'name': '', 'relation_id': '', 'boundary': {'outer': '', 'inner': ''}}

Installation
------------

PyPI version: ::

    $ pip install openstreetmap

Alternatively, you can also get the latest source code from `GitHub`_ and install it manually:

.. _GitLab: https://github.com/Mywayking/openstreetmap

::

    $ git clone https://github.com/Mywayking/openstreetmap
    $ cd openstreetmap
    $ python setup.py install

For update: ::

    $ pip install openstreetmap --upgrade


License
-------

