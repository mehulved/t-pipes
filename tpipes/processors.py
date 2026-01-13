import json
from typing import Any, List, Dict
from .core import Block
from rich.console import Console
from rich.table import Table
from rich import print as rprint
import xmltodict
from bs4 import BeautifulSoup

class JsonParser(Block):
    def process(self, data: Any, context: Any) -> Any:
        if isinstance(data, str):
            try:
                return json.loads(data)
            except json.JSONDecodeError as e:
                rprint(f"[red]Failed to parse JSON:[/red] {e}")
                raise
        return data

class XmlParser(Block):
    def process(self, data: Any, context: Any) -> Any:
        if isinstance(data, str):
            try:
               # parse to dict
               return xmltodict.parse(data)
            except Exception as e:
                rprint(f"[red]Failed to parse XML:[/red] {e}")
                raise
        return data

class HtmlSelector(Block):
    def process(self, data: Any, context: Any) -> Any:
        selector = self.config.get('selector')
        if not selector:
             raise ValueError("HtmlSelector requires 'selector' in config")
        
        if not isinstance(data, str):
             # Try to handle if it's already a bs4 object? 
             # For now assume input is string.
             pass

        soup = BeautifulSoup(data, 'lxml') 
        # Extract text from selected elements
        results = [tag.get_text(strip=True) for tag in soup.select(selector)]
        return results


class Filter(Block):
    def process(self, data: Any, context: Any) -> Any:
        # Expects specific structure: list of dicts
        key = self.config.get('key')
        value = self.config.get('value')
        op = self.config.get('op', 'eq') # eq, contains
        
        if not isinstance(data, list):
            # If it's a dict, maybe we filter keys? For now assume list of items
            return data 
            
        filtered = []
        for item in data:
            if not isinstance(item, dict):
                continue
            item_val = item.get(key)
            if item_val is None:
                continue
            
            if op == 'eq':
                if str(item_val) == str(value):
                    filtered.append(item)
            elif op == 'contains':
                if str(value).lower() in str(item_val).lower():
                     filtered.append(item)
        return filtered

class Print(Block):
    cacheable = False
    
    def process(self, data: Any, context: Any) -> Any:
        console = Console()
        console.rule("[bold green]Step Output")
        
        if isinstance(data, list) and data and isinstance(data[0], dict):
            # Debugging check
            rprint(f"[dim]Data type: {type(data)}, Item type: {type(data[0])}[/dim]")
            if len(data) > 0:
                 rprint(f"[dim]Keys: {list(data[0].keys())}[/dim]")

            # Print table
            table = Table(show_header=True, header_style="bold magenta")
            # Dynamic columns based on first item keys
            # Limit number of columns to avoid messy wrap
            keys = list(data[0].keys())[:8] 
            
            for key in keys:
                table.add_column(str(key))
            
            for item in data[:10]: # Limit to 10 for view
                row = [str(item.get(k, '')) for k in keys]
                table.add_row(*row)
                
            console.print(table)
            
            if len(data) > 10:
                console.print(f"[italic]... and {len(data)-10} more items[/italic]")
                
        else:
            rprint(data)
            
        return data
