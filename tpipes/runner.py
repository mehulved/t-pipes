import hashlib
import pickle
import os
import json
from typing import List, Dict, Any
from .core import Block
import importlib

class PipelineContext:
    def __init__(self, base_dir: str = ".", block_registry: Dict[str, Any] = None, pipeline_name: str = "default"):
        self.base_dir = base_dir
        self.pipeline_name = pipeline_name
        self.cache_dir = os.path.join(base_dir, '.cache', pipeline_name)
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        self.block_registry = block_registry or {}

class PipelineRunner:
    def __init__(self, pipeline_config: List[Dict[str, Any]], block_registry: Dict[str, Any], pipeline_name: str = "default", context: PipelineContext = None):
        self.config = pipeline_config
        # reuse context if provided (for sub-pipelines), else create new
        self.context = context or PipelineContext(block_registry=block_registry, pipeline_name=pipeline_name)
        self.block_registry = block_registry

    def _get_cache_key(self, block_name: str, config: Dict, input_data: Any) -> str:
        """Generate a unique hash for the block execution."""
        # We assume input_data is hashable or serializable to string for hashing
        # For simplicity in this POC, we'll try to execute consistent string representation
        try:
            input_str = str(input_data)
        except Exception:
            # Fallback for un-stringifiable data (though most should be)
            input_str = str(id(input_data)) 
        
        content = f"{block_name}{json.dumps(config, sort_keys=True)}{input_str}"
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    def _load_cache(self, key: str) -> Any:
        cache_path = os.path.join(self.context.cache_dir, f"{key}.pkl")
        if os.path.exists(cache_path):
            with open(cache_path, 'rb') as f:
                return pickle.load(f)
        return None

    def _save_cache(self, key: str, data: Any):
        cache_path = os.path.join(self.context.cache_dir, f"{key}.pkl")
        with open(cache_path, 'wb') as f:
            pickle.dump(data, f)

    def run(self, force_refresh: bool = False, verbose: bool = True):
        current_data = None
        
        for step_idx, step_conf in enumerate(self.config):
            block_type = step_conf.get('type')
            block_config = step_conf.get('config', {})
            
            if block_type not in self.block_registry:
                raise ValueError(f"Unknown block type: {block_type}")
            
            block_cls = self.block_registry[block_type]
            block = block_cls(block_config)
            
            if verbose:
                print(f"[{step_idx+1}] Running {block_type}...")
            
            # Caching Logic
            cache_key = self._get_cache_key(block_type, block_config, current_data)
            
            # Default to not using cache if block says so
            should_cache = block.cacheable
            cached_result = None

            if should_cache:
                cached_result = self._load_cache(cache_key)
            
            if cached_result is not None and not force_refresh:
                if verbose:
                    print(f"  -> Used cache: {cache_key[:8]}", end="")
                    self._print_summary(cached_result)
                current_data = cached_result
            else:
                current_data = block.process(current_data, self.context)
                if should_cache:
                    self._save_cache(cache_key, current_data)
                    if verbose:
                        print(f"  -> Executed and cached: {cache_key[:8]}", end="")
                        self._print_summary(current_data)
                elif verbose:
                     # For non-cached blocks (like Print), just say Executed
                     print(f"  -> Executed", end="")
                     self._print_summary(current_data)

        return current_data

    def _print_summary(self, data: Any):
        """Helper to print a summary of the data."""
        if isinstance(data, list):
            print(f" (List: {len(data)} items)")
        elif isinstance(data, str):
            print(f" (Str: {len(data)} chars)")
        elif isinstance(data, dict):
            print(f" (Dict: {len(data)} keys)")
        else:
            print(f" ({type(data).__name__})")
