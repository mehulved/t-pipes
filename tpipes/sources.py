import requests
import os
import csv
from typing import Any, List, Dict
from .core import Block

class HttpSource(Block):
    def process(self, data: Any, context: Any) -> Any:
        url = self.config.get('url')
        if not url:
            raise ValueError("HttpSource requires 'url' in config")
        
        method = self.config.get('method', 'GET')
        # In a real app, we might want to handle headers, params etc.
        response = requests.request(method, url)
        response.raise_for_status()
        return response.text

class FileSource(Block):
    def process(self, data: Any, context: Any) -> Any:
        path = self.config.get('path')
        if not path:
             raise ValueError("FileSource requires 'path' in config")
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        with open(path, 'r') as f:
            return f.read()

class CsvSource(Block):
    def process(self, data: Any, context: Any) -> Any:
        path = self.config.get('path')
        if not path:
             raise ValueError("CsvSource requires 'path' in config")
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)

