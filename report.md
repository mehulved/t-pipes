# T-Pipes Verification Report
**Date:** Wed Jan 14 11:13:41 IST 2026

## Checking: Unit Tests
Command: `venv/bin/python tests_blocks.py -v`

```
test_csv_source (__main__.TestBlocks.test_csv_source) ... ok
test_export_json_csv (__main__.TestBlocks.test_export_json_csv) ... Exported data to 
output_test/out.json (json)
Exported data to 
output_test/out.csv (csv)
ok
test_export_xml_html (__main__.TestBlocks.test_export_xml_html) ... Exported data to 
output_test_2/out.xml (xml)
Exported data to 
output_test_2/out.html 
(html)
ok
test_file_source (__main__.TestBlocks.test_file_source) ... ok
test_filter_contains (__main__.TestBlocks.test_filter_contains) ... ok
test_filter_eq (__main__.TestBlocks.test_filter_eq) ... ok
test_html_selector (__main__.TestBlocks.test_html_selector) ... ok
test_http_source (__main__.TestBlocks.test_http_source) ... ok
test_json_parser (__main__.TestBlocks.test_json_parser) ... ok
test_print (__main__.TestBlocks.test_print) ... ─────── Step Output ───────
{'test': 123}
ok
test_xml_parser (__main__.TestBlocks.test_xml_parser) ... ok

----------------------------------------------------------------------
Ran 11 tests in 0.024s

OK
```

**RESULT:** ✅ PASS

---
## Checking: JSON Pipeline (example.yaml)
Command: `venv/bin/python main.py run example.yaml --refresh`

```
[1] Running http_source...
  -> Executed and cached: b91a0d9a (Str: 5645 chars)
[2] Running json_parser...
  -> Executed and cached: 6aea069a (List: 10 items)
[3] Running print...
─────── Step Output ───────
Data type: <class 'list'>, 
Item type: <class 'dict'>
Keys: ['id', 'name', 
'username', 'email', 
'address', 'phone', 
'website', 'company']
┏━━┳━━┳━━┳━━┳━━┳━━━┳━━┳━━━┓
┃  ┃  ┃  ┃  ┃  ┃ … ┃  ┃ … ┃
┡━━╇━━╇━━╇━━╇━━╇━━━╇━━╇━━━┩
│  │  │  │  │  │ … │  │ … │
│  │  │  │  │  │ … │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │ … │  │ … │
│  │  │  │  │  │ … │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │ … │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │ … │  │ … │
│  │  │  │  │  │ … │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │ … │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │ … │  │ … │
│  │  │  │  │  │ … │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │ … │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │ … │  │ … │
│  │  │  │  │  │ … │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │ … │  │ … │
│  │  │  │  │  │ … │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │ … │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
└──┴──┴──┴──┴──┴───┴──┴───┘
  -> Executed (List: 10 items)
[4] Running filter...
  -> Executed and cached: 01d002c2 (List: 2 items)
[5] Running print...
─────── Step Output ───────
Data type: <class 'list'>, 
Item type: <class 'dict'>
Keys: ['id', 'name', 
'username', 'email', 
'address', 'phone', 
'website', 'company']
┏━━┳━━┳━━┳━━┳━━┳━━━┳━━┳━━━┓
┃  ┃  ┃  ┃  ┃  ┃ … ┃  ┃ … ┃
┡━━╇━━╇━━╇━━╇━━╇━━━╇━━╇━━━┩
│  │  │  │  │  │ … │  │ … │
│  │  │  │  │  │ … │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │ … │  │ … │
│  │  │  │  │  │ … │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
│  │  │  │  │  │   │  │ … │
└──┴──┴──┴──┴──┴───┴──┴───┘
  -> Executed (List: 2 items)
```

**RESULT:** ✅ PASS

---
## Checking: XML Pipeline (example_xml.yaml)
Command: `venv/bin/python main.py run example_xml.yaml --refresh`

```
[1] Running file_source...
  -> Executed and cached: b6378f9a (Str: 544 chars)
[2] Running xml_parser...
  -> Executed and cached: c732d109 (Dict: 1 keys)
[3] Running print...
─────── Step Output ───────
{
    'rss': {
        '@version': '2.0',
        'channel': {
            'title': 
'T-Pipes News',
            'link': 
'https://www.example.com',
            'description': 
'T-Pipes is awesome',
            'item': [
                {
                    'title'
: 'XML Support Added',
                    'link':
'https://www.example.com/xm
l',
                    'descri
ption': 'Now supporting XML
parsing via xmltodict'
                },
                {
                    'title'
: 'HTML Scraping Live',
                    'link':
'https://www.example.com/ht
ml',
                    'descri
ption': 'Extract data with 
CSS selectors'
                }
            ]
        }
    }
}
  -> Executed (Dict: 1 keys)
```

**RESULT:** ✅ PASS

---
## Checking: HTML Pipeline (example_html.yaml)
Command: `venv/bin/python main.py run example_html.yaml --refresh`

```
[1] Running file_source...
  -> Executed and cached: 86f3bcb4 (Str: 600 chars)
[2] Running html_selector...
  -> Executed and cached: dce9e73b (List: 5 items)
[3] Running print...
─────── Step Output ───────
[
    'Modular Blocks',
    'Caching',
    'CLI Interface',
    'Update 1: Initial 
POC',
    'Update 2: Registry 
Support'
]
  -> Executed (List: 5 items)
```

**RESULT:** ✅ PASS

---
## Checking: Export Pipeline (example_export.yaml)
Command: `venv/bin/python main.py run example_export.yaml --refresh`

```
[1] Running csv_source...
  -> Executed and cached: 0784e480 (List: 3 items)
[2] Running print...
─────── Step Output ───────
Data type: <class 'list'>, 
Item type: <class 'dict'>
Keys: ['id', 'name', 
'role']
┏━━━━┳━━━━━━━━━┳━━━━━━━━━━┓
┃ id ┃ name    ┃ role     ┃
┡━━━━╇━━━━━━━━━╇━━━━━━━━━━┩
│ 1  │ Alice   │ Engineer │
│ 2  │ Bob     │ Designer │
│ 3  │ Charlie │ Manager  │
└────┴─────────┴──────────┘
  -> Executed (List: 3 items)
[3] Running export...
Exported data to 
output/users.json (json)
  -> Executed (List: 3 items)
[4] Running export...
Exported data to 
output/users.html (html)
  -> Executed (List: 3 items)
[5] Running export...
Exported data to 
output/users.xml (xml)
  -> Executed (List: 3 items)
[6] Running export...
Exported data to 
output/users_export.csv 
(csv)
  -> Executed (List: 3 items)
```

**RESULT:** ✅ PASS

---
