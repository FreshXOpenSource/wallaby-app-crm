# Copyright (c) by it's authors. 
# Some rights reserved. See LICENSE, AUTHORS.

from wallaby.common.abstractService import AbstractService
from wallaby.backends.couchdb import *
from wallaby.plugins.pdfgenerator import *
from twisted.internet import defer

class InvoiceGenerator(AbstractService):
    def __init__(self, config):
        AbstractService.__init__(self, config)
        self._limit = 10
        self._processing = 0

    @defer.inlineCallbacks
    def initialize(self):
        print "Initializing invoice generator"
        self._database = Database.getDatabase(self._config.get('databaseName'))
        self._pdfGenerator = PDFGenerator(self._config.get('templateFile'))
        self._flagKey = self._config.get('flag.key')
        self._flagGenerate = self._config.get('flag.generate')
        self._flagInProgress = self._config.get('flag.inProgress')
        self._flagError = self._config.get('flag.error')
        self._flagSuccess = self._config.get('flag.success')

        try:
            self._sender = yield self._database.get(self._config.get('senderDocID'))
            #reset invoice which are stuck in inProgress state to generate state
            inProgress = yield self._database.view(self._config.get('view.inProgress'))
            for p in inProgress:
                self._resetInProgress(p['id'])
            print "Triggered reset of "+str(len(inProgress))+" invoices: inProgress->generate"

            #generate pdfs for all invoices in generate state
            pending = yield self._database.view(self._config.get('view.pending'))
            print "pending", pending
            for p in pending:
                self._dbChanged(p)
            print "Triggered creation of "+str(len(pending))+" invoice pdfs"

            self._database.changes(self._dbChanged)
            print "Listening for changes"
        except Exception as e:
            print "invoiceGenerator.py: initialize", e

    @defer.inlineCallbacks
    def _resetInProgress(self, id):
        self._processing += 1
        if self._processing > self._limit:
            self._processing -= 1
            from twisted.internet import reactor
            reactor.callLater(1, self._resetInProgress, id)
            return

        doc = yield self._database.get(id)
        doc[self._flagKey] = self._flagGenerate
        self._database.save(doc)

        self._processing -= 1


    @defer.inlineCallbacks
    def _dbChanged(self, changes, viewID=None):
        if changes == None: return

        self._processing += 1
        if self._processing > self._limit:
            self._processing -= 1
            from twisted.internet import reactor
            reactor.callLater(1, self._dbChanged, changes)
            return

        if 'id' in changes:
            doc = yield self._database.get(changes['id'])

            if doc and self._flagKey in doc and doc[self._flagKey] == self._flagGenerate:
                doc[self._flagKey] = self._flagInProgress
                response = yield self._database.save(doc)
                doc['_rev'] = response['rev']

                try:
                    pdf = yield self._pdfGenerator.generatePDF({'invoice':doc, 'sender':self._sender, 'print':True})

                    response =  yield self._database.put_attachment(doc, 'invoice.pdf', pdf, contentType='application/pdf')

                    if 'ok' in response and response['ok'] == True:
                        doc = yield self._database.get(changes['id'])

                        if doc != None:
                       	    doc[self._flagKey] = self._flagSuccess
                            if 'invoiceGeneratorError' in doc:
                                del doc['invoiceGeneratorError']
                            response = yield self._database.save(doc)

                            print "generated invoice for", changes['id']
                except LatexError as e:
                    doc['invoiceGeneratorError'] = e._error
                    doc[self._flagKey] = self._flagError
                    response = yield self._database.save(doc)

        self._processing -= 1
