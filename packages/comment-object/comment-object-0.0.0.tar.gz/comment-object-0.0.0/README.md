# comment

The `comment` Python library provides an explicit object for comments.

## Install

```
pip install comment-object
```

## Usage

You can use `Comment` as a context. It does nothing but expell all comments
from your source code!

```
from comment import Comment

with Comment("seconds") as c:
    DAY = 60 * 60 * 24
```

## Philosophy

A comment should have its scope inside some other code scope.

For example,

```
DAY = 60 * 60 * 24 # seconds
```

The comment "# seconds" explains `DAY` constant that it has the unit second.
The scope of this comment is this one line, inside module scope maybe.

A comment can be replaced with an object which does not have any effects on
the code around.

If a comment breaks the principle, then it is not a comment.
The coding comment, for example, can be such a type; it should be called a pragma.

## License

See LICENSE.txt.
