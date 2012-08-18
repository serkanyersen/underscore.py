                       __
                      /\ \
     __  __    ___    \_\ \     __   _ __   ____    ___    ___   _ __    __      _____   __  __
    /\ \/\ \ /' _ `\  /'_` \  /'__`\/\`'__\/',__\  /'___\ / __`\/\`'__\/'__`\   /\ '__`\/\ \/\ \
    \ \ \_\ \/\ \/\ \/\ \_\ \/\  __/\ \ \//\__, `\/\ \__//\ \_\ \ \ \//\  __/  _\ \ \_\ \ \ \_\ \
     \ \____/\ \_\ \_\ \___,_\ \____\\ \_\\/\____/\ \____\ \____/\ \_\\ \____\/\_\ \ ,__/\/`____ \
      \/___/  \/_/\/_/\/__,_ /\/____/ \/_/ \/___/  \/____/\/___/  \/_/ \/____/\/_/\ \ \/  `/___/> \
                                                                                   \ \_\     /\___/
                                                                                    \/_/     \/__/

Underscore.py is a python port of excellent javascript library underscore.js

**From underscore page:**

    Underscore.js is a utility-belt library for JavaScript that provides support for the usual functional
    suspects (each, map, reduce, filter...) without extending any core JavaScript objects.

## Installing
Clone this repository:
```bash
git clone git://github.com/serkanyersen/underscore.py.git
```
Get into underscore.py directory
```bash
cd underscore.py
```
Run setup script
```bash
sudo python setup.py install
```
That's it

## Usage
Import underscore to your project
```python
 from underscore import _
```
Use it just like javascript version
```python
 # Dynamically
 _(["foo", "bar"]).invoke("upper")  # ["FOO", "BAR"]
 # or statically
 _.filter(["foo", "hello", "bar", "world"], lambda x, *args: len(x) > 3)  # ["hello", "world"]
 # Do chaining
 _([10, 48, 56, 30, 20]).chain().filter(lambda x, *args: x > 20).map(lambda x, *args: x * 2).sortBy().value()
 # [60, 96, 112]
```

For more information [underscorejs.org](http://underscorejs.org)

Source: [Underscore.js on Github](https://github.com/documentcloud/underscore)