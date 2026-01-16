import argparse
import yaml
import sys
import os
from tpipes.runner import PipelineRunner
from tpipes.sources import HttpSource, FileSource, CsvSource
from tpipes.processors import JsonParser, Filter, Print, XmlParser, HtmlSelector, Export, Pick
from tpipes.registry import PipelineRegistry

BLOCK_REGISTRY = {
    'http_source': HttpSource,
    'file_source': FileSource,
    'csv_source': CsvSource,
    'json_parser': JsonParser,
    'xml_parser': XmlParser,
    'html_selector': HtmlSelector,
    'filter': Filter,
    'pick': Pick,
    'export': Export,
    'print': Print
}

def load_config(path: str):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def run_pipeline(path: str, refresh: bool = False):
    try:
        config = load_config(path)
        
        # Flexible config: can be list of steps or dict with 'steps'
        pipeline_steps = config
        if isinstance(config, dict):
             if 'steps' in config:
                 pipeline_steps = config['steps']
             else:
                 print("Error: Config root must be a list of steps or a dict containing 'steps'.")
                 sys.exit(1)
        
        if not isinstance(pipeline_steps, list):
             print(f"Error: Pipeline steps must be a list, got {type(pipeline_steps)}")
             sys.exit(1)

        runner = PipelineRunner(pipeline_steps, BLOCK_REGISTRY)
        runner.run(force_refresh=refresh)
        
    except FileNotFoundError:
        print(f"Error: Config file '{path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def main():
    registry = PipelineRegistry()
    
    parser = argparse.ArgumentParser(description="T-Pipes: Terminal Data Pipelines")
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Run command
    run_parser = subparsers.add_parser('run', help='Run a pipeline')
    run_parser.add_argument('name_or_path', help='Name of registered pipeline OR path to YAML file')
    run_parser.add_argument("--refresh", action="store_true", help="Force refresh of cache")

    # Register command
    reg_parser = subparsers.add_parser('register', help='Register a pipeline')
    reg_parser.add_argument('path', help='Path to YAML file')
    reg_parser.add_argument('--name', help='Name for the pipeline (defaults to filename without extension)')

    # List command
    subparsers.add_parser('list', help='List registered pipelines')

    args = parser.parse_args()

    if args.command == 'run':
        target = args.name_or_path
        # Check if it's a registered name
        path = registry.get_pipeline_path(target)
        if not path:
            # If not registered, assume it's a path
            path = target
        
        if not os.path.exists(path):
             print(f"Error: Pipeline '{target}' not found in registry and file '{target}' does not exist.")
             sys.exit(1)
             
        run_pipeline(path, refresh=args.refresh)

    elif args.command == 'register':
        name = args.name
        if not name:
            name = os.path.splitext(os.path.basename(args.path))[0]
        try:
            registry.register_pipeline(name, args.path)
        except Exception as e:
            print(f"Error registering pipeline: {e}")

    elif args.command == 'list':
        registry.list_pipelines()

    else:
        # Fallback for backward compatibility or simple usage:
        # If arguments provided and not a command, try to treat as run
        if len(sys.argv) > 1 and sys.argv[1] not in ['run', 'register', 'list'] and not sys.argv[1].startswith('-'):
             # Assume implicit run
             target = sys.argv[1]
             path = registry.get_pipeline_path(target) or target
             if os.path.exists(path):
                 # print(f"[Note] Implicitly running: {path}") # Optional verbosity
                 run_pipeline(path)
             else:
                 parser.print_help()
        else:
            parser.print_help()

if __name__ == "__main__":
    main()
