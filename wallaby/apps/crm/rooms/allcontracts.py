# Copyright (c) by it's authors. 
# Some rights reserved. See LICENSE, AUTHORS.

# -*- coding: UTF-8 -*-

from wallaby.pf.room import *
from wallaby.backends.couchdb import *
from wallaby.plugins.couchdb.document import *

from twisted.internet import defer
from datetime import date

class Allcontracts(Room):
    def __init__(self, name):
        Room.__init__(self, name)
        self.catch('Custom.In.CreateDueInvoices', self._createDueInvoices)

    @defer.inlineCallbacks
    def _createDueInvoices(self, action, payload):
        print "Create Due invoices"

        today = date.today()

        db = Database.getDatabase(None)

        try:
            rows = yield db.view('_design/couchapp/_view/allDueContracts', endkey=[[today.year, today.month, today.day], {}], inclusive_end=True)
    
            for row in rows:
                doc = CouchdbDocument(data=row['value'])
                newDoc = doc.clone()
                newDoc.resetDocumentID()
                newDoc.set('status', 'OPEN')
    
                nextInvoice = doc.get('contract.nextInvoice')
                y, m, d = nextInvoice[0], nextInvoice[1], nextInvoice[2]
    
                if doc.get('interval')[0] == 'M':
                    m = m + 1
                elif doc.get('interval')[0] == 'Q':
                    m = m + 3
                elif doc.get('interval')[0] == 'J':
                    y = y + 1

                if m > 12:
                    m = m - 12
                    y = y + 1

                newDoc.set('workPeriod.fromDate', doc.get('contract.nextInvoice'))
                doc.set('contract.nextInvoice', [y, m, d])
                newDoc.set('workPeriod.toDate', doc.get('contract.nextInvoice'))
    
                yield db.save(doc._data)
                yield db.save(newDoc._data)
        except Exception as e:
            print "allcontractsContext EXCEPTION", e


