"""
Octogon Panel Constants
"""
import os

cwd = os.getcwd()

# location of .scss files
STYLE_PATH = os.path.join(cwd, "style/")

# location of jinja2 templates
TEMPLATE_PATH = os.path.join(cwd, "templates/")

# location of scoreboard data
# SB_DATA_PATH = "output/sb_data.json"
SB_DATA_PATH = os.path.join(cwd, "output/sb_data_new.json")
