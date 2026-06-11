#!/usr/bin/env python3
# ---
# requires:
#   env: []
#   bins:
#     - git
# permissions:
#   filesystem: read/write
#   description: Setup output directories for microservice code reconstruction and check rule files presence.
# ---

import os
import sys
import argparse

# Default Workspace Configuration
DEFAULT_CODE_ROOT = "C:/Users/10240008/zhixu-code-ws/zhiliang/code"
DEFAULT_OUTPUT_ROOT = "C:/Users/10240008/zhixu-code-ws/iepmszhiliang"

# Rules Files to check
RULES = {
    "Feature List Rules": "commands/01-prd-rules/feature-list-generation-rules_v1.md",
    "PRD Gen Rules": "commands/01-prd-rules/prd-generation_v8.md",
    "PRD Review Rules": "commands/01-prd-rules/prd-completeness-check.md",
    "DoD Criteria": "commands/01-prd-rules/xuqiuceshidod.md",
    "API Gen Rules": "commands/02-api-rules/api-doc-generation-rules_v1.md",
    "API Review Rules": "commands/02-api-rules/api-doc-reconstruction-review-rules_v1.md",
    "Design Gen Rules": "commands/03-design-rules/design-doc-reconstruction-rules_v2.md",
    "Design Review Rules": "commands/03-design-rules/design-doc-reconstruction-review-rules_v2.md"
}

def check_rules():
    print("[*] Verifying rules files presence in the repository...")
    missing = 0
    for key, path in RULES.items():
        if os.path.exists(path):
            print(f"  [+] Found: {key} -> {path}")
        else:
            print(f"  [-] MISSING: {key} -> {path}")
            missing += 1
    return missing == 0

def init_workspace(microservice_name, output_root):
    print(f"\n[*] Initializing directories for microservice: '{microservice_name}'...")
    base_dir = os.path.join(output_root, "knowledge", "micro", microservice_name)
    
    subdirs = [
        "prd-docs",
        "prd-review",
        "api-docs",
        "api-review",
        "design-docs",
        "design-review"
    ]
    
    for folder in subdirs:
        dir_path = os.path.join(base_dir, folder)
        try:
            os.makedirs(dir_path, exist_ok=True)
            print(f"  [+] Created: {dir_path}")
        except Exception as e:
            print(f"  [-] Failed to create {dir_path}: {e}")
            sys.exit(1)
            
    print(f"\n[+] Initialization complete. You can output files under: {base_dir}")

def main():
    parser = argparse.ArgumentParser(description="OpenClaw Skill Helper: Code Reconstruction workflow environment manager")
    parser.add_argument("--service", "-s", required=True, help="Microservice name to initialize folders for")
    parser.add_argument("--output-root", "-o", default=DEFAULT_OUTPUT_ROOT, help="Base path for outputting docs")
    
    args = parser.parse_args()
    
    # Check rule files
    rules_ok = check_rules()
    if not rules_ok:
        print("[!] Warning: Some rule files are missing. Make sure you are running this from the repository root directory.")
        
    init_workspace(args.service, args.output_root)

if __name__ == "__main__":
    main()
