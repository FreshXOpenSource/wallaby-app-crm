# Copyright (c) by it's authors. 
# Some rights reserved. See LICENSE, AUTHORS.

from wallaby.pf.room import *

import wallaby.backends.couchdb as couchdb
from wallaby.plugins.couchdb.document import *
from wallaby.pf.peer.database import *
from wallaby.pf.peer.viewer import *
from wallaby.pf.peer.multiViewer import *
from wallaby.pf.peer.editDocument import *
from wallaby.pf.peer.documentChanger import *

from datetime import date

import re

class Tickets(Room):
    Receiving = [
        Viewer.In.Document,
        'Custom.In.CreateInvoicePos',
        'Custom.In.CreateSingleInvoicePos',
        MultiViewer.Out.MultiSelect 
    ]

    Sending = [
        Database.In.SaveDocument,
        DocumentChanger.In.InsertRow
    ]

    def __init__(self, name):
        Room.__init__(self, name)

        self._couchdb = couchdb.Database.getDatabase(None)

        self._doc = None
        self._invoiceDoc = None
        self._multi = None
        self._state = None

    def customPeers(self):
        self._invoiceRoom = House.get('INVOICE')

        self.catch(MultiViewer.Out.MultiSelect, self._multiSelect)
        self.catch('Custom.In.CreateInvoicePos', self._createInvoicePos)
        self.catch('Custom.In.CreateSingleInvoicePos', self._createInvoicePos)
        self.catch(Viewer.In.Document, self._document)
        self._invoiceRoom.catch(Viewer.In.Document, self._invoiceDocument)
        self._invoiceRoom.catch(EditDocument.Out.State, self._docState)

    def _multiSelect(self, action, selection):
        print "select multi", selection
        if selection != None and len(selection) > 0:
            self._multi = selection
        else:
            self._multi = None

    def _docState(self, action, state):
        self._state = state

    @defer.inlineCallbacks
    def _createInvoicePos(self, action, payload):
        if action == 'Custom.In.CreateSingleInvoicePos':
            single = True
        else:
            single = False

        if self._invoiceDoc == None or not self._state:
            return

        if not self._state in ('Edit', 'New', 'Dirty', 'View'):
            return

        ids = self._multi

        if not ids:
            ids = []

        if self._doc != None:
            if self._doc.documentID not in ids:
                ids.append(self._doc.documentID)

        newdoc = self._invoiceDoc.clone()

        articles = newdoc.get('articles')
        if articles == None: articles = []
        
        newArticles = []

        allFromDate = None
        allToDate   = None

        for id in ids:
            doc = yield self._couchdb.get(id)
            if not doc: continue

            doc = CouchdbDocument(data=doc)

            issueDescription = doc.get('issueDescription')

            if issueDescription == None: issueDescription = ''
            else: issueDescription = re.sub(r'[\r\n]', '', issueDescription) + "\n"

            tracks = doc.get('tracks')

            fromDate = None
            toDate   = None

            if tracks != None:
                for key, t in tracks.items():
                    desc    = t['comment']
                    spentOn = t['spentOn'] 

                    d = date(*spentOn)

                    if not fromDate or d < fromDate: fromDate = d
                    if not toDate or d > toDate: toDate = d
                    if not allFromDate or d < allFromDate: allFromDate = d
                    if not allToDate or d > allToDate: allToDate = d

                    if desc != None and len(desc) > 0: issueDescription += ' - ' + desc + "\n"

            hours = float(doc.get('hours'))

            article = {
                "count": hours,
                "description": issueDescription,
                "price": 100.0,
                "unit": "Stunde(n)",
                "total": hours * 100.0,
                "fromDate": [fromDate.year, fromDate.month, fromDate.day],
                "toDate": [toDate.year, toDate.month, toDate.day]
            }

            if not single and self._state in ('Edit', 'New', 'Dirty'):
                self._invoiceContext.throw(DocumentChanger.In.InsertRow, ("articles", article) )
            else:
                newArticles.append(article)

            doc.set('status', 'booked')
            yield self._couchdb.save(doc._data)

        if single: 
            article = {
                "count": 0.0,
                "description": "",
                "price": 100.0,
                "unit": "Stunde(n)",
                "total": 0.0,
                "fromDate": [allFromDate.year, allFromDate.month, allFromDate.day],
                "toDate": [allToDate.year, allToDate.month, allToDate.day]
            }

            for a in newArticles:
                article["count"] += float(a["count"])
                article["description"] += a["description"]

            article["total"] = float(article["count"]) * float(article["price"])

            newArticles = [article]

            if self._state in ('Edit', 'New', 'Dirty'):
                self._invoiceContext.throw(DocumentChanger.In.InsertRow, ("articles", article) )

        if self._state in ('Edit', 'New', 'Dirty'):
            return

        for a in newArticles:
            articles.append(a)

        total    = 0.0
        fromDate = None
        toDate   = None

        for a in articles:
            d1 = d2 = None
            if "fromDate" in a: d1 = date(*a["fromDate"])
            if "toDate" in a:   d2 = date(*a["toDate"])

            if d1 and (not fromDate or d1 < fromDate): fromDate = d1
            if d2 and (not toDate or d2 > toDate): toDate = d2

            total += float(a['total'])

        vat = total * 0.19

        if fromDate: newdoc.set('workPeriod.fromDate', [fromDate.year, fromDate.month, fromDate.day])
        if toDate:   newdoc.set('workPeriod.toDate', [toDate.year, toDate.month, toDate.day])
        newdoc.set('vat', vat)
        newdoc.set('vat', vat)
        newdoc.set('netto', total)
        newdoc.set('brutto', total + vat)
        newdoc.set('articles', articles)

        self._invoiceContext.throw(Database.In.SaveDocument, (newdoc, None))

    def _document(self, action, doc):
        self._doc = doc

    def _invoiceDocument(self, action, doc):
        self._invoiceDoc = doc
