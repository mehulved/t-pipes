import unittest
from tpipes.processors import JsonParser, XmlParser, HtmlSelector, Filter, Export
from tpipes.sources import CsvSource
import os
import csv
import json
import shutil


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

    def test_csv_source(self):
        # Create dummy csv
        os.makedirs('data_test', exist_ok=True)
        path = 'data_test/test.csv'
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'val'])
            writer.writerow(['1', 'a'])
            writer.writerow(['2', 'b'])
            
        block = CsvSource({'path': path})
        result = block.process(None, None)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['id'], '1')
        self.assertEqual(result[0]['val'], 'a')
        
        # Cleanup
        shutil.rmtree('data_test')

    def test_export_json_csv(self):
        os.makedirs('output_test', exist_ok=True)
        data = [{'id': 1, 'name': 'test'}]
        
        # JSON Export
        json_path = 'output_test/out.json'
        exp_json = Export({'path': json_path, 'format': 'json'})
        exp_json.process(data, None)
        
        with open(json_path, 'r') as f:
            loaded = json.load(f)
        self.assertEqual(loaded, data)

        # CSV Export
        csv_path = 'output_test/out.csv'
        exp_csv = Export({'path': csv_path, 'format': 'csv'})
        exp_csv.process(data, None)
        
        with open(csv_path, 'r') as f:
            content = f.read()
        self.assertIn('id,name', content)
        self.assertIn('1,test', content)
        
        # Cleanup
        shutil.rmtree('output_test')

if __name__ == '__main__':
    unittest.main()
