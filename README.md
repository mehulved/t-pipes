```text
 _____           ______ _                 
|_   _|          | ___ (_)                
  | |    ______  | |_/ /_ _ __   ___  ___ 
  | |   |______| |  __/| | '_ \ / _ \/ __|
  | |            | |   | | |_) |  __/\__ \
  |_|            \_|   |_| .__/ \___||___/
                         | |              
                         |_|              
```

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

**`csv_source`**
Reads data from a CSV file into a list of dictionaries.
- `path`: (Required) Path to the CSV file.

```yaml
- type: csv_source
  config:
    path: ./data.csv
```

**`concat`**
Merges results from multiple sources into a single list.
- `sources`: (Required) List of source definitions. Each source can be a single block (`type` + `config`) or a sub-pipeline (`steps`).

```yaml
- type: concat
  config:
    sources:
      - type: csv_source
        config: { path: ./data.csv }
      - steps:
          - type: http_source
            config: { url: https://api.example.com/data }
          - type: json_parser
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
- `key`: (Required) The dictionary key to check. Nested keys supported (e.g., `user.address.city`).
- `value`: (Required) The value to compare against (ignored if `op` is `exists`).
- `op`: (Optional) `eq` (equality), `contains`, or `exists`. Default is `eq`.

```yaml
- type: filter
  config:
    key: category
    op: contains
    value: tech
```

**`pick`**
Extracts specific fields from the data.
- `key`: (Optional) Single nested key to extract as value (e.g., `rates.INR`).
- `keys`: (Optional) List of nested keys to extract into a new dictionary.

```yaml
- type: pick
  config:
    key: rates.INR
```

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

**`export`**
Exports the current data to a file.
- `format`: (Optional) `json` (default), `xml`, `html`, or `csv`.
- `path`: (Required) Path to save the file.

```yaml
- type: export
  config:
    format: csv
    path: ./output.csv
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
