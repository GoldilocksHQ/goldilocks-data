import os


def get_goldilocks_data_root() -> str:
    """
    Traverses up from the current file's location to find the 'goldilocks-data'
    project root, which is identified by the presence of a '.git' directory
    within it. This makes pathing robust to where the script is called from.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # We expect this file to be in .../goldilocks-data/src/config/
    # So we traverse up until we find the directory containing '.git'
    while True:
        # Assuming the .git folder is at the root of the goldilocks-data project
        if ".git" in os.listdir(current_dir):
            return current_dir
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            # Reached the filesystem root and didn't find .git
            raise FileNotFoundError(
                "Could not find the project root. Make sure you are running within the git repository."
            )
        current_dir = parent_dir


# This will be the path to the 'goldilocks-data' directory
GOLDILOCKS_DATA_ROOT = get_goldilocks_data_root()

# All other paths are relative to this root.
DATA_DIR = os.path.join(GOLDILOCKS_DATA_ROOT, "data")
LOGS_DIR = os.path.join(GOLDILOCKS_DATA_ROOT, "logs")
LEDGER_DIR = os.path.join(DATA_DIR, "systematic_request_ledgers")
NEURON360_DATA_DIR = os.path.join(DATA_DIR, "neuron360")
UK_PROFILES_DIR = os.path.join(NEURON360_DATA_DIR, "profile_search_uk_results")
LOG_FILE_PATH = os.path.join(LOGS_DIR, "goldilocks.log")
