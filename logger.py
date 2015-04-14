# -*- coding: utf-8 -*-
#!/usr/bin/env python
#

import logging
import os


logger = logging.getLogger("htemp")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler(os.path.join(os.path.dirname(__file__), "htemp.log"))
handler.setFormatter(formatter)
logger.addHandler(handler)
