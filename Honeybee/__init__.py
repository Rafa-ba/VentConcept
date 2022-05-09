"""Honeybee core library."""
import importlib
import pkgutil
from honeybee.logutil import get_logger

import honeybee_energy
import honeybee_standards

# logger = get_logger(__name__)

# #  find and import honeybee extensions
# #  this is a critical step to add additional functionalities to honeybee core library.
# extensions = {}
# for finder, name, ispkg in pkgutil.iter_modules():
#     if not name.startswith('honeybee_') or name.count('_') > 1:
#         continue
#     try:

#         #extensions[name] = importlib.import_module(name)
#         print(extensions[name], name, "THHHHHHHHHHHHHHIS IS IMPORTANT MAUS")
#     except Exception:
#         logger.exception('Failed to import {0}!'.format(name))
#     else:
#         logger.info('Successfully imported Honeybee plugin: {}'.format(name))
