# Copyright (c) by it's authors. 
# Some rights reserved. See LICENSE, AUTHORS.

from wallaby.pf.room import *

from wallaby.pf.peer.documentChanger import *
import wallaby.backends.couchdb as couchdb

from datetime import date

from wallaby.pf.peer.documentCache import *
from twisted.internet import defer

class Customer(Room):
    def __init__(self, name):
        Room.__init__(self, name)

        DocumentChanger.registerToken("EMBEDCUSTOMER", self._embedCustomer)
        DocumentChanger.registerToken("CUSTOMERNUMBER", self._customerNumber)
        DocumentChanger.registerToken("INVOICENUMBER", self._invoiceNumber)

        self._couchdb = couchdb.Database.getDatabase(None)

        self._deferredDocs = {}

    def customPeers(self):
        self.catch(DocumentCache.Out.RequestedDocument, self._requestedDocument)
        pass

    def _requestedDocument(self, action, doc):
        if doc == None or doc.documentID not in self._deferredDocs:
            return

        self._deferredDocs[doc.documentID].callback(doc)
        del self._deferredDocs[doc.documentID]

    @defer.inlineCallbacks
    def _invoiceNumber(self, invoice):
        if invoice != None:
            oldNumber = invoice.get('invoiceNumber')
            if oldNumber != None and len(oldNumber) > 0 and oldNumber != '-': 
                defer.returnValue(oldNumber)
                return

        try:
            numbers = yield self._couchdb.get('numbers')
            number = unicode(numbers['invoiceNumber'])
            year, month, day, inc = number[0:4], number[4:6], number[6:8], number[9:]
            today = date.today()
            y, m, d = today.year, today.month, today.day
            y = "%04d" % y
            m = "%02d" % m
            d = "%02d" % d

            if y==year and month==m and day==d:
                inc = str(int(inc) + 1)
            else:
                inc = "1"

            number = y + m + d + "-" + inc
            numbers['invoiceNumber'] = number
            yield self._couchdb.save(numbers)
            defer.returnValue(number)
        except Exception as e:
            print "customerContext.py: _invoiceNumber", e

    @defer.inlineCallbacks
    def _customerNumber(self, customer):
        try:
            numbers = yield self._couchdb.get('numbers')
            number = str(int(numbers['customerNumber']) + 1)
            numbers['customerNumber'] = number
            yield self._couchdb.save(numbers)
            defer.returnValue(number)
        except Exception as e:
            print "customerContext.py: _customerNumber", e

    @defer.inlineCallbacks
    def _embedCustomer(self, article):
        customerID = article.get('customerID')

        if customerID == None:
            defer.returnValue('null')
            return
    
        if customerID not in self._deferredDocs:
            self._deferredDocs[customerID] = defer.Deferred()

        self.throw(DocumentCache.In.RequestDocument, customerID)

        doc = yield self._deferredDocs[customerID]

        if doc != None:
            defer.returnValue({
                "name": doc.get('name'),
                "name2": doc.get('name2'),
                "street": doc.get('street'),
                "zip": doc.get('zip'),
                "city": doc.get('city'),
                "customerNumber": doc.get('customerNumber')
            })
        else:
            defer.returnValue('null')
