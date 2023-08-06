try:
    from .version import __version__, version_info
except ImportError:
    version_info = (0, 0, 0, "x")
    __version__ = "{}.{}.{}+{}".format(*version_info)

authors = (
    ("Dmitry Orlov", "me@mosquito.su"),
)

# TODO: Use mailing list instead
authors_email = ", ".join(
    str(email) for _, email in authors
)

__license__ = "MIT",
__author__ = ", ".join(
    "{0} <{1}>".format(name, email) for name, email in authors
)

package_info = "RSA helpers for PyJWT"

# It's same persons right now
__maintainer__ = __author__

__all__ = (
    "__author__", "__author__", "__license__",
    "__maintainer__", "__version__", "version_info",
)
