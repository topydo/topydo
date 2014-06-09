import re
import unittest

import TodoBase

class TodoBaseTester(unittest.TestCase):
    def test_parse_tag(self):
        todo = TodoBase.TodoBase("(C) Test foo:bar foo:baz foo_:baz_ blah:zah:haz")

        self.assertTrue(todo.has_tag('foo'))
        self.assertTrue(todo.has_tag('foo_'))
        self.assertTrue(todo.has_tag('foo', 'bar'))
        self.assertTrue(todo.has_tag('foo', 'baz'))
        self.assertTrue(todo.has_tag('blah'))
        self.assertTrue(todo.has_tag('blah', 'zah:haz'))

    def test_add_tag(self):
        todo = TodoBase.TodoBase("(C) Foo")
        todo.set_tag('foo', 'bar')

        self.assertTrue(todo.has_tag('foo'))
        self.assertTrue(todo.has_tag('foo', 'bar'))
        self.assertFalse(todo.has_tag('foo', 'baz'))
        self.assertFalse(todo.has_tag('bar'))
        self.assertTrue(re.search(r'\bfoo:bar\b', todo.src))

    def test_set_tag(self):
        todo = TodoBase.TodoBase("(C) Foo foo:bar")
        todo.set_tag('foo', 'baz')

        self.assertTrue(todo.has_tag('foo'))
        self.assertTrue(todo.has_tag('foo', 'baz'))
        self.assertFalse(todo.has_tag('foo', 'bar'))

        self.assertTrue(re.search(r'\bfoo:baz\b', todo.src))
        self.assertFalse(re.search(r'\bfoo:bar\b', todo.src))

    def test_set_tag_empty_value(self):
        todo = TodoBase.TodoBase("(C) Foo foo:bar foo:baz")
        todo.set_tag('foo')

        self.assertFalse(todo.has_tag('foo'))
        self.assertFalse(re.search(r'\bfoo:', todo.src))

    def test_remove_all(self):
        todo = TodoBase.TodoBase("(C) Foo foo:bar foo:baz foo:")
        todo.remove_tag('foo')

        self.assertFalse(todo.has_tag('foo'))
        self.assertFalse(re.search(r'\bfoo:(bar|baz)\b', todo.src))
        self.assertTrue(re.search(r'foo:', todo.src))

    def test_remove_specific_tag_value(self):
        todo = TodoBase.TodoBase("(C) Foo kungfoo:bar foo:bar foo:barz")
        todo.remove_tag('foo', 'bar')

        self.assertTrue(todo.has_tag('foo'))
        self.assertTrue(todo.has_tag('kungfoo', 'bar'))
        self.assertTrue(todo.has_tag('foo', 'barz'))
        self.assertFalse(todo.has_tag('foo', 'bar'))

        self.assertTrue(re.search(r'\bkungfoo:bar\b', todo.src))
        self.assertTrue(re.search(r'\bfoo:barz\b', todo.src))
        self.assertFalse(re.search(r'\bfoo:bar\b', todo.src))

    def test_set_priority1(self):
        todo = TodoBase.TodoBase("(A) Foo")
        todo.set_priority('B')

        self.assertEquals(todo.priority(), 'B')
        self.assertTrue(re.match(r'^\(B\) Foo$', todo.src))

    def test_set_priority2(self):
        todo = TodoBase.TodoBase("Foo")
        todo.set_priority('B')

        self.assertEquals(todo.priority(), 'B')
        self.assertTrue(re.match(r'^\(B\) Foo$', todo.src))

    def test_set_priority3(self):
        todo = TodoBase.TodoBase("(A) Foo")
        todo.set_priority('AB')

        self.assertEquals(todo.priority(), 'A')
        self.assertTrue(re.match(r'^\(A\) Foo$', todo.src))

    def test_set_priority4(self):
        todo = TodoBase.TodoBase("(A)Foo")

        self.assertNotEqual(todo.priority(), 'A')

        todo.set_priority('B')

        self.assertEquals(todo.priority(), 'B')
        self.assertTrue(re.match(r'^\(B\) \(A\)Foo$', todo.src))

    def test_set_priority5(self):
        todo = TodoBase.TodoBase("(A) Foo")
        todo.set_priority(None)

        self.assertEquals( todo.priority(), None )
        self.assertTrue(re.match(r'^Foo$', todo.src))

if __name__ == '__main__':
    unittest.main()
