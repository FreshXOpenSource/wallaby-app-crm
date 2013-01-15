#!/usr/bin/env python
# Copyright (c) by it's authors. 
# Some rights reserved. See LICENSE, AUTHORS.


from wallaby.qt_combat import *

from UI_mainWindow import Ui_MainWindow

from wallaby.pf.room import *
from wallaby.frontends.qt.baseWindow import *

import wallaby.backends.couchdb as couchdb
import wallaby.backends.elasticsearch as es

class MainWindow(BaseWindow, Ui_MainWindow):
    def __init__(self, quitCB, options):
        db = "crm"
        if options:
            db = options.app 
            if options.db is not None: db = options.db

        BaseWindow.__init__(self, "wallaby", "wallycrm", options, quitCB, dbName=db)

        # set up User Interface (widgets, layout...)
        self.setupUi(self)

        House.get("COIVIEW")
        House.get("CCVIEW")
        House.get("ORDVIEW")
        House.get("CIVIEW")
        House.get("ISVIEW")
        House.get("AIVIEW")
        House.get("OPENTRACKSVIEW")
        House.get("ARTICLEINVOICES")
        House.get("REVENUEVIEW")

    def setConnectionSettings(self, options):
        if options and options.fx:
            options.server = "https://relax.freshx.de"
            options.couchPort = "443"
            options.esPort = "443/es"

        couch.Database.setURLForDatabase(self.dbName(), options.server + ":" + options.couchPort)
        es.Connection.setURLForIndex(None, options.server + ':' + options.esPort)

        if options and options.username != None and options.password != None:
            es.Connection.setLoginForIndex(None, options.username, options.password)

    def _credentialsArrived(self, action, payload):
        House.throw("CUSTOMERSEARCH:SearchDocument.In.Search")
        House.throw("ARTICLESEARCH:SearchDocument.In.Search")
        House.throw("OPENINVOICES:MultiViewer.In.Refresh")
        # House.throw("TICKETS:MultiViewer.In.Refresh")
        House.throw("ALLINVOICEJOURNAL:MultiViewer.In.Refresh")
        House.throw("ALLCONTRACTS:MultiViewer.In.Refresh")
        # House.throw("REVENUE:MultiViewer.In.Refresh")
        # House.throw("REDMINE:ViewDocumentFromDatabase.In.Load", "projects")
