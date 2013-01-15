# Copyright (c) by it's authors. 
# Some rights reserved. See LICENSE, AUTHORS.

from wallaby.pf.room import *

import wallaby.backends.couchdb as couchdb

from wallaby.pf.peer.multiViewer import *
from wallaby.pf.peer.tab import *
from wallaby.pf.peer.editDocument import *

from twisted.internet import defer

class Search(Room):
    def __init__(self, name):
        Room.__init__(self, name)

        self._queryResult = None
        self._row = None
        self._documentID = None

    def customPeers(self):
        self.catch(MultiViewer.In.Data, self._resultChanged)
        self.catch("MultiViewer.Out.Select", self._select)
        self.catch("Search.In.Load", self._load)

    def _select(self, pillow, feathers):
        self._documentID, _, self._row = feathers
    
    @defer.inlineCallbacks
    def _load(self, pillow, feathers):
        if not self._queryResult or not self._documentID: return

        type = yield self._queryResult.deferredGetValue(self._row, "_source.type")

        if type == "CUSTOMER":
            self.throw("CUSTOMER:" + EditDocument.In.Load, self._documentID)
            self.throw("DEFAULT:" + Tab.In.Select, "main.1")

        elif type == "INVOICE":
            customerID = yield self._queryResult.deferredGetValue(self._row, "_source.customerID")
            status = yield self._queryResult.deferredGetValue(self._row, "_source.status")

            self.throw("CUSTOMER:" + EditDocument.In.Load, customerID)
            self.throw("DEFAULT:" + Tab.In.Select, "main.1")

            if status == "OPEN":
                yield House.get("INVOICE").catchNow(EditDocument.In.Load)
                self.throw("INVOICE:" + EditDocument.In.Load, self._documentID)
                self.throw("INVOICE:" + MultiViewer.In.SelectID, self._documentID)
                self.throw("CUSTOMER:" + Tab.In.Select, "customer.0")

            elif status == "CONTRACT":
                yield House.get("CONTRACT").catchNow(EditDocument.In.Load)
                self.throw("CONTRACT:" + EditDocument.In.Load, self._documentID)
                self.throw("CONTRACT:" + MultiViewer.In.SelectID, self._documentID)
                self.throw("CUSTOMER:" + Tab.In.Select, "customer.2")

            else:
                yield House.get("INVOICEJOURNAL").catchNow(EditDocument.In.Load)
                self.throw("INVOICEJOURNAL:" + EditDocument.In.Load, self._documentID)
                self.throw("INVOICEJOURNAL:" + MultiViewer.In.SelectID, self._documentID)
                self.throw("CUSTOMER:" + Tab.In.Select, "customer.1")

        elif type == "ARTICLE":
            self.throw("ARTICLE:" + EditDocument.In.Load, self._documentID)
            self.throw("DEFAULT:" + Tab.In.Select, "main.2")

    def _resultChanged(self, pillow, qr):
        if qr.identifier() == "SEARCH":
            self._queryResult = qr
        
