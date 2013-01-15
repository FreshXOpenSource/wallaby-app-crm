class Options:
    def __init__(self):
        self.server = "127.0.0.1"
        self.app = "crm"
        self.db = "crm"
        self.password = self.username = None
        self.fx = True
        self.debug = ""

import warnings
warnings.simplefilter('ignore')

import wallaby.apps.wallabyApp
wallaby.apps.wallabyApp.WallabyApp("crm", options=Options())
