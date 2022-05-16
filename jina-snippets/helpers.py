import os
import pathlib
import shutil


def print_search_results(docs):
    left_da = docs[0]
    
    print(f"\nYour search results for: {left_da.text}")
    print("-------------------\n")

    for match in left_da.matches:
        print(f"> {match.scores['cosine'].value:.3f} - {match.text}")

def clear_workspace(workspace):
    current_dir = pathlib.Path(__file__).parent.resolve()
    if os.path.exists(os.path.join(current_dir, "workspace")):
        print("[INFO] removing existing workspace...")
        shutil.rmtree(os.path.join(current_dir, f"{workspace}"))

