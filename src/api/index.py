import sys
import os
from pathlib import Path

def app(event, context):
    print("Event:", event)
    print("Context:", context)
    print("Current working directory:", os.getcwd())
    print("Directory contents:", os.listdir())
    print("Python path:", sys.path)
    
    root_path = Path(__file__).resolve().parent.parent
    print("Root path:", root_path)
    print("Root directory contents:", os.listdir(root_path))
    
    rpalmdata_path = root_path / 'rpalmdata'
    if rpalmdata_path.exists():
        print("rpalmdata directory contents:", os.listdir(rpalmdata_path))
    else:
        print("rpalmdata directory does not exist")
    
    return {
        'statusCode': 200,
        'body': 'Debug information printed to logs'
    }