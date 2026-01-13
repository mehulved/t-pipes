import unittest
from tpipes.processors import JsonParser, XmlParser, HtmlSelector, Filter

class TestBlocks(unittest.TestCase):
    
    def test_json_parser(self):
        block = JsonParser()
        data = '{"key": "value", "list": [1, 2, 3]}'
        result = block.process(data, None)
        self.assertIsInstance(result, dict)
        self.assertEqual(result['key'], 'value')
        self.assertEqual(len(result['list']), 3)

    def test_xml_parser(self):
        block = XmlParser()
        data = """<root><item id="1">Text</item></root>"""
        result = block.process(data, None)
        self.assertIn('root', result)
        self.assertEqual(result['root']['item']['#text'], 'Text')
        self.assertEqual(result['root']['item']['@id'], '1')

    def test_html_selector(self):
        block = HtmlSelector({'selector': 'div.target > p'})
        data = """
        <html>
            <body>
                <div class="target">
                    <p>Match 1</p>
                    <p>Match 2</p>
                </div>
                <div class="other">
                    <p>No Match</p>
                </div>
            </body>
        </html>
        """
        result = block.process(data, None)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], 'Match 1')
        self.assertEqual(result[1], 'Match 2')

    def test_filter_eq(self):
        block = Filter({'key': 'status', 'value': 'active', 'op': 'eq'})
        data = [
            {'id': 1, 'status': 'active'},
            {'id': 2, 'status': 'inactive'},
            {'id': 3, 'status': 'active'}
        ]
        result = block.process(data, None)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['id'], 1)
        self.assertEqual(result[1]['id'], 3)

    def test_filter_contains(self):
        block = Filter({'key': 'title', 'value': 'pipes', 'op': 'contains'})
        data = [
            {'title': 'T-Pipes are cool'},
            {'title': 'Yahoo Pipes was old'},
            {'title': 'Something else'}
        ]
        result = block.process(data, None)
        self.assertEqual(len(result), 2)

if __name__ == '__main__':
    unittest.main()
