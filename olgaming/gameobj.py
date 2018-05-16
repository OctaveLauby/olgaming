"""Class for major objects of a game (board, player, game itself, ...)"""
from collections import defaultdict

from olutils.log import LogClass
from olutils.params import read_params
from .parameters import LOGLVL


class GameObjMeta(type):
    """Meta class of GameObject

    > track ineheritance within GameObject.
    > init class attributes to avoid bounding
    """

    __inheritors__ = defaultdict(list)

    def __new__(mcs, clsname, superclasses, attributedict):
        """Create a new game class."""
        klass = type.__new__(mcs, clsname, superclasses, attributedict)
        for base in klass.mro()[1:-1]:  # skip current class
            mcs.__inheritors__[base].append(klass)
        return klass

    def __init__(cls, clsname, superclasses, attributedict):
        """Init game object class."""
        super().__init__(clsname, superclasses, attributedict)
        cls._logname = None
        cls._loglvl = LOGLVL
        cls._logpath = None


class GameObject(LogClass, metaclass=GameObjMeta):
    """Major object of game."""

    # ----------------------------------------------------------------------- #
    # Class methods

    @classmethod
    def dft_params(cls):
        """Return default params."""
        params = cls.dft_logparams()
        params.update({
            'identity': None,
        })
        return params

    @classmethod
    def dft_logparams(cls):
        """Return default log params."""
        return {
            'name': cls._logname,
            'loglvl': cls._loglvl,
            'logpath': cls._logpath
        }

    @classmethod
    def set_dft_loglvl(cls, level, propag=False):
        """Set default log level (use to create instances).

        Args:
            level (int or str):         readable log level for logging
            propag (bool, optional):    propagate to subclasses
        """
        if not propag:
            cls._loglvl = level
        else:
            cls._loglvl = level
            for subclass in GameObjMeta.__inheritors__[cls]:
                subclass.set_dft_loglvl(level=level, propag=True)

    # ---- Object counter

    counter = defaultdict(int)  # (class, number of instances) dict

    @classmethod
    def count(cls):
        """Return number of instances."""
        return GameObject.counter[cls]

    @staticmethod
    def reset_counter():
        """Reset counter of game objects.

        QUICKFIX: for tests, as counts are not reset between scripts
        """
        GameObject.counter = defaultdict(int)

    # ----------------------------------------------------------------------- #
    # Instances methods

    def __new__(cls, *args, **kwargs):
        """Create a new game object."""

        # # Disable pylint unused argument in method scope
        # pylint: disable=W0613

        # Update counter of all mother classes within GameObject
        GameObject.counter[GameObject] += 1
        for gameobj_cls in GameObjMeta.__inheritors__[GameObject]:
            if issubclass(cls, gameobj_cls):
                GameObject.counter[gameobj_cls] += 1
        return super().__new__(cls)

    def __init__(self, identity=None, **log_kwargs):
        """Init new game object."""
        if identity is None:
            identity = self.__class__.count()
        self._id = identity

        log_kwargs = read_params(log_kwargs, self.__class__.dft_logparams())
        if log_kwargs['name'] is None:
            log_kwargs['name'] = self.name
        super().__init__(**log_kwargs)

        self.log.debug("Created")

    @property
    def name(self):
        """Return name of instance"""
        return "%s_%s" % (self.__class__.__name__, self._id)

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    # ----------------------------------------------------------------------- #
    # Class decorators

    @classmethod
    def keep_doc(cls, method):
        """Decorator to override a method and keep documentation."""
        try:
            method.__doc__ = getattr(cls, method.__name__).__doc__
        except AttributeError:
            raise AttributeError(
                "%s is not an attribute of %s, so it can't be overwritten"
                % method.__name__, cls.__name__
            )
        return method
