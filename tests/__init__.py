""" python -m unittest discover . -c """
import os
import sys
PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH,"sonnen_api_v2"
)
sys.path.append(SOURCE_PATH)
