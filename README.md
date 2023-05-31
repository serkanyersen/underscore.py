                       __
                      /\ \
     __  __    ___    \_\ \     __   _ __   ____    ___    ___   _ __    __      _____   __  __
    /\ \/\ \ /' _ `\  /'_` \  /'__`\/\`'__\/',__\  /'___\ / __`\/\`'__\/'__`\   /\ '__`\/\ \/\ \
    \ \ \_\ \/\ \/\ \/\ \_\ \/\  __/\ \ \//\__, `\/\ \__//\ \_\ \ \ \//\  __/  _\ \ \_\ \ \ \_\ \
     \ \____/\ \_\ \_\ \___,_\ \____\\ \_\\/\____/\ \____\ \____/\ \_\\ \____\/\_\ \ ,__/\/`____ \
      \/___/  \/_/\/_/\/__,_ /\/____/ \/_/ \/___/  \/____/\/___/  \/_/ \/____/\/_/\ \ \/  `/___/> \
                                                                                   \ \_\     /\___/
                                                                                    \/_/     \/__/
                                                                                    
This is an update for python3 of: github.com/serkanyersen/underscore3.py.git


---


Underscore.py is a python port of excellent javascript library underscore3.js

**What is underscore3.js?**

    From underscore3 page: Underscore.js is a utility-belt library for JavaScript that provides support for the
    usual functional suspects (each, map, reduce, filter...) without extending any core JavaScript objects.

NOTE: It's obvious that python already has nearly all features of underscore3 library built-in. I'm not trying to fill any gap in python. If you are coming from JavaScript this library will provide you a familiar interface, a set of tools you already know how to use and micro templating functionality. Use it wisely and try to use built-in functions wherever possible.

## Installing

Install from pypi
```bash
pip install underscore3.py
```
**or**

Clone the repository:
```bash
git clone git://github.com/serkanyersen/underscore3.py.git
```
Get into underscore3.py directory
```bash
cd underscore3.py
```
Run setup script
```bash
sudo python setup.py install
```
That's it

## Usage
Import underscore3 to your project
```python
from underscore3 import _
```
or if you don't want to mess with _ variable
```python
from underscore3 import _ as us  # You can use any name you want, __ or u
```

## Use it just like javascript version
```python
# Dynamically
_(["foo", "bar"]).invoke("upper")  # ["FOO", "BAR"]
# or statically
_.filter(["foo", "hello", "bar", "world"], lambda x, *a: len(x) > 3)  # ["hello", "world"]
# Do chaining
_([10, 48, 56, 30, 20]).chain().filter(lambda x, *a: x > 20).map(lambda x, *a: x * 2).sortBy().value()
# [60, 96, 112]
```

## Full micro templating support
```python
tmpl = _.template("Name: <% if prefix: %><%= prefix %>. <% endif %><%= name %>\n\
Last Name: <%=lname.upper() %>\n\
<% if email: %>\
E-mail: <%= email %>\n\
<% endif %>")

people = [{
  "prefix": "",
  "name": "John",
  "lname": "Doe",
  "email": "johndoe@example.com"
},{
  "prefix": "Mr",
  "name": "James",
  "lname": "Brown",
  "email": "james@brown.net"
}]

for person in people:
  print tmpl(person)
```
Output

    Name: John
    Last Name: DOE
    E-mail: johndoe@example.com
    Name: Mr. James
    Last Name: BROWN
    E-mail: james@brown.net

For more information and documentation [underscore3js.org](http://underscore3js.org)

Original Source: [Underscore.js on Github](https://github.com/documentcloud/underscore3)

### Disclaimer
Please keep in mind that this is a direct port of a javascript library, so don't get started with
the "but it's not pythonic" stuff. This library has no intentions to be pythonic, infact it tries to
bring the same underscore3 experience from javascript to python
