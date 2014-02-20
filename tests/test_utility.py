import unittest
from unittesthelper import init
init()  # will let you import modules from upper folder
from src.underscore import _
import math
import time


class TestUtility(unittest.TestCase):

    class Namespace():
        pass

    def setUp(self):
        _.templateSettings = {}

    def test_identity(self):
        moe = {"name": 'moe'}
        self.assertEqual(moe, _.identity(moe),
                         "moe is the same as his identity")

    def test_constant(self):
        moe = {"name": 'moe'}
        self.assertEqual(_.constant(moe)(), moe,
                         'should create a function that returns moe')

    def test_property(self):
        moe = {"name": 'moe'}
        self.assertEqual(_.property('name')(moe), 'moe',
                         'should return the property with the given name')

    def test_random(self):
        array = _.range(1000)
        mi = math.pow(2, 31)
        ma = math.pow(2, 62)

        def check(*args):
            return _.random(mi, ma) >= mi
        result = _.every(array, check)
        self.assertTrue(
            result, "should produce a random number greater than or equal"
            " to the minimum number")

        def check2(*args):
            r = _.random(ma)
            return r >= 0 and r <= ma
        result = _.every(array, check2)
        self.assertTrue(
            result, "should produce a random number when passed max_number")

    def test_now(self):
        diff = _.now() - time.time()
        self.assertTrue(diff <= 0 and diff > -5,
                        'Produces the correct time in milliseconds')

    def test_uniqueId(self):
        ns = self.Namespace()
        ns.ids = []
        i = 0
        for i in range(0, 100):
            ns.ids.append(_.uniqueId())

        self.assertEqual(len(ns.ids), len(_.uniq(ns.ids)),
                         "can generate a globally-unique stream of ids")

    def test_times(self):
        vals = []
        _.times(3, lambda i: vals.append(i))
        self.assertEqual([0, 1, 2], vals, "is 0 indexed")
        vals = []
        _(3).times(lambda i: vals.append(i))
        self.assertEqual([0, 1, 2], vals, "is 0 indexed")
        pass

    def test_mixin(self):
        _.mixin({
            "myUpper": lambda self: self.obj.upper(),
        })
        self.assertEqual('TEST', _.myUpper('test'), "mixed in a function to _")
        self.assertEqual('TEST', _('test').myUpper(),
                         "mixed in a function to _ OOP")

    def test_escape(self):
        self.assertEqual("Curly &amp; Moe", _.escape("Curly & Moe"))
        self.assertEqual("Curly &amp;amp; Moe", _.escape("Curly &amp; Moe"))

    def test_template(self):
        basicTemplate = _.template("<%= thing %> is gettin' on my noives!")
        result = basicTemplate({"thing": 'This'})
        self.assertEqual(result, "This is gettin' on my noives!",
                         'can do basic attribute interpolation')

        sansSemicolonTemplate = _.template("A <% this %> B")
        self.assertEqual(sansSemicolonTemplate(), "A  B")

        backslashTemplate = _.template("<%= thing %> is \ridanculous")
        self.assertEqual(
            backslashTemplate({"thing": 'This'}), "This is \ridanculous")

        escapeTemplate = _.template(
            '<%= "checked=\\"checked\\"" if a else "" %>')
        self.assertEqual(escapeTemplate({"a": True}), 'checked="checked"',
                         'can handle slash escapes in interpolations.')

        fancyTemplate = _.template(
            "<ul><% for key in people: %><li><%= key %></li><% endfor %></ul>")
        result = fancyTemplate({"people": ["Larry", "Curly", "Moe"]})
        self.assertEqual(
            result, "<ul><li>Larry</li><li>Curly</li><li>Moe</li></ul>",
            'can run arbitrary javascript in templates')

        escapedCharsInJavascriptTemplate = _.template(
            "<ul><% def by(item, *args): %><li><%= item %></li><% enddef %>"
            "<% _.each(numbers.split('\\n'), by) %></ul>")
        # print escapedCharsInJavascriptTemplate.source
        result = escapedCharsInJavascriptTemplate(
            {"numbers": "one\ntwo\nthree\nfour"})
        # print result, "####"
        self.assertEqual(
            result, "<ul><li>one</li><li>two</li>"
            "<li>three</li><li>four</li></ul>",
            'Can use escaped characters (e.g. \\n) in Javascript')

        namespaceCollisionTemplate = _.template(
            "<%= pageCount %> <%= thumbnails[pageCount] %>"
            " <% def by(p, *args): %><div class=\"thumbnail\""
            " rel=\"<%= p %>\"></div><% enddef %><% _.each(thumbnails, by) %>")
        result = namespaceCollisionTemplate({
            "pageCount": 3,
            "thumbnails": {
                1: "p1-thumbnail.gif",
                2: "p2-thumbnail.gif",
                3: "p3-thumbnail.gif"
            }
        })

        self.assertEqual(
            result, '3 p3-thumbnail.gif <div class="thumbnail"'
            ' rel="p1-thumbnail.gif"></div><div class="thumbnail"'
            ' rel="p2-thumbnail.gif"></div><div class="thumbnail"'
            ' rel="p3-thumbnail.gif"></div>')

        noInterpolateTemplate = _.template(
            "<div><p>Just some text. Hey, I know this is silly"
            " but it aids consistency.</p></div>")
        result = noInterpolateTemplate()
        self.assertEqual(
            result, "<div><p>Just some text. Hey, I know this is"
            " silly but it aids consistency.</p></div>")

        quoteTemplate = _.template("It's its, not it's")
        self.assertEqual(quoteTemplate({}), "It's its, not it's")

        quoteInStatementAndBody = _.template("<% \
           if foo == 'bar': \
        %>Statement quotes and 'quotes'.<% endif %>")
        self.assertEqual(
            quoteInStatementAndBody({"foo": "bar"}),
            "Statement quotes and 'quotes'.")

        withNewlinesAndTabs = _.template(
            'This\n\t\tis: <%= x %>.\n\tok.\nend.')
        self.assertEqual(
            withNewlinesAndTabs({"x": 'that'}),
            'This\n\t\tis: that.\n\tok.\nend.')

        template = _.template("<i><%- value %></i>")
        result = template({"value": "<script>"})
        self.assertEqual(result, '<i>&lt;script&gt;</i>')

        # This wouldn't work in python
        # stooge = {
        #    "name": "Moe",
        #    "template": _.template("I'm <%= this.name %>")
        # }
        # self.assertEqual(stooge.template(), "I'm Moe")

        _.templateSettings = {
            "evaluate": r"\{\{([\s\S]+?)\}\}",
            "interpolate": r"\{\{=([\s\S]+?)\}\}"
        }

        custom = _.template(
            "<ul>{{ for key in people: }}<li>{{= key }}</li>{{ endfor }}</ul>")
        result = custom({"people": ["Larry", "Curly", "Moe"]})
        self.assertEqual(
            result, "<ul><li>Larry</li><li>Curly</li><li>Moe</li></ul>",
            'can run arbitrary javascript in templates')

        customQuote = _.template("It's its, not it's")
        self.assertEqual(customQuote({}), "It's its, not it's")

        quoteInStatementAndBody = _.template(
            "{{ if foo == 'bar': }}Statement quotes and 'quotes'.{{ endif }}")
        self.assertEqual(
            quoteInStatementAndBody({"foo": "bar"}),
            "Statement quotes and 'quotes'.")

        _.templateSettings = {
            "evaluate": r"<\?([\s\S]+?)\?>",
            "interpolate": r"<\?=([\s\S]+?)\?>"
        }

        customWithSpecialChars = _.template(
            "<ul><? for key in people: ?><li><?= key ?></li><? endfor ?></ul>")
        result = customWithSpecialChars({"people": ["Larry", "Curly", "Moe"]})
        self.assertEqual(
            result, "<ul><li>Larry</li><li>Curly</li><li>Moe</li></ul>",
            'can run arbitrary javascript in templates')

        customWithSpecialCharsQuote = _.template("It's its, not it's")
        self.assertEqual(customWithSpecialCharsQuote({}), "It's its, not it's")

        quoteInStatementAndBody = _.template(
            "<? if foo == 'bar': ?>Statement quotes and 'quotes'.<? endif ?>")
        self.assertEqual(
            quoteInStatementAndBody({"foo": "bar"}),
            "Statement quotes and 'quotes'.")

        _.templateSettings = {
            "interpolate": r"\{\{(.+?)\}\}"
        }

        mustache = _.template("Hello {{planet}}!")
        self.assertEqual(mustache({"planet": "World"}),
                         "Hello World!", "can mimic mustache.js")

        templateWithNull = _.template("a null undefined {{planet}}")
        self.assertEqual(
            templateWithNull({"planet": "world"}), "a null undefined world",
            "can handle missing escape and evaluate settings")

    def test_template_escape(self):
        tmpl = _.template('<p>\u2028<%= "\\u2028\\u2029" %>\u2029</p>')
        self.assertEqual(tmpl(), '<p>\u2028\u2028\u2029\u2029</p>')

    def test_result(self):
        obj = {"w": '', "x": 'x', "y": lambda x="x": x}
        self.assertEqual(_.result(obj, 'w'), '')
        self.assertEqual(_.result(obj, 'x'), 'x')
        self.assertEqual(_.result(obj, 'y'), 'x')
        self.assertEqual(_.result(obj, 'z'), None)
        self.assertEqual(_.result(None, 'x'), None)

    def test_template_variable(self):
        s = '<%=data["x"]%>'
        data = {"x": 'x'}
        self.assertEqual(_.template(s, data, {"variable": 'data'}), 'x')
        _.templateSettings = {
            "variable": 'data'
        }
        self.assertEqual(_.template(s)(data), 'x')

    def test_temp_settings_no_change(self):
        self.assertFalse("variable" in _.templateSettings)
        _.template('', {}, {"variable": 'x'})
        self.assertFalse("variable" in _.templateSettings)

    def test_template_undef(self):
        template = _.template('<%=x%>')
        self.assertEqual(template({"x": None}), '')

        templateEscaped = _.template('<%-x%>')
        self.assertEqual(templateEscaped({"x": None}), '')

        templateWithPropertyEscaped = _.template('<%-x["foo"]%>')
        self.assertEqual(templateWithPropertyEscaped({"x": {"foo": None}}), '')

    def test_interpolate_only_once(self):
        ns = self.Namespace()
        ns.count = 0
        template = _.template('<%= f() %>')

        def test():
            self.assertTrue(not ns.count)
            ns.count += 1

        template({"f": test})

        ns.countEscaped = 0
        templateEscaped = _.template('<%- f() %>')

        def test2():
            self.assertTrue(not ns.countEscaped)
            ns.countEscaped += 1

        templateEscaped({"f": test2})

if __name__ == "__main__":
    print("run these tests by executing `python -m unittest"
          " discover` in unittests folder")
    unittest.main()
