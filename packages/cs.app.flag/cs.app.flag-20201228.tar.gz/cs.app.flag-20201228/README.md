Persistent filesystem based flags for state and control.

*Latest release 20201228*:
Import fix.

Filesystem visible boolean flags
for control and status,
allowing easy monitoring of services or other status,
and control by flag management
for programmes which also monitor the flags.

The flags are expressed as individual files with uppercase names
in a common directory ($HOME/var/flags by default);
an empty or missing file is "false"
and a nonempty file is "true".

The Flags class provides easy Pythonic access to this directory.
It presents as a modifiable mapping whose keys are the flag names:

      flags = Flags()
      flags['UNTOPPOST'] = True

There is also a FlaggedMixin class providing convenient methods and attributes
for maintaining a collection of flags associated with some object
with flag names prefixed by the object's .name attribute
uppercased and with an underscore appended:

      class SvcD(...,FlaggedMixin):
        def __init__(self, name, ...)
          self.name = name
          FlaggedMixin.__init__(self)
          ...
        def disable(self):
          self.flag_disable = True
        def restart(self):
          self.flag_restart = True
        def _restart(self):
          self.flag_restart = False
          ... restart the SvcD ...

so that an object set up as:

      svcd = SvcD("portfwd")
      print(svcd.flag_disable)

accesses the flag named "PORTFWD_DISABLE".

## Function `DummyFlags()`

factory to make a dummy flagslike object without persistent storage

## Class `FlaggedMixin`

A mixin class adding flag_* and flagname_* attributes.

 This defines the following attributes on instances:
 * `flags`: the `Flags` instance providing the flag values.
 * `flags_prefix`: the prefix for the flags of interest.
 * `flagname_`*name*: the full name within `.flags`
   of the flag referred to as *name*.
   This is `.flags_prefix + '_' + `*name*
   if `.flags_prefix` is not empty,
   or just *name* otherwise.
* `flag_`*name*: the value from `.flags`
   of the flag referred to as *name*.
   This is a setable attribute
   with changes propagated to `.flags`.

### Method `FlaggedMixin.__init__(self, flags=None, debug=None, prefix=None)`

Initialise the mixin.

Parameters:
* `flags`: optional parameter;
  if `None` defaults to a new default `Flags()`.
* `prefix`: optional prefix;
  if not provided the prefix is derived
  from the object's `.name` attribute,
  or is empty if there is no `.name`

### Method `FlaggedMixin.__getattr__(self, attr)`

Support .flag_suffix and .flagname_suffix.

### Method `FlaggedMixin.__setattr__(self, attr, value)`

Support .flag_suffix=value.

## Class `Flags(collections.abc.MutableMapping,collections.abc.Mapping,collections.abc.Collection,collections.abc.Sized,collections.abc.Iterable,collections.abc.Container,FlaggedMixin)`

A mapping which directly inspects the flags directory.

### Method `Flags.__init__(self, flagdir=None, environ=None, lock=None, debug=None)`

Initialise the `Flags` instance.

Parameters:
* `flagdir`: the directory holding flag state files;
  if omitted use the value from `cs.env.FLAGDIR(environ)`
* `environ`: the environment mapping to use,
  default `os.environ`
* `lock`: a `Lock`like mutex to control multithreaded access;
  if omitted no locking is down
* `debug`: debug mode, default `False`

### Method `Flags.__getitem__(self, k)`

Return the truthiness of this flag.
True means a non-empty file exists.

### Method `Flags.__iter__(self)`

Iterator returning the flag names in the directory.

### Method `Flags.__len__(self)`

Return the number of flag files.

### Method `Flags.__setitem__(self, k, value)`

Set the flag value.

        If true, write `"1
"` to the flag file.
        If false, truncate the flag file.

### Method `Flags.init(self)`

Ensure the flag directory exists.

### Method `Flags.update_prefix(self, prefix, updates, omitted_value=False)`

Update all flag values commencing with `prefix`,
falsifying any unmentioned flags.

Parameters:
* `prefix`: common prefix for updated flags.
* `updates`: iterable of `(flagname,flagvalue)`.
* `omitted_value`: value to be assigned to any unmentioned flags,
  default `False`.
  Set this to `None` to leave unmentioned flags alone.

## Function `lowername(s)`

Lowercase letters, transmute '_' to '-'. Note: NOT the reverse of uppername.

## Function `main(argv=None)`

Main program: inspect or modify flags.

## Function `main_flagset(argv=None, stdin=None)`

Main program for "flagset" command.

## Class `PolledFlags(builtins.dict)`

A mapping which maintains a dict of the current state of the flags directory
and updates it regularly.

This allows an application to consult the flags very frequently
without hammering the filesystem.

## Function `truthy(value)`

Decide whether a value is considered true.

Strings are converted to:
* `'0'`: `False`
* `'1'`: `True`
* `'true'`: `True` (case insensitive)
* `'false'`: `False` (case insensitive)
* other string values are unchanged.

Other types are converted with `bool()`.

## Function `uppername(s)`

Uppercase letters, transmute some characters to '_' or '__'.

# Release Log



*Release 20201228*:
Import fix.

*Release 20190729*:
Python 2 backport for super call. Other minor changes.

*Release 20190220*:
FlaggedMixin: make .flags_prefix public; document mixin attributes.

*Release 20181109*:
Assorted minor updates.

*Release 20170906.2*:
tweak docstring

*Release 20170906.1*:
Improve module docstring.

*Release 20170906*:
Fill out module docstring.

*Release 20170905*:
Initial PyPI release.
