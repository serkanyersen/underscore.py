import unittest
from unittesthelper import init
init()  # will let you import modules from upper folder
from src.underscore import _


class TestUtility(unittest.TestCase):

    class Namespace():
        pass

    def test_identity(self):
        moe = {"name": 'moe'}
        self.assertEqual(moe, _.identity(moe), "moe is the same as his identity")

    def test_uniqueId(self):
        ns = self.Namespace()
        ns.ids = []
        i = 0
        for i in range(0, 100):
            ns.ids.append(_.uniqueId())

        self.assertEqual(len(ns.ids), len(_.uniq(ns.ids)), "can generate a globally-unique stream of ids")

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
        self.assertEqual('TEST', _('test').myUpper(), "mixed in a function to _ OOP")

    def test_escape(self):
        self.assertEqual("Curly &amp; Moe", _.escape("Curly & Moe"))
        self.assertEqual("Curly &amp;amp; Moe", _.escape("Curly &amp; Moe"))

    def test_template(self):
        #   var basicTemplate = _.template("<%= thing %> is gettin' on my noives!");
        #   var result = basicTemplate({thing : 'This'});
        #   equal(result, "This is gettin' on my noives!", 'can do basic attribute interpolation');

        #   var sansSemicolonTemplate = _.template("A <% this %> B");
        #   equal(sansSemicolonTemplate(), "A  B");

        #   var backslashTemplate = _.template("<%= thing %> is \\ridanculous");
        #   equal(backslashTemplate({thing: 'This'}), "This is \\ridanculous");

        #   var escapeTemplate = _.template('<%= a ? "checked=\\"checked\\"" : "" %>');
        #   equal(escapeTemplate({a: true}), 'checked="checked"', 'can handle slash escapes in interpolations.');

        #   var fancyTemplate = _.template("<ul><% \
        #     for (key in people) { \
        #   %><li><%= people[key] %></li><% } %></ul>");
        #   result = fancyTemplate({people : {moe : "Moe", larry : "Larry", curly : "Curly"}});
        #   equal(result, "<ul><li>Moe</li><li>Larry</li><li>Curly</li></ul>", 'can run arbitrary javascript in templates');

        #   var escapedCharsInJavascriptTemplate = _.template("<ul><% _.each(numbers.split('\\n'), function(item) { %><li><%= item %></li><% }) %></ul>");
        #   result = escapedCharsInJavascriptTemplate({numbers: "one\ntwo\nthree\nfour"});
        #   equal(result, "<ul><li>one</li><li>two</li><li>three</li><li>four</li></ul>", 'Can use escaped characters (e.g. \\n) in Javascript');

        #   var namespaceCollisionTemplate = _.template("<%= pageCount %> <%= thumbnails[pageCount] %> <% _.each(thumbnails, function(p) { %><div class=\"thumbnail\" rel=\"<%= p %>\"></div><% }); %>");
        #   result = namespaceCollisionTemplate({
        #     pageCount: 3,
        #     thumbnails: {
        #       1: "p1-thumbnail.gif",
        #       2: "p2-thumbnail.gif",
        #       3: "p3-thumbnail.gif"
        #     }
        #   });
        #   equal(result, "3 p3-thumbnail.gif <div class=\"thumbnail\" rel=\"p1-thumbnail.gif\"></div><div class=\"thumbnail\" rel=\"p2-thumbnail.gif\"></div><div class=\"thumbnail\" rel=\"p3-thumbnail.gif\"></div>");

        #   var noInterpolateTemplate = _.template("<div><p>Just some text. Hey, I know this is silly but it aids consistency.</p></div>");
        #   result = noInterpolateTemplate();
        #   equal(result, "<div><p>Just some text. Hey, I know this is silly but it aids consistency.</p></div>");

        #   var quoteTemplate = _.template("It's its, not it's");
        #   equal(quoteTemplate({}), "It's its, not it's");

        #   var quoteInStatementAndBody = _.template("<%\
        #     if(foo == 'bar'){ \
        #   %>Statement quotes and 'quotes'.<% } %>");
        #   equal(quoteInStatementAndBody({foo: "bar"}), "Statement quotes and 'quotes'.");

        #   var withNewlinesAndTabs = _.template('This\n\t\tis: <%= x %>.\n\tok.\nend.');
        #   equal(withNewlinesAndTabs({x: 'that'}), 'This\n\t\tis: that.\n\tok.\nend.');

        #   var template = _.template("<i><%- value %></i>");
        #   var result = template({value: "<script>"});
        #   equal(result, '<i>&lt;script&gt;</i>');

        #   var stooge = {
        #     name: "Moe",
        #     template: _.template("I'm <%= this.name %>")
        #   };
        #   equal(stooge.template(), "I'm Moe");

        #   if (!$.browser.msie) {
        #     var fromHTML = _.template($('#template').html());
        #     equal(fromHTML({data : 12345}).replace(/\s/g, ''), '<li>24690</li>');
        #   }

        #   _.templateSettings = {
        #     evaluate    : /\{\{([\s\S]+?)\}\}/g,
        #     interpolate : /\{\{=([\s\S]+?)\}\}/g
        #   };

        #   var custom = _.template("<ul>{{ for (key in people) { }}<li>{{= people[key] }}</li>{{ } }}</ul>");
        #   result = custom({people : {moe : "Moe", larry : "Larry", curly : "Curly"}});
        #   equal(result, "<ul><li>Moe</li><li>Larry</li><li>Curly</li></ul>", 'can run arbitrary javascript in templates');

        #   var customQuote = _.template("It's its, not it's");
        #   equal(customQuote({}), "It's its, not it's");

        #   var quoteInStatementAndBody = _.template("{{ if(foo == 'bar'){ }}Statement quotes and 'quotes'.{{ } }}");
        #   equal(quoteInStatementAndBody({foo: "bar"}), "Statement quotes and 'quotes'.");

        #   _.templateSettings = {
        #     evaluate    : /<\?([\s\S]+?)\?>/g,
        #     interpolate : /<\?=([\s\S]+?)\?>/g
        #   };

        #   var customWithSpecialChars = _.template("<ul><? for (key in people) { ?><li><?= people[key] ?></li><? } ?></ul>");
        #   result = customWithSpecialChars({people : {moe : "Moe", larry : "Larry", curly : "Curly"}});
        #   equal(result, "<ul><li>Moe</li><li>Larry</li><li>Curly</li></ul>", 'can run arbitrary javascript in templates');

        #   var customWithSpecialCharsQuote = _.template("It's its, not it's");
        #   equal(customWithSpecialCharsQuote({}), "It's its, not it's");

        #   var quoteInStatementAndBody = _.template("<? if(foo == 'bar'){ ?>Statement quotes and 'quotes'.<? } ?>");
        #   equal(quoteInStatementAndBody({foo: "bar"}), "Statement quotes and 'quotes'.");

        #   _.templateSettings = {
        #     interpolate : /\{\{(.+?)\}\}/g
        #   };

        #   var mustache = _.template("Hello {{planet}}!");
        #   equal(mustache({planet : "World"}), "Hello World!", "can mimic mustache.js");

        #   var templateWithNull = _.template("a null undefined {{planet}}");
        #   equal(templateWithNull({planet : "world"}), "a null undefined world", "can handle missing escape and evaluate settings");
        # });

        # test('_.template handles \\u2028 & \\u2029', function() {
        #   var tmpl = _.template('<p>\u2028<%= "\\u2028\\u2029" %>\u2029</p>');
        #   strictEqual(tmpl(), '<p>\u2028\u2028\u2029\u2029</p>');
        # });

        # test('result calls functions and returns primitives', function() {
        #   var obj = {w: '', x: 'x', y: function(){ return this.x; }};
        #   strictEqual(_.result(obj, 'w'), '');
        #   strictEqual(_.result(obj, 'x'), 'x');
        #   strictEqual(_.result(obj, 'y'), 'x');
        #   strictEqual(_.result(obj, 'z'), undefined);
        #   strictEqual(_.result(null, 'x'), null);
        # });

        # test('_.templateSettings.variable', function() {
        #   var s = '<%=data.x%>';
        #   var data = {x: 'x'};
        #   strictEqual(_.template(s, data, {variable: 'data'}), 'x');
        #   _.templateSettings.variable = 'data';
        #   strictEqual(_.template(s)(data), 'x');
        # });

        # test('#547 - _.templateSettings is unchanged by custom settings.', function() {
        #   ok(!_.templateSettings.variable);
        #   _.template('', {}, {variable: 'x'});
        #   ok(!_.templateSettings.variable);
        # });

        # test('#556 - undefined template variables.', function() {
        #   var template = _.template('<%=x%>');
        #   strictEqual(template({x: null}), '');
        #   strictEqual(template({x: undefined}), '');

        #   var templateEscaped = _.template('<%-x%>');
        #   strictEqual(templateEscaped({x: null}), '');
        #   strictEqual(templateEscaped({x: undefined}), '');

        #   var templateWithProperty = _.template('<%=x.foo%>');
        #   strictEqual(templateWithProperty({x: {} }), '');
        #   strictEqual(templateWithProperty({x: {} }), '');

        #   var templateWithPropertyEscaped = _.template('<%-x.foo%>');
        #   strictEqual(templateWithPropertyEscaped({x: {} }), '');
        #   strictEqual(templateWithPropertyEscaped({x: {} }), '');
        # });

        # test('interpolate evaluates code only once.', 2, function() {
        #   var count = 0;
        #   var template = _.template('<%= f() %>');
        #   template({f: function(){ ok(!(count++)); }});

        #   var countEscaped = 0;
        #   var templateEscaped = _.template('<%- f() %>');
        #   templateEscaped({f: function(){ ok(!(countEscaped++)); }});
        # });
        pass
