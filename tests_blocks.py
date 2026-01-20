import unittest
from tpipes.processors import JsonParser, XmlParser, HtmlSelector, Filter, Export, Print, CsvParser
from tpipes.sources import FileSource, HttpSource
import os
import csv
import json
import shutil
from unittest.mock import patch, MagicMock



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

    def test_csv_parser(self):
        # Test CsvParser with string input
        csv_data = "id,val\n1,a\n2,b"
        
        block = CsvParser()
        result = block.process(csv_data, None)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['id'], '1')
        self.assertEqual(result[0]['val'], 'a')
        
        # Test autodetection with semicolon
        csv_semi = "id;val\n1;a\n2;b"
        result_semi = block.process(csv_semi, None)
        self.assertEqual(len(result_semi), 2)
        self.assertEqual(result_semi[1]['val'], 'b')

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

    def test_export_xml_html(self):
        os.makedirs('output_test_2', exist_ok=True)
        data = {'id': 1, 'name': 'test'}
        
        # XML Export
        xml_path = 'output_test_2/out.xml'
        exp_xml = Export({'path': xml_path, 'format': 'xml'})
        exp_xml.process(data, None)
        
        with open(xml_path, 'r') as f:
            content = f.read()
        self.assertIn('<root>', content)
        self.assertIn('<name>test</name>', content)

        # HTML Export
        html_path = 'output_test_2/out.html'
        exp_html = Export({'path': html_path, 'format': 'html'})
        # HTML export expects list of dicts for table
        list_data = [data]
        exp_html.process(list_data, None)
        
        with open(html_path, 'r') as f:
            content = f.read()
        self.assertIn('<table', content)
        self.assertIn('<td>test</td>', content)
        
        # Cleanup
        shutil.rmtree('output_test_2')

    def test_file_source(self):
        os.makedirs('data_test_2', exist_ok=True)
        path = 'data_test_2/test.txt'
        with open(path, 'w') as f:
            f.write("Hello World")
            
        block = FileSource({'path': path})
        result = block.process(None, None)
        self.assertEqual(result, "Hello World")
        
        shutil.rmtree('data_test_2')

    @patch('requests.request')
    def test_http_source(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = "API Data"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        block = HttpSource({'url': 'http://test.com'})
        result = block.process(None, None)
        self.assertEqual(result, "API Data")
        mock_get.assert_called_with('GET', 'http://test.com')

    def test_print(self):
        # Print is output only, just verify pass-through
        block = Print()
        data = {'test': 123}
        result = block.process(data, None)
        self.assertEqual(result, data)


if __name__ == '__main__':
    unittest.main()
