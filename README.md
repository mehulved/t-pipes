# T-Pipes (Terminal Pipes)

A terminal-based data pipeline tool similar to Yahoo Pipes. Chain together blocks to fetch, process, and visualize data.

## Usage

```bash
# Run a specific file
python main.py example.yaml

# Register a pipeline
python main.py register example.yaml --name mypipe

# List available pipelines
python main.py list

# Run a registered pipeline
python main.py run mypipe

# Force refresh cache
python main.py run mypipe --refresh
```

## DSL Reference

Pipelines are defined in YAML format as a list of steps. Each step has a `type` and an optional `config`.

### Blocks

#### Sources

**`http_source`**
Fetches data from a URL.
- `url`: (Required) The URL to fetch.
- `method`: (Optional) HTTP method (default: `GET`).

```yaml
- type: http_source
  config:
    url: https://api.example.com/data
```

**`file_source`**
Reads data from a local file.
- `path`: (Required) Path to the file.

```yaml
- type: file_source
  config:
    path: ./data.json
```

#### Processors

**`json_parser`**
Parses a JSON string into a Python list/dictionary.
- *No configuration required.*

```yaml
- type: json_parser
```

**`xml_parser`**
Parses XML string into a Python dictionary (using `xmltodict`).
- *No configuration required.*

```yaml
- type: xml_parser
```

**`html_selector`**
Extracts text from HTML using CSS selectors (using `BeautifulSoup`).
- `selector`: (Required) CSS selector string (e.g., `div.content > p`).

```yaml
- type: html_selector
  config:
     selector: "h1.title"
```

**`filter`**
Filters a list of dictionaries based on a criteria.
- `key`: (Required) The dictionary key to check.
- `value`: (Required) The value to compare against.
- `op`: (Optional) The operation: `eq` (equality) or `contains`. Default is `eq`.

```yaml
- type: filter
  config:
    key: category
    op: contains
    value: tech
```

#### Output

**`print`**
Visualizes the data in the terminal. Prints tables for lists of dictionaries, or raw output for other types.
- *No configuration required.*

```yaml
- type: print
```

## specific examples

### Fetch and Filter

```yaml
- type: http_source
  config:
    url: https://jsonplaceholder.typicode.com/users
- type: json_parser
- type: filter
  config:
    key: website
    op: contains
    value: .org
- type: print
```
