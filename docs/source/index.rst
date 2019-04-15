.. SQLAlchemy-Rope documentation master file, created by
   sphinx-quickstart on Sun Feb 24 01:43:54 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

The Simple Thread-local Session Maker
=====================================
|image1| |image2|

.. |image1| image:: https://img.shields.io/pypi/v/sqlalchemy-rope.svg
   :target: https://pypi.org/project/responder/
.. |image2| image:: https://img.shields.io/pypi/l/sqlalchemy-rope.svg
   :target: https://pypi.org/project/responder/

Powered by `Yamato Nagata <https://twitter.com/514YJ>`_.

SQLAlchemy-Rope provides simple thread-local session maker for SQLAlchemy.
`Github <https://github.com/delta114514/SQLAlchemy-Rope>`_ --
`Simple example <https://github.com/delta114514/SQLAlchemy-Rope/blob/master/example/example_2.py>`_

   I recommend to use :code:`sqlalchemy.orm.scoping.scoped_session` explicitly. There is some possibility of :code:`SessionJenny` dirty your code. This library is only for lazy people just like me.

.. contents::
   :local:
   :backlinks: none

Instllation
===========

Install with pip::

   $pip install sqlalchemy_rope

Configuring Application
=======================

make instance of :code:`SessionJenny` with :code:`sessionmaker`

.. code:: python

   from sqlalchemy import Integer, Column
   from sqlalchemy.orm.session import sessionmaker
   import sqlalchemy.ext.declarative
   
   from sqlalchemy_rope import SessionJenny
   
   Base = sqlalchemy.ext.declarative.declarative_base()
   
   url = "sqlite:///database.db"
   
   
   class Data(Base):
       __tablename__ = "database"
       id = Column(Integer, primary_key=True)
   
   
   engine = sqlalchemy.create_engine(url)
   Base.metadata.create_all(engine)
   SessionMaker = sessionmaker(bind=engine)
   
   jenny = SessionJenny(SessionMaker)

How It Works
============


Making :code:`SessionRope`
--------------------------
You can access :code:`Session` object with :code:`SessionJenny().session`

.. code:: python

   data = Data()
   
   jenny.session.add(data)
   jenny.session.commit()

:code:`SessionJenny` object make :code:`SessionRope` object when you call or use attribute of :code:`SessionJenny.rope`

And :code:`SessionJenny.session` returns `SessionJenny.rope.session`, So using :code:`SessionJenny.session` also makes :code:`SessionRope` object.

Where the :code:`SessionRope` object go? It's set as the local variable of first outer scope of :code:`SessionJenny` automatically. variable's name will be the return value of :code:`SessionJenny.create_rope_name()`

If you want to set explicitly, call :code:`SessionJenny.set_rope(frame=None)`. if :code:`frame` is given, :code:`SessionRope` will be set as local variable of :code:`frame`, or not, set as the local variable of first outer scope of :code:`SessionJenny`.

Calling `SessionRope`
---------------------

:code:`SessionJenny` object has :code:`_ropes` attribute. This is :code:`WeakValueDictionary` which key is :code:`SessionJenny.create_rope_name()`, value is :code:`SessionRope` made by using :code:`SessionJenny.rope` or :code:`SessionJenny.session`.

Every time you use :code:`SessionJenny.rope` or :code:`SessionJenny.session`, :code:`SessionJenny` will make :code:`SessionRope` if there is no :code:`SessionJenny` object stored in :code:`SessionJenny._ropes` which key is :code:`SessionJenny.create_rope_name()`.

Exiting Scope
-------------

:code:`SessionJenny` object make :code:`SessionRope` object as local variable. So, when exiting scope(finish running function/generator/coroutine), :code:`SessionRope` object will be deleted.

:code:`SessionRope` object run :code:`SessionRope.remove()` which is same as :code:`SQLAlchemy.orm.scoping.scoped_session.remove()`.


Documentation
=============

`SessionJenny(session_factory, scopefunc=None)`
---------------------------------------------------
Initialize :code:`SessionJenny`. All arguments will be passed to :code:`SQLAlchemy.orm.scoping.scoped_session`

`SessionJenny._rope_name_callback`
--------------------------------------
settable callback returns :code:`str` which will be :code:`SessionRope` variable's name. This has to be callable. Default is :code:`None`

`SessionJenny.set_rope(frame=None)`
---------------------------------------
Create :code:`SessionRope` object and set as local variable to :code:`frame.f_locals` if frame is provided. Otherwise, first outer scope of :code:`SessionJenny`.

`SessionJenny.rope`
-----------------------
Create :code:`SessionRope` object and set as local variable to first outer scope of :code:`SessionJenny` if there is no :code:`SessionJenny` object stored in :code:`SessionJenny._ropes` which key is :code:`SessionJenny.create_rope_name()`. And return :code:`SessionRope` object.

`SessionJenny.session`
--------------------------
Return :code:`SessionJenny.rope.session`

`SessionJenny.remove(rope_name=None)`
-----------------------------------------
Do as :code:`SQLAlchemy.orm.scoping.scoped_session.remove()`.
And remove data stored in :code:`SessionJenny._ropes` which key is :code:`rope_name` if :code:`rope_name` provided. Otherwise, :code:`SessionJenny._ropes` which key is :code:`SessionJenny.create_rope_name()` will be deleted.

`SessionRope(registry)`
---------------------------
In usual use, I recommend to use :code:`SessionJenny`, not :code:`SessionRope`.
But if you want to create :code:`SessionRope` explicitly, Use this.
register must be an instance of :code:`ScopedRegistry` or :code:`ThreadLocalRegistry`

`SessionRope.session`
-------------------------
Return :code:`self.registry()`

`SessionRope.remove()`
--------------------------
Do as :code:`SQLAlchemy.orm.scoping.scoped_session.remove()`.

Usage Example
=============

.. code:: python

   import responder

   from sqlalchemy import Integer, Column
   from sqlalchemy.orm.session import sessionmaker
   import sqlalchemy.ext.declarative

   from sqlalchemy_rope import SessionJenny

   api = responder.API()
   Base = sqlalchemy.ext.declarative.declarative_base()

   url = "sqlite:///data.db"


   class Data(Base):
       __tablename__ = "data"
       id = Column(Integer, primary_key=True)
       count = Column(Integer, default=0)


   engine = sqlalchemy.create_engine(url, echo=False)
   Base.metadata.create_all(engine)
   SessionMaker = sessionmaker(bind=engine)

   jenny = SessionJenny(SessionMaker)

   if not jenny.session.query(Data).all():
       data = Data()
       jenny.session.add(data)
       jenny.session.commit()


   @api.route("/")
   def index(req, resp):
       data = jenny.session.query(Data).first()
       data.count += 1
       jenny.session.commit()
       resp.content = str(data.count)


   def session_id():
       return id(jenny.session)


   if __name__ == "__main__":
       api.run()


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


In End
======
Sorry for my poor English.
I want **you** to join us and send many pull requests about Doc, code, features and more!!