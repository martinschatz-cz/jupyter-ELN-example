import json
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import nbformat
import os

# ============================================================================
# LOAD RESULTS FROM INDIVIDUAL EXPERIMENTS - AUTOMATED EXTRACTION
# ============================================================================
# Extract results automatically from individual experiment .ipynb files
# by parsing their notebooks and retrieving the analysis_results variable

def extract_experiment_results(notebook_path):
    """
    Extract experiment metadata and results from an ELN experiment notebook.
    
    Looks for a cell containing 'analysis_results = {...}' and extracts the dict.
    Falls back to searching for experiment_metadata if needed.
    
    Args:
        notebook_path (str): Path to the .ipynb file
    
    Returns:
        dict: Extracted experiment results with all biometric measurements
    """
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)
    except FileNotFoundError:
        print(f"  WARNING: Could not find {notebook_path}")
        return None
    
    # Search through notebook cells for analysis_results definition
    for cell in notebook.cells:
        if cell.cell_type == 'code':
            source = cell.source
            
            # Look for analysis_results dictionary
            if 'analysis_results' in source and '=' in source:
                # Try to extract and parse the analysis_results dict
                try:
                    # Find the line(s) defining analysis_results
                    lines = source.split('\n')
                    dict_start = None
                    for i, line in enumerate(lines):
                        if 'analysis_results' in line and '=' in line:
                            dict_start = i
                            break
                    
                    if dict_start is not None:
                        # Reconstruct the dictionary definition from source
                        dict_lines = []
                        brace_count = 0
                        found_opening = False
                        
                        for line in lines[dict_start:]:
                            dict_lines.append(line)
                            brace_count += line.count('{') - line.count('}')
                            
                            if '{' in line:
                                found_opening = True
                            
                            # Stop when we've closed all braces
                            if found_opening and brace_count == 0:
                                break
                        
                        # Execute to extract the dict
                        exec_globals = {}
                        exec('\n'.join(dict_lines), exec_globals)
                        
                        if 'analysis_results' in exec_globals:
                            return exec_globals['analysis_results']
                except Exception as e:
                    print(f"  Error parsing {os.path.basename(notebook_path)}: {e}")
                    continue
    
    return None


def extract_experiment_results_from_output(notebook_path):
    """
    Extracts the analysis_results JSON printed by the experiment notebook.

    Looks specifically for output text that contains valid JSON blocks,
    such as the output of:
        print(json.dumps(analysis_results, indent=2))

    Args:
        notebook_path (str): Path to .ipynb
    
    Returns:
        dict or None: Parsed analysis_results dictionary
    """
    try:
        with open(notebook_path, "r", encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)
    except Exception as e:
        print(f"  ERROR: Unable to read {notebook_path}: {e}")
        return None

    # Scan for printed JSON output
    for cell in nb.cells:
        if cell.cell_type != "code":
            continue

        if "outputs" not in cell:
            continue

        for output in cell.outputs:
            # Text outputs from print(...) appear here:
            if hasattr(output, "text"):
                text = output.text.strip()

                # Try to isolate JSON block
                if text.startswith("{") and text.endswith("}"):
                    try:
                        data = json.loads(text)
                        return data
                    except json.JSONDecodeError:
                        pass

                # Also handle cases where print adds a header line before JSON
                if "{" in text and "}" in text:
                    try:
                        json_part = text[text.index("{") : text.rindex("}") + 1]
                        data = json.loads(json_part)
                        return data
                    except Exception:
                        continue

    print("  WARNING: No valid JSON output found in notebook.")
    return None