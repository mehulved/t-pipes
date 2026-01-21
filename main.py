import argparse
import yaml
import sys
import os
from tpipes.runner import PipelineRunner
from tpipes.sources import HttpSource, FileSource
from tpipes.processors import JsonParser, Filter, Print, XmlParser, HtmlSelector, Export, Pick, Concat, Mesh, CsvParser, Lookup
from tpipes.registry import PipelineRegistry

BLOCK_REGISTRY = {
    'http_source': HttpSource,
    'file_source': FileSource,
    'csv_parser': CsvParser,
    'concat': Concat,
    'mesh': Mesh,
    'json_parser': JsonParser,
    'xml_parser': XmlParser,
    'html_selector': HtmlSelector,
    'filter': Filter,
    'pick': Pick,
    'export': Export,
    'print': Print,
    'lookup': Lookup
}

def load_config(path: str):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

import shutil
import zipfile
import glob

def run_pipeline(path: str, refresh: bool = False):
    try:
        config = load_config(path)
        
        # Derive pipeline name from file path
        # e.g., ./pipelines/my_pipe.yaml -> my_pipe
        pipeline_name = os.path.splitext(os.path.basename(path))[0]
        
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

        runner = PipelineRunner(pipeline_steps, BLOCK_REGISTRY, pipeline_name=pipeline_name)
        runner.run(force_refresh=refresh)
        
    except FileNotFoundError:
        print(f"Error: Config file '{path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def export_cache(pipeline_name_or_path: str, output_path: str):
    # Determine pipeline name
    if os.path.exists(pipeline_name_or_path):
        pipeline_name = os.path.splitext(os.path.basename(pipeline_name_or_path))[0]
        source_yaml_path = pipeline_name_or_path
    else:
        pipeline_name = pipeline_name_or_path
        source_yaml_path = None # We might look it up in registry if needed, but for now optional

    cache_dir = os.path.join('.', '.cache', pipeline_name)
    
    if not os.path.exists(cache_dir):
        print(f"Error: No cache found for pipeline '{pipeline_name}' at {cache_dir}")
        return

    print(f"Exporting cache for '{pipeline_name}' to '{output_path}'...")
    
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 1. Add cache files
        # We walk the directory to add all files
        for root, dirs, files in os.walk(cache_dir):
            for file in files:
                if file.endswith(".pkl"):
                    abs_path = os.path.join(root, file)
                    # Archive name should be relative to facilitate clean import
                    # We store it as .cache/<pipeline_name>/<file> provided we extract correctly
                    # OR we just store as <pipeline_name>/<file> inside zip?
                    # Let's store as <pipeline_name>/<file>
                    arcname = os.path.join(pipeline_name, file)
                    zipf.write(abs_path, arcname)
                    print(f"  Added {file}")
        
        # 2. Add source YAML if available
        if source_yaml_path:
             zipf.write(source_yaml_path, os.path.basename(source_yaml_path))
             print(f"  Added source config: {os.path.basename(source_yaml_path)}")
             
    print(f"Done. Exported to {output_path}")

def import_cache(zip_path: str):
    if not os.path.exists(zip_path):
        print(f"Error: File '{zip_path}' not found.")
        return
        
    print(f"Importing cache from '{zip_path}'...")
    
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        # Check contents
        file_list = zipf.namelist()
        
        # Logic: 
        # If file is like "pipeline_name/hash.pkl", extract it to .cache/pipeline_name/hash.pkl
        # If file is "*.yaml", extract it to current dir?
        
        for file in file_list:
             if file.endswith(".pkl"):
                  # It should have the directory structure in it
                  # Extract to .cache/
                  # zipfile extract uses the full path in arcname
                  target_path = os.path.join('.', '.cache', file)
                  
                  # Ensure target dir structure exists
                  target_dir = os.path.dirname(target_path)
                  os.makedirs(target_dir, exist_ok=True)
                  
                  with open(target_path, "wb") as f_out:
                       f_out.write(zipf.read(file))
                  print(f"  Imported cache: {file}")
             
             elif file.endswith(".yaml") or file.endswith(".yml"):
                  # Extract config to current directory
                  zipf.extract(file, ".")
                  print(f"  Imported config: {file}")
                  
    print("Done.")

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

    # Cache command
    cache_parser = subparsers.add_parser('cache', help='Manage cache')
    cache_sub = cache_parser.add_subparsers(dest='cache_command')
    
    cexport = cache_sub.add_parser('export', help='Export cache to zip')
    cexport.add_argument('pipeline', help='Pipeline name OR path to YAML file')
    cexport.add_argument('output', help='Output zip file path')
    
    cimport = cache_sub.add_parser('import', help='Import cache from zip')
    cimport.add_argument('input', help='Input zip file path')

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
    
    elif args.command == 'cache':
        if args.cache_command == 'export':
             export_cache(args.pipeline, args.output)
        elif args.cache_command == 'import':
             import_cache(args.input)
        else:
             cache_parser.print_help()

    else:
        # Fallback for backward compatibility or simple usage:
        # If arguments provided and not a command, try to treat as run
        if len(sys.argv) > 1 and sys.argv[1] not in ['run', 'register', 'list', 'cache'] and not sys.argv[1].startswith('-'):
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
