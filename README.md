# SQLAlchemy-Rope
The Simple Thread-local Session Maker

```python

from sqlalchemy import Integer, Column
from sqlalchemy.orm.session import sessionmaker
import sqlalchemy.ext.declarative

from sqlalchemy_rope import SessionJenny

Base = sqlalchemy.ext.declarative.declarative_base()

url = "sqlite:///database.db"


class Database(Base):
    __tablename__ = "database"
    id = Column(Integer, primary_key=True)


engine = sqlalchemy.create_engine(url)
Base.metadata.create_all(engine)
SessionMaker = sessionmaker(bind=engine)

jenny = SessionJenny(SessionMaker)
print(jenny.session is jenny.session)  # Now This "session" object is thread-local!!

```
Powered by [Yamato Nagata](https://twitter.com/514YJ)

[Simple Example](https://github.com/delta114514/SQLAlchemy-Rope/blob/master/example/example_1.py)

[ReadTheDocs](https://sqlalchemy-rope.readthedocs.io/en/latest/)


# Usage

make instance of `SessionJenny` with `sessionmaker`

```python
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
```

now you can access `Session` object with `SessionJenny().session`

```python
data = Data()

jenny.session.add(data)
jenny.session.commit()

```
# How This Works?


## Making `SessionRope`
`SessionJenny` object make `SessionRope` object when you call or use attribute of `SessionJenny.rope`

And `SessionJenny.session` returns `SessionJenny.rope.session`, So using `SessionJenny.session` also makes `SessionRope` object.

Where the `SessionRope` object go? It's set as the local variable of first outer scope of `SessionJenny` automatically. variable's name will be the return value of `SessionJenny.create_rope_name()`

If you want to set explicitly, call `SessionJenny.set_rope(frame=None)`. if `frame` is given, `SessionRope` will be set as local variable of `frame`, or not, set as the local variable of first outer scope of `SessionJenny`.

## Calling `SessionRope`
`SessionJenny` object has `_ropes` attribute. This is `WeakValueDictionary` which key is `SessionJenny.create_rope_name()`, value is `SessionRope` made by using `SessionJenny.rope` or `SessionJenny.session`.

Every time you use `SessionJenny.rope` or `SessionJenny.session`, `SessionJenny` will make `SessionRope` if there is no `SessionJenny` object stored in `SessionJenny._ropes` which key is `SessionJenny.create_rope_name()`.

## Exiting Scope
`SessionJenny` object make `SessionRope` object as local variable. So, when exiting scope(finish running function/generator/coroutine), `SessionRope` object will be deleted.

`SessionRope` object run `SessionRope.remove()` which is same as `SQLAlchemy.orm.scoping.scoped_session.remove()`.

# Documentation

### SessionJenny(session_factory, scopefunc=None)
Initialize `SessionJenny`. All arguments will be passed to `SQLAlchemy.orm.scoping.scoped_session`

### SessionJenny._rope_name_callback
settable callback returns `str` which will be `SessionRope` variable's name. This has to be callable. Default is `None`

### SessionJenny.set_rope(frame=None)
Create `SessionRope` object and set as local variable to `frame.f_locals` if frame is provided. Otherwise, first outer scope of `SessionJenny`.

### SessionJenny.rope
Create `SessionRope` object and set as local variable to first outer scope of `SessionJenny` if there is no `SessionJenny` object stored in `SessionJenny._ropes` which key is `SessionJenny.create_rope_name()`. And return `SessionRope` object.

### SessionJenny.session
Return `SessionJenny.rope.session`

### SessionJenny.remove(rope_name=None)
Do as `SQLAlchemy.orm.scoping.scoped_session.remove()`.
And remove data stored in `SessionJenny._ropes` which key is `rope_name` if `rope_name` provided. Otherwise, `SessionJenny._ropes` which key is `SessionJenny.create_rope_name()` will be deleted.

### SessionRope(registry)
In usual use, I recommend to use `SessionJenny`, not `SessionRope`.
But if you want to create `SessionRope` explicitly, Use this.
register must be an instance of `ScopedRegistry` or `ThreadLocalRegistry`

### SessionRope.session
Return `self.registry()`

### SessionRope.remove()
Do as `SQLAlchemy.orm.scoping.scoped_session.remove()`.
