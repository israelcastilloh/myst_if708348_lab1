
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Lab 1                                                                                      -- #
# -- script: main.py : python script with the main functionality                                         -- #
# -- author: israecastilloh                                                                              -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/israelcastilloh/myst_if708348_lab1                                                                    -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import pandas as pd
import numpy as np
from functions import file_walker, read_csv, calculate_returns


files_list = file_walker()
calculate_returns()
