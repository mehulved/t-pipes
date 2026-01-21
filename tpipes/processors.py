import json
from typing import Any, List, Dict
from .core import Block
from rich.console import Console
from rich.table import Table
from rich import print as rprint
import xmltodict
import csv
import os
import io
from bs4 import BeautifulSoup

class Concat(Block):
    cacheable = False
    
    def process(self, data: Any, context: Any) -> Any:
        # Concatenates results from multiple sources defined in config
        sources_conf = self.config.get('sources', [])
        if not sources_conf:
             return []
        
        # Delayed import to avoid circular dependency
        from .runner import PipelineRunner
        
        result_list = []
        
        for source_def in sources_conf:
            source_result = None
            
            # Option 1: Full sub-pipeline
            if 'steps' in source_def:
                runner = PipelineRunner(source_def['steps'], context.block_registry, context=context)
                source_result = runner.run(verbose=False)
                
            # Option 2: Single block shorthand
            elif 'type' in source_def:
                stype = source_def.get('type')
                sconfig = source_def.get('config', {})
                
                if stype not in context.block_registry:
                    rprint(f"[red]Unknown block type in concat source: {stype}[/red]")
                    continue
                    
                block_cls = context.block_registry[stype]
                block = block_cls(sconfig)
                source_result = block.process(None, context)
            
            # Normalize and append
            if isinstance(source_result, list):
                result_list.extend(source_result)
            elif source_result is not None:
                result_list.append(source_result)
                
        return result_list

class Mesh(Block):
    cacheable = False
    
    def process(self, data: Any, context: Any) -> Any:
        # Meshes results from multiple sources into a dictionary based on mapping
        mapping = self.config.get('mapping', {})
        if not mapping:
             return {}
        
        from .runner import PipelineRunner
        
        result_dict = {}
        
        for key, source_def in mapping.items():
            source_result = None
            
            # Handle list of steps directly (most likely for mesh mapping)
            # mapping: key: [list of steps]
            if isinstance(source_def, list):
                 # Assume it's a pipeline definition (list of steps)
                 runner = PipelineRunner(source_def, context.block_registry, context=context)
                 source_result = runner.run(verbose=False)
            
            elif isinstance(source_def, dict):
                # Single block or explicit 'steps' dict
                if 'steps' in source_def:
                    runner = PipelineRunner(source_def['steps'], context.block_registry, context=context)
                    source_result = runner.run(verbose=False)
                elif 'type' in source_def:
                    stype = source_def.get('type')
                    sconfig = source_def.get('config', {})
                    
                    if stype not in context.block_registry:
                        rprint(f"[red]Unknown block type in mesh key '{key}': {stype}[/red]")
                        continue
                        
                    block_cls = context.block_registry[stype]
                    block = block_cls(sconfig)
                    source_result = block.process(None, context)
            
            result_dict[key] = source_result
            
        return result_dict

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


class CsvParser(Block):
    def process(self, data: Any, context: Any) -> Any:
        if not isinstance(data, str):
            # Maybe it's already a list?
            if isinstance(data, list):
                 return data
            raise ValueError("CsvParser expects a string input (or already parsed list)")
            
        delimiter = self.config.get('delimiter')
        quotechar = self.config.get('quotechar', '"')
        
        # Autodetection
        if not delimiter:
            try:
                # Sample the first few lines
                sample = '\n'.join(data.splitlines()[:5])
                dialect = csv.Sniffer().sniff(sample)
                delimiter = dialect.delimiter
                # rprint(f"[dim]Autodetected delimiter: {repr(delimiter)}[/dim]")
            except csv.Error:
                # Fallback
                delimiter = ','
                
        f = io.StringIO(data)
        reader = csv.DictReader(f, delimiter=delimiter, quotechar=quotechar)
        return list(reader)

class Export(Block):
    cacheable = False  # Export is a side-effect, usually we want it to run? Or maybe cache logic handles it?
                       # Actually, if we cache the output (which is the data passed through), 
                       # we might skip the file writing if we just load from cache.
                       # So Export block should NOT be effectively cached if the side effect is crucial.
                       # However, our runner logic uses `cacheable` to decide if we LOOKUP cache. 
                       # If we set cacheable=False, it runs process().
    
    def process(self, data: Any, context: Any) -> Any:
        # Pass-through block: returns data as-is, but writes to file.
        
        fmt = self.config.get('format', 'json').lower()
        path = self.config.get('path')
        
        if not path:
             raise ValueError("Export block requires 'path'")
        
        # Ensure dir exists
        os.makedirs(os.path.dirname(os.path.abspath(path)) or '.', exist_ok=True)

        if fmt == 'json':
            context_dict = data
            if not isinstance(context_dict, (dict, list)):
                 # try to wrap?
                 pass
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
                
        elif fmt == 'xml':
            to_write = data
            if isinstance(data, dict):
                 if len(data.keys()) != 1:
                     to_write = {'root': data}
            elif isinstance(data, list):
                 to_write = {'root': {'item': data}}
            
            with open(path, 'w', encoding='utf-8') as f:
                xmltodict.unparse(to_write, output=f, pretty=True)
                
        elif fmt == 'csv':
            if isinstance(data, dict):
                 data = [data]
            if not isinstance(data, list):
                 raise ValueError("CSV export requires a list of dicts (or a single dict)")
            if not data:
                 # Empty list, just create empty file
                 with open(path, 'w') as f: pass
            else:
                 keys = data[0].keys()
                 with open(path, 'w', newline='', encoding='utf-8') as f:
                     writer = csv.DictWriter(f, fieldnames=keys)
                     writer.writeheader()
                     writer.writerows(data)
                     
        elif fmt == 'html':
            # Basic HTML table export
             if not isinstance(data, list):
                 content = f"<pre>{data}</pre>"
             else:
                 # Create a simple table
                 if not data:
                     content = "<p>No data</p>"
                 else:
                     keys = data[0].keys()
                     rows = []
                     rows.append("<tr>" + "".join(f"<th>{k}</th>" for k in keys) + "</tr>")
                     for item in data:
                         rows.append("<tr>" + "".join(f"<td>{item.get(k, '')}</td>" for k in keys) + "</tr>")
                     content = f"<table border='1'>{''.join(rows)}</table>"
            
             html = f"<html><body>{content}</body></html>"
             with open(path, 'w', encoding='utf-8') as f:
                 f.write(html)
        
        else:
             raise ValueError(f"Unsupported format: {fmt}")
             
        rprint(f"[green]Exported data to {path} ({fmt})[/green]")
        return data



def get_nested_value(data: Any, path: str) -> Any:
    keys = path.split('.')
    current = data
    for k in keys:
        if isinstance(current, dict):
            current = current.get(k)
        elif isinstance(current, list):
            # Optional: handle list index access like users.0.name?
            # For simplicity, let's stick to dict keys for now, or maybe simple integer support
            try:
                idx = int(k)
                if 0 <= idx < len(current):
                    current = current[idx]
                else:
                    return None
            except ValueError:
                return None
        else:
            return None
        
        if current is None:
            return None
    return current

class Filter(Block):
    def process(self, data: Any, context: Any) -> Any:
        # Expects specific structure: list of dicts
        key = self.config.get('key')
        value = self.config.get('value')
        op = self.config.get('op', 'eq') # eq, contains, exists
        
        if not isinstance(data, list):
            # If it's a dict, maybe we filter keys? For now assume list of items
            return data 
            
        filtered = []
        for item in data:
            if not isinstance(item, (dict, list)):
                continue
                
            item_val = get_nested_value(item, key)
            
            # Handle 'exists' op specifically
            if op == 'exists':
                if item_val is not None:
                    filtered.append(item)
                continue

            if item_val is None:
                continue
            
            if op == 'eq':
                if str(item_val) == str(value):
                    filtered.append(item)
            elif op == 'contains':
                if str(value).lower() in str(item_val).lower():
                     filtered.append(item)
        return filtered

class Pick(Block):
    def process(self, data: Any, context: Any) -> Any:
        # Extracts specific fields from the data
        # config: key (string) or keys (list of strings)
        key = self.config.get('key')
        keys = self.config.get('keys')
        
        if not key and not keys:
            raise ValueError("Pick block requires 'key' or 'keys' in config")
            
        def extract(item):
            if key:
                return get_nested_value(item, key)
            else:
                # Return a new dict with only selected keys
                # We flatten the keys for the new dict? or keep structure?
                # "user.name" -> {"user.name": "Bob"} seems safer for flattening
                return {k: get_nested_value(item, k) for k in keys}

        if isinstance(data, list):
            return [extract(item) for item in data]
        elif isinstance(data, (dict, list)):
            return extract(data)
        
        return data

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

class Lookup(Block):
    def process(self, data: Any, context: Any) -> Any:
        lookup_path = self.config.get('lookup_key')
        source_path = self.config.get('source_key')
        
        if not lookup_path or not source_path:
             raise ValueError("Lookup block requires 'lookup_key' and 'source_key'")
             
        key_val = get_nested_value(data, lookup_path)
        source_container = get_nested_value(data, source_path)
        
        if source_container is None:
             # Decide if we want to error or return None. 
             # Block usually shouldn't break pipeline unless critical?
             # But if expected source is missing, it's likely error.
             # rprint(f"[red]Source container not found at {source_path}[/red]")
             return None
             
        if not isinstance(source_container, (dict, list)):
             raise ValueError(f"Source container at '{source_path}' must be dict or list. Got {type(source_container)}")
             
        try:
            if isinstance(source_container, dict):
                 # key_val might be int or str
                 return source_container.get(str(key_val))
            elif isinstance(source_container, list):
                 idx = int(key_val)
                 if 0 <= idx < len(source_container):
                     return source_container[idx]
        except (ValueError, TypeError):
            rprint(f"[red]Failed to lookup key '{key_val}' in source[/red]")
            return None
            
        return None
