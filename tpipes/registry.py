import json
import os
from typing import Dict, List, Optional
from rich.table import Table
from rich.console import Console

REGISTRY_FILE = ".tpipes_registry.json"

class PipelineRegistry:
    def __init__(self):
        self.registry_path = REGISTRY_FILE
        self._load()

    def _load(self):
        if os.path.exists(self.registry_path):
            with open(self.registry_path, 'r') as f:
                self.pipelines = json.load(f)
        else:
            self.pipelines = {}

    def save(self):
        with open(self.registry_path, 'w') as f:
            json.dump(self.pipelines, f, indent=2)

    def register_pipeline(self, name: str, path: str):
        abs_path = os.path.abspath(path)
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"Pipeline file not found: {path}")
        
        self.pipelines[name] = abs_path
        self.save()
        print(f"Registered pipeline '{name}' -> {abs_path}")

    def get_pipeline_path(self, name: str) -> Optional[str]:
        return self.pipelines.get(name)

    def list_pipelines(self):
        console = Console()
        table = Table(title="Available Pipelines")
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Path", style="magenta")

        for name, path in self.pipelines.items():
            table.add_row(name, path)

        console.print(table)
