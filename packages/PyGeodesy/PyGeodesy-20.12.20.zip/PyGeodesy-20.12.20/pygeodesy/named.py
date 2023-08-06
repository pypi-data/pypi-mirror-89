
# -*- coding: utf-8 -*-

u'''(INTERNAL) Classes C{_Named}, C{_NamedDict} and C{_NamedTuple},
all with nameable instances and several subclasses thereof.

In addition, the items in a C{_NamedDict} are accessable as attributes
and the items in a C{_NamedTuple} can be named to be accessable as
attributes, similar to standard Python C{namedtuple}s.

@see: Module L{pygeodesy.namedTuples} for the C{Named-Tuples}.

@newfield example: Example, Examples
'''

from pygeodesy.basics import isclass, isidentifier, iskeyword, isstr, issubclassof, \
                             property_doc_, property_RO, _xcopy
from pygeodesy.errors import _AssertionError, _AttributeError, _incompatible, \
                             _IndexError, _IsnotError, LenError, _NameError, \
                             _NotImplementedError, _TypeError, _TypesError, \
                             _ValueError, UnitError, _xkwds, _xkwds_popitem
from pygeodesy.interns import NN, _AT_, _COLON_, _COLONSPACE_, _COMMASPACE_, \
                             _doesn_t_exist_, _DOT_, _DUNDER_, _dunder_name, \
                             _EQUAL_, _immutable_, _invalid_, _name_, _other_, \
                             _s_, _SPACE_, _UNDER_, _valid_, _vs_
from pygeodesy.lazily import _ALL_DOCS, _ALL_LAZY, _caller3
from pygeodesy.streprs import attrs, Fmt, pairs, reprs, unstr

__all__ = _ALL_LAZY.named
__version__ = '20.12.18'

_at_     = 'at'
_del_    = 'del'
_exists_ = 'exists'
_I_      = 'I'
_item_   = 'item'
_MRO_    = 'MRO'
_O_      = 'O'
# __DUNDER gets mangled in class
_name     = '_name'
_n_a_m_e_ = '__name__'  # no __name__
_Names_   = '_Names_'
_Units_   = '_Units_'


def _xjoined_(prefix, name):
    '''(INTERNAL) Join C{pref} and non-empty C{name}.
    '''
    return _SPACE_(prefix, repr(name)) if name and prefix else (prefix or name)


def _xnamed(inst, name, force=False):
    '''(INTERNAL) Set the instance' C{.name = }B{C{name}}.

       @arg inst: The instance (C{_Named}).
       @arg name: The name (C{str}).
       @kwarg force: Force name change (C{bool}).

       @return: The B{C{inst}}, named if B{C{force}}d or
                not named before.
    '''
    if name and isinstance(inst, _Named) \
            and (force or not inst.name):
        inst.name = name
    return inst


def _xother3(inst, other, name=_other_, up=1, **name_other):
    '''(INTERNAL) Get C{name} and C{up} for a named C{other}.
    '''
    if name_other:  # and not other and len(name_other) == 1
        name, other = _xkwds_popitem(name_other)
    elif other and len(other) == 1:
        other = other[0]
    else:
        raise _AssertionError(name, other, txt=classname(inst, prefixed=True))
    return other, name, up


def _xotherError(inst, other, name=_other_, up=1):
    '''(INTERNAL) Return a C{_TypeError} for an incompatible, named C{other}.
    '''
    n = _callname(name, classname(inst, prefixed=True), inst.name, up=up + 1)
    return _TypeError(name, other, txt=_incompatible(n))


def _xvalid(name, _OK=False):
    '''(INTERNAL) Check valid attribute name C{name}.
    '''
    return True if (name and isstr(name)
                         and name != _name_
                         and (_OK or not name.startswith(_UNDER_))
                         and (not iskeyword(name))
                         and isidentifier(name)) else False


class _Named(object):
    '''(INTERNAL) Root class for named objects.
    '''
    _name        = NN     # name (C{str})
    _classnaming = False  # prefixed (C{bool})

    def __repr__(self):
        '''Default C{repr(self)}.
        '''
        return Fmt.ANGLE(_SPACE_(self, _at_, hex(id(self))))

    def __str__(self):
        '''Default C{str(self)}.
        '''
        return self.named2

    def attrs(self, *names, **kwds):
        '''Join attributes as C{name=value} pairs.

           @arg names: The attribute names (C{str}s).
           @kwarg kwds: Keyword argument for function L{attrs}.

           @return: All C{name=value} pairs joined (C{str}).
        '''
        return _COMMASPACE_.join(attrs(self, *names, **kwds))

    @property_RO
    def classname(self):
        '''Get this object's C{[module.]class} name (C{str}), see
           property C{.classnaming} and function C{classnaming}.
        '''
        return classname(self, prefixed=self._classnaming)

    @property_doc_(''' the class naming (C{bool}).''')
    def classnaming(self):
        '''Get the class naming (C{bool}), see function C{classnaming}.
        '''
        return self._classnaming

    @classnaming.setter  # PYCHOK setter!
    def classnaming(self, prefixed):
        '''Set the class naming for C{[module.].class} names.

           @arg prefixed: Include the module name (C{bool}).
        '''
        self._classnaming = bool(prefixed)

    def classof(self, *args, **kwds):
        '''Create another instance of this very class.

           @arg args: Optional, positional arguments.
           @kwarg kwds: Optional, keyword arguments.

           @return: New instance (B{self.__class__}).
        '''
        return _xnamed(self.__class__(*args, **kwds), self.name)

    def copy(self, deep=False):
        '''Make a shallow or deep copy of this instance.

           @kwarg deep: If C{True} make a deep, otherwise
                          a shallow copy (C{bool}).

           @return: The copy (C{This class} or subclass thereof).
        '''
        return _xcopy(self, deep=deep)

    def _DOT_(self, *names):
        '''(INTERNAL) Period-join C{self.name} and C{names}.
        '''
        return _DOT_(self.name, *names)

    @property_doc_(''' the name (C{str}).''')
    def name(self):
        '''Get the name (C{str}).
        '''
        return self._name

    @name.setter  # PYCHOK setter!
    def name(self, name):
        '''Set the name.

           @arg name: New name (C{str}).
        '''
        self._name = str(name)
        # to set the name from a sub-class, use
        # self.name = name or
        # _Named.name.fset(self, name), but not
        # _Named(self).name = name

    @property_RO
    def named(self):
        '''Get the name I{or} class name or C{""} (C{str}).
        '''
        return self.name or self.classname

    @property_RO
    def named2(self):
        '''Get the C{class} name I{and/or} the name or C{""} (C{str}).
        '''
        return _xjoined_(self.classname, self.name)

    @property_RO
    def named3(self):
        '''Get the I{prefixed} C{class} name I{and/or} the name or C{""} (C{str}).
        '''
        return _xjoined_(classname(self, prefixed=True), self.name)

    @property_RO
    def named4(self):
        '''Get the C{package.module.class} name I{and/or} the name or C{""} (C{str}).
        '''
        return _xjoined_(_DOT_(self.__module__, self.__class__.__name__),  self.name)

    def toRepr(self, **unused):  # PYCHOK expected
        '''Default C{repr(self)}.
        '''
        return repr(self)

    toStr2 = toRepr  # PYCHOK for backward compatibility
    '''DEPRECATED, used method C{toRepr}.'''

    def toStr(self, **unused):  # PYCHOK expected
        '''Default C{str(self)}.
        '''
        return str(self)

    def _xnamed(self, inst, name=NN):
        '''(INTERNAL) Set the instance' C{.name = self.name}.

           @arg inst: The instance (C{_Named}).
           @kwarg name: Optional name, overriding C{self.name} (C{str}).

           @return: The B{C{inst}}, named if not named before.
        '''
        n = name or self.name
        return _xnamed(inst, n) if n else inst

    def _xrenamed(self, inst):
        '''(INTERNAL) Rename the instance' C{.name = self.name}.

           @arg inst: The instance (C{_Named}).

           @return: The B{C{inst}}, named if not named before.
        '''
        if not isinstance(inst, _Named):
            raise _IsnotError(_valid_, inst=inst)

        if inst.name != self.name:
            inst.name = self.name
        return inst


class _NamedBase(_Named):
    '''(INTERNAL) Base class with name.
    '''

    def __repr__(self):
        '''Default C{repr(self)}.
        '''
        return self.toRepr()

    def __str__(self):
        '''Default C{str(self)}.
        '''
        return self.toStr()

    def _update(self, updated, *attrs):
        '''(INTERNAL) Zap cached instance attributes.
        '''
        if updated and attrs:
            for a in attrs:  # zap attrs to None
                if getattr(self, a, None) is not None:
                    setattr(self, a, None)
                elif not hasattr(self, a):
                    a = NN(_DOT_, a, _SPACE_, _invalid_)
                    raise _AssertionError(a, txt=repr(self))

#   def notImplemented(self, attr):
#       '''Raise error for a missing method, function or attribute.
#
#          @arg attr: Attribute name (C{str}).
#
#          @raise NotImplementedError: No such attribute.
#       '''
#       c = self.__class__.__name__
#       return NotImplementedError(_DOT_(c, attr))

    def others(self, *other, **name_other_up):  # see .points.LatLon_.others
        '''Refined class comparison, invoked as C{.others(other=other)},
           C{.others(name=other)} or C{.others(other, name='other')}.

           @arg other: The other instance (L{any}).
           @kwarg name_other_up: Overriding C{name=other} and C{up=1}
                                 keyword arguments.

           @return: The B{C{other}} iff compatible with this instance's
                    C{class} or C{type}.

           @raise TypeError: Mismatch of the B{C{other}} and this
                             instance's C{class} or C{type}.
        '''
        if other:  # most common, just one arg B{C{other}}
            other0 = other[0]
            if isinstance(other0, self.__class__) or \
               isinstance(self, other0.__class__):
                return other0

        other, name, up = _xother3(self, other, **name_other_up)
        if isinstance(self, other.__class__) or \
           isinstance(other, self.__class__):
            return other

        raise _xotherError(self, other, name=name, up=up + 1)

    def toRepr(self, **kwds):  # PYCHOK expected
        '''(INTERNAL) I{Could be overloaded}.

           @kwarg kwds: Optional, keyword arguments.

           @return: C{toStr}() with keyword arguments (as C{str}).
        '''
        t = self.toStr(**kwds).lstrip('([{').rstrip('}])')
        return Fmt.PAREN(self.classname, t)  # XXX (self.named, t)

#   def toRepr(self, **kwds)
#       if kwds:
#           s = NN.join(reprs((self,), **kwds))
#       else:  # super().__repr__ only for Python 3+
#           s = super(self.__class__, self).__repr__()
#       return Fmt.PAREN(self.named, s)  # clips(s)

    def toStr(self, **kwds):  # PYCHOK no cover
        '''(INTERNAL) I{Must be overloaded}.

           @raise AssertionError: Always, see function L{notOverloaded}.
        '''
        notOverloaded(self, self.toStr, **kwds)

#   def toStr(self, **kwds):
#       if kwds:
#           s = NN.join(strs((self,), **kwds))
#       else:  # super().__str__ only for Python 3+
#           s = super(self.__class__, self).__str__()
#       return s


class _NamedDict(dict, _Named):
    '''(INTERNAL) Named C{dict} with key I{and} attribute
       access to the items.
    '''

    def __init__(self, *args, **kwds):
        if args:  # args override kwds
            if len(args) != 1:
                t = unstr(self.classname, *args, **kwds)
                raise _ValueError(args=len(args), txt=t)
            kwds = _xkwds(dict(args[0]), **kwds)
        if _name_ in kwds:
            _Named.name.fset(self, kwds.pop(_name_))  # see _Named.name
        dict.__init__(self, kwds)

    def __delattr__(self, name):
        '''Delete an attribute or item by B{C{name}}.
        '''
        if name in dict.keys(self):
            dict.pop(name)
        elif name in (_name_, _name):
            dict.__setattr__(self, name, NN)
        else:
            dict.__delattr__(self, name)

    def __getattr__(self, name):
        '''Get the value of an attribute or item by B{C{name}}.
        '''
        try:
            return self[name]
        except KeyError:
            if name == _name_:
                return _Named.name.fget(self)
            return dict.__getattr__(self, name)

    def __getitem__(self, key):
        '''Get the value of an item by B{C{key}}.
        '''
        if key == _name_:
            raise KeyError(Fmt.SQUARE(self.classname, key))
        return dict.__getitem__(self, key)

    def __repr__(self):
        '''Default C{repr(self)}.
        '''
        return self.toRepr()

    def __setattr__(self, name, value):
        '''Set attribute or item B{C{name}} to B{C{value}}.
        '''
        if name in dict.keys(self):
            dict.__setitem__(self, name, value)  # self[name] = value
        else:
            dict.__setattr__(self, name, value)

    def __setitem__(self, key, value):
        '''Set item B{C{key}} to B{C{value}}.
        '''
        if key == _name_:
            raise KeyError(_EQUAL_(Fmt.SQUARE(self.classname, key), repr(value)))
        dict.__setitem__(self, key, value)

    def __str__(self):
        '''Default C{str(self)}.
        '''
        return self.toStr()

    def toRepr(self, prec=6, fmt=Fmt.F):  # PYCHOK _Named
        '''Like C{repr(dict)} but with C{name} and  C{floats} formatting by C{fstr}.
        '''
        t = pairs(self.items(), prec=prec, fmt=fmt, sep=_EQUAL_)
        return Fmt.PAREN(self.name, _COMMASPACE_.join(sorted(t)))

    toStr2 = toRepr  # PYCHOK for backward compatibility
    '''DEPRECATED, use method C{toRepr}.'''

    def toStr(self, prec=6, fmt=Fmt.F):  # PYCHOK _Named
        '''Like C{str(dict)} but with C{floats} formatting by C{fstr}.
        '''
        t = pairs(self.items(), prec=prec, fmt=fmt, sep=_COLONSPACE_)
        return Fmt.CURLY(_COMMASPACE_.join(sorted(t)))


class _NamedEnum(_NamedDict):
    '''(INTERNAL) Enum-like C{_NamedDict} with attribute access
       restricted to valid keys.
    '''
    _item_Classes = ()

    def __init__(self, Class, *Classes, **name):
        '''New C{_NamedEnum}.

           @arg Class: Initial class or type acceptable as enum
                       values (C{str}).
           @arg Classes: Additional, acceptable classes or types.
        '''
        self._item_Classes = (Class,) + Classes
        n = name.get(_name_, NN) or NN(Class.__name__, _s_)
        if n and _xvalid(n, _OK=True):
            _Named.name.fset(self, n)  # see _Named.name

    def __getattr__(self, name):
        '''Get the value of an attribute or enum by B{C{name}}.
        '''
        try:
            return self[name]
        except KeyError:
            if name == _name_:
                return _NamedDict.name.fget(self)
        raise _AttributeError(item=self._DOT_(name), txt=_doesn_t_exist_)

    def __repr__(self):
        '''Default C{repr(self)}.
        '''
        return self.toRepr()

    def __str__(self):
        '''Default C{str(self)}.
        '''
        return self.toStr()

    def _assert(self, **kwds):
        '''(INTERNAL) Check names against given, registered names.
        '''
        for a, v in kwds.items():
            assert self[a] is v and getattr(self, a) \
                                and self.find(v) == a

    def find(self, item):
        '''Find a registered item.

           @arg item: The item to look for (any C{type}).

           @return: If found the B{C{item}}'s name (C{str}), C{None} otherwise.
        '''
        for k, v in self.items():
            if v is item:
                return k
        return None

    def register(self, item):
        '''Registed a new item.

           @arg item: The item (any C{type}).

           @return: The item name (C{str}).

           @raise NameError: An B{C{item}} already registered with
                             that name or the B{C{item}} has no, an
                             empty or an invalid name.

           @raise TypeError: The B{C{item}} type invalid.
        '''
        try:
            n = item.name
            if not (n and isstr(n) and isidentifier(n)):
                raise ValueError
        except (AttributeError, ValueError, TypeError) as x:
            raise _NameError(_DOT_(_item_, _name_), item, txt=str(x))
        if n in self:
            raise _NameError(self._DOT_(n), item, txt=_exists_)
        if not (self._item_Classes and isinstance(item, self._item_Classes)):
            raise _TypesError(self._DOT_(n), item, *self._item_Classes)
        self[n] = item

    def unregister(self, name_or_item):
        '''Remove a registered item.

           @arg name_or_item: Name (C{str}) of or the item (any C{type}).

           @return: The unregistered item.

           @raise NameError: No item with that B{C{name}}.

           @raise ValueError: No such item.
        '''
        name = self.find(name_or_item)
        if name is None:
            if not isstr(name_or_item):
                raise _ValueError(name_or_item=name_or_item)
            name = name_or_item
        try:
            item = dict.pop(self, name)
        except KeyError:
            raise _NameError(item=self._DOT_(name), txt=_doesn_t_exist_)
        item._enum = None
        return item

    def toRepr(self, prec=6, fmt=Fmt.F, sep=',\n'):  # PYCHOK _NamedDict
        '''Like C{repr(dict)} but with C{name} and C{floats} formatting by C{fstr}.
        '''
        t = sorted((self._DOT_(n), v) for n, v in self.items())
        return sep.join(pairs(t, prec=prec, fmt=fmt, sep=_COLONSPACE_))

    toStr2 = toRepr  # PYCHOK for backward compatibility
    '''DEPRECATED, use method C{toRepr}.'''

    def toStr(self, *unused):  # PYCHOK _NamedDict
        '''Like C{str(dict)} but with C{floats} formatting by C{fstr}.
        '''
        return self._DOT_(', .'.join(sorted(self.keys())))


class _NamedEnumItem(_NamedBase):
    '''(INTERNAL) Base class for items in a C{_NamedEnum} registery.
    '''
    _enum = None

    def __ne__(self, other):
        '''Compare this and an other item.

           @return: C{True} if different, C{False} otherwise.
        '''
        return not self.__eq__(other)

    def _instr(self, prec, *attrs, **kwds):
        '''(INTERNAL) Format, used by C{Conic}, C{Ellipsoid}, C{Transform}.
        '''
        t = Fmt.EQUAL(_name_, repr(self.name)),
        if attrs:
            t += pairs(((a, getattr(self, a)) for a in attrs),
                       prec=prec, ints=True)
        if kwds:
            t += pairs(kwds, prec=prec)
        return _COMMASPACE_.join(t)

    @property_doc_(''' the I{registered} name (C{str}).''')
    def name(self):
        '''Get the I{registered} name (C{str}).
        '''
        return self._name

    @name.setter  # PYCHOK setter!
    def name(self, name):
        '''Set the name, unless already registered.

           @arg name: New name (C{str}).
        '''
        if self._enum:
            raise _NameError(str(name), self, txt='registered')  # XXX _TypeError
        self._name = str(name)

    def _register(self, enum, name):
        '''(INTERNAL) Add this item as B{C{enum.name}}.

           @note: Don't register if name is empty or doesn't
                  start with a letter.
        '''
        if name and _xvalid(name, _OK=True):
            self.name = name
            if name[:1].isalpha():  # '_...' not registered
                enum.register(self)
                self._enum = enum

    def unregister(self):
        '''Remove this instance from its C{_NamedEnum} registry.

           @raise AssertionError: Mismatch of this and registered item.

           @raise NameError: This item is unregistered.
        '''
        enum = self._enum
        if enum and self.name and self.name in enum:
            item = enum.unregister(self.name)
            if item is not self:
                t = _SPACE_(repr(item), _vs_, repr(self))
                raise _AssertionError(t)


class _NamedTuple(tuple, _Named):
    '''(INTERNAL) Base for named C{tuple}s with both index I{and}
       attribute name access to the items.

       @note: This class is similar to Python's C{namedtuple},
              but statically defined, lighter and limited.
    '''
    _iteration = None  # Iteration number (C{int} or C{None})
    _Names_    = ()  # item names, non-identifier, no leading underscore
    '''Tuple specifying the C{name} of each C{Named-Tuple} item.

       @note: Specify at least 2 item names.
    '''
    _Units_    = ()    # .units classes
    '''Tuple defining the C{units} of the value of each C{Named-Tuple} item.

       @note: The C{len(_Units_)} must match C{len(_Names_)}.
    '''
    _validated = False  # set to True I{per sub-class!}

    def __new__(cls, *args, **name_only):
        '''New L{_NamedTuple} initialized with B{C{positional}} arguments.

           @arg args: Tuple items (C{any}), all positional arguments.
           @kwarg name_only: Only C{B{name}='name'} is used, anu other
                             keyword arguments are I{silently} ignored.

           @raise LenError: Unequal number of positional arguments and
                            number of item C{_Names_} or C{_Units_}.

           @raise TypeError: The C{_Names_} or C{_Units_} attribute is
                             not a C{tuple} of at least 2 items.

           @raise ValueError: Item name is not a C{str} or valid C{identifier}
                              or starts with C{underscore}.
        '''
        self = tuple.__new__(cls, args)
        if not self._validated:
            self._validate()

        n = len(self._Names_)
        if len(args) != n:
            raise LenError(self.__class__, args=len(args), _Names_=n)
        if name_only:  # name=NN
            n = name_only.get(_name_, NN)
            if n:
                self.name = n
        return self

    def __delattr__(self, name):
        '''Delete an attribute by B{C{name}}.

           @note: Items can not be deleted.
        '''
        if name in self._Names_:
            raise _TypeError(_del_, _DOT_(self.classname, name), txt=_immutable_)
        elif name in (_name_, _name):
            _Named.__setattr__(self, name, NN)  # XXX _Named.name.fset(self, NN)
        else:
            tuple.__delattr__(self, name)

    def __getattr__(self, name):
        '''Get the value of an attribute or item by B{C{name}}.
        '''
        try:
            return tuple.__getitem__(self, self._Names_.index(name))
        except IndexError:
            raise _IndexError(_DOT_(self.classname, Fmt.ANGLE(_name_)), name)
        except ValueError:
            return tuple.__getattribute__(self, name)

    def __getitem__(self, item):  # index, slice, etc.
        '''Get the value of an item by B{C{name}}.
        '''
        return tuple.__getitem__(self, item)

    def __repr__(self):
        '''Default C{repr(self)}.
        '''
        return self.toRepr()

    def __setattr__(self, name, value):
        '''Set attribute or item B{C{name}} to B{C{value}}.
        '''
        if name in self._Names_:
            raise _TypeError(_DOT_(self.classname, name), value, txt=_immutable_)
        elif name in (_name_, _name):
            _Named.__setattr__(self, name, value)  # XXX _Named.name.fset(self, value)
        else:
            tuple.__setattr__(self, name, value)

    def __str__(self):
        '''Default C{repr(self)}.
        '''
        return self.toStr()

    def items(self):
        '''Yield the items, each as a C{(name, value)} pair (C{2-tuple}).

           @see: Method C{.units}.
        '''
        for n, v in zip(self._Names_, self):
            yield n, v

    iteritems = items

    @property_RO
    def iteration(self):
        '''Get the iteration number (C{int} or C{None} if not available/applicable).
        '''
        return self._iteration

    def _xtend(self, xTuple, *items):
        '''(INTERNAL) Extend this C{Named-Tuple} with C{items} to an other B{C{xTuple}}.
        '''
        if not (issubclassof(xTuple, _NamedTuple) and
               (len(self._Names_) + len(items)) == len(xTuple._Names_)
                and self._Names_ == xTuple._Names_[:len(self)]):
            c = NN(self.classname,  repr(self._Names_))
            x = NN(xTuple.__name__, repr(xTuple._Names_))
            raise TypeError(_SPACE_(c, _vs_, x))
        return self._xnamed(xTuple(*(self + items)))

    def toRepr(self, prec=6, sep=_COMMASPACE_, **unused):  # PYCHOK signature
        '''Return this C{Named-Tuple} items as C{name=value} string(s).

           @kwarg prec: The C{float} precision, number of decimal digits (0..9).
                        Trailing zero decimals are stripped for B{C{prec}} values
                        of 1 and above, but kept for negative B{C{prec}} values.
           @kwarg sep: Optional separator to join (C{str}).

           @return: Tuple items (C{str}).
        '''
        return Fmt.PAREN(self.named, sep.join(pairs(self.items(), prec=prec)))

    toStr2 = toRepr  # PYCHOK for backward compatibility
    '''DEPRECATED, use method C{toRepr}.'''

    def toStr(self, prec=6, sep=_COMMASPACE_, **unused):  # PYCHOK signature
        '''Return this C{Named-Tuple} items as string(s).

           @kwarg prec: The C{float} precision, number of decimal digits (0..9).
                        Trailing zero decimals are stripped for B{C{prec}} values
                        of 1 and above, but kept for negative B{C{prec}} values.
           @kwarg sep: Optional separator to join (C{str}).

           @return: Tuple items (C{str}).
        '''
        return Fmt.PAREN(sep.join(reprs(self, prec=prec)))

    def toUnits(self, Error=UnitError):  # overloaded in .frechet, .hausdorff
        '''Return a copy of this C{Named-Tuple} with each item value wrapped
           as an instance of its L{units} class.

           @kwarg Error: Error to raise for L{units} issues (C{UnitError}).

           @return: A duplicate of this C{Named-Tuple} (C{C{Named-Tuple}}).

           @raise Error: Invalid C{Named-Tuple} item or L{units} class.
        '''
        t = (v for _, v in self.units(Error=Error))
        return self.classof(*tuple(t))

    def units(self, Error=UnitError):
        '''Yield the items, each as a C{(name, value}) pair (C{2-tuple}) with
           the value wrapped as an instance of its L{units} class.

           @kwarg Error: Error to raise for L{units} issues (C{UnitError}).

           @raise Error: Invalid C{Named-Tuple} item or L{units} class.

           @see: Method C{.items}.
        '''
        for n, v, U in zip(self._Names_, self, self._Units_):
            if not (v is None or U is None
                              or (isclass(U) and
                                  isinstance(v, U) and
                                  hasattr(v, _name_) and
                                  v.name == n)):  # PYCHOK indent
                v = U(v, name=n, Error=Error)
            yield n, v

    iterunits = units

    def _validate(self, _OK=False):  # see .EcefMatrix
        '''(INTERNAL) One-time check of C{_Names_} and C{_Units_}
           for each C{_NamedUnit} I{sub-class separately}.
        '''
        ns = self._Names_
        if not (isinstance(ns, tuple) and len(ns) > 1):  # XXX > 0
            raise _TypeError(_DOT_(self.classname, _Names_), ns)
        for i, n in enumerate(ns):
            if not _xvalid(n, _OK=_OK):
                t = Fmt.SQUARE(_Names_=i)
                raise _ValueError(_DOT_(self.classname, t), n)

        us = self._Units_
        if not isinstance(us, tuple):
            raise _TypeError(_DOT_(self.classname, _Units_), us)
        if len(us) != len(ns):
            raise LenError(self.__class__, _Units_=len(us), _Names_=len(ns))
        for i, u in enumerate(us):
            if not (u is None or callable(u)):
                t = Fmt.SQUARE(_Units_=i)
                raise _TypeError(_DOT_(self.classname, t), u)

        self.__class__._validated = True


def callername(up=1, dflt=NN, source=False):
    '''Get the name of the calling callable.

       @kwarg up: Number of call stack frames up (C{int}).
       @kwarg dflt: Default return value (C{any}).
       @kwarg source: Include source file name and line
                      number (C{bool}).

       @return: Name of the non-internal callable (C{str})
                or B{C{dflt}} if none found.
    '''
    try:  # see .lazily._caller3
        for u in range(up, up + 32):
            n, f, s = _caller3(u)
            if n and (n.startswith(_DUNDER_) or
                  not n.startswith(_UNDER_)):
                if source:
                    n = NN(n, _AT_, f, _COLON_, str(s))
                return n
    except (AttributeError, ValueError):  # PYCHOK no cover
        pass
    return dflt


def _callname(name, class_name, self_name, up=1):  # imported by .points
    '''(INTERNAL) Assemble the name for an invokation.
    '''
    n, c = class_name, callername(up=up + 1)
    if c:
        n = _DOT_(n, Fmt.PAREN(c, name))
    if self_name:
        n = _SPACE_(n, repr(self_name))
    return n


def classname(inst, prefixed=None):
    '''Return the instance' class name optionally prefixed with the
       module name.

       @arg inst: The object (any C{type}).
       @kwarg prefixed: Include the module name (C{bool}), see
                        function C{classnaming}.

       @return: The B{C{inst}}'s C{[module.]class} name (C{str}).
    '''
    if prefixed is None:
        prefixed = getattr(inst, classnaming.__name__, prefixed)
    return modulename(inst.__class__, prefixed=prefixed)


def classnaming(prefixed=None):
    '''Get/set the default class naming for C{[module.]class} names.

       @kwarg prefixed: Include the module name (C{bool}).

       @return: Previous class naming setting (C{bool}).
    '''
    t = _Named._classnaming
    if prefixed in (True, False):
        _Named._classnaming = prefixed
    return t


def modulename(clas, prefixed=None):  # in .basics._xversion
    '''Return the class name optionally prefixed with the
       module name.

       @arg clas: The class (any C{class}).
       @kwarg prefixed: Include the module name (C{bool}), see
                        function C{classnaming}.

       @return: The B{C{class}}'s C{[module.]class} name (C{str}).
    '''
    try:
        n = clas.__name__
    except AttributeError:
        n = _n_a_m_e_
    if prefixed or (classnaming() if prefixed is None else False):
        try:
            m =  clas.__module__.rsplit(_DOT_, 1)
            n = _DOT_.join(m[1:] + [n])
        except AttributeError:
            pass
    return n


def nameof(inst):
    '''Get the name of an instance.

       @arg inst: The object (any C{type}).

       @return: The instance' name (C{str}) or C{""}.
    '''
    return getattr(inst, _name_, NN)


def _notError(inst, name, args, kwds):  # PYCHOK no cover
    '''(INTERNAL) Format an error message.
    '''
    n = _DOT_(classname(inst, prefixed=True), _dunder_name(name, name))
    m = _COMMASPACE_.join(modulename(c, prefixed=True) for c in inst.__class__.__mro__[1:-1])
    return _COMMASPACE_(unstr(n, *args, **kwds), Fmt.PAREN(_MRO_, m))


def notImplemented(inst, name, *args, **kwds):  # PYCHOK no cover
    '''Raise a C{NotImplementedError} for a missing method or property.

       @arg inst: Instance (C{any}).
       @arg name: Method, property or name (C{str} or C{callable}).
       @arg args: Method or property positional arguments (any C{type}s).
       @arg kwds: Method or property keyword arguments (any C{type}s).
    '''
    t = _notError(inst, name, args, kwds)
    raise _NotImplementedError(t, txt=notImplemented.__name__.replace(_I_, ' i'))


def notOverloaded(inst, name, *args, **kwds):  # PYCHOK no cover
    '''Raise an C{AssertionError} for a method or property not overloaded.

       @arg inst: Instance (C{any}).
       @arg name: Method, property or name (C{str} or C{callable}).
       @arg args: Method or property positional arguments (any C{type}s).
       @arg kwds: Method or property keyword arguments (any C{type}s).
    '''
    t = _notError(inst, name, args, kwds)
    raise _AssertionError(t, txt=notOverloaded.__name__.replace(_O_, ' o'))


def _Pass(arg, **unused):  # PYCHOK no cover
    '''(INTERNAL) I{Pass-thru} class for C{_NamedTuple._Units_}.
    '''
    return arg


__all__ += _ALL_DOCS(_Named,
                     _NamedBase,  # _NamedDict,
                     _NamedEnum, _NamedEnumItem,
                     _NamedTuple)

# **) MIT License
#
# Copyright (C) 2016-2021 -- mrJean1 at Gmail -- All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

# % env PYGEODESY_FOR_DOCS=1 python -m pygeodesy.named
# all 71 locals OK
