# Copyright (c) by it's authors. 
# Some rights reserved. See LICENSE, AUTHORS.

from ..services.invoiceGenerator import *
from wallaby.common.document import *

import wallaby.backends.couchdb as couchdb

def run(appPath, options):
    if options.db == None and not options.fx:
        print "The --db options is required!"
        from twisted.internet import reactor
        reactor.stop()
        return

    if options.fx:
        options.db = "crm"
        options.server = "https://relax.freshx.de"
        options.couchPort = "443"

    couchdb.Database.setURLForDatabase(options.db, options.server + ":" + options.couchPort)
    
    if options.username is not None and options.password is not None:
        couchdb.Database.setLoginForDatabase(options.db, options.username, options.password)
    
    invoiceGeneratorConfig = Document(data={'databaseName':options.db,'templateFile':os.path.join(appPath, "invoices", "template.tex"),'senderDocID':'company'})

    invoiceGeneratorConfig.set('flag.key', 'generateInvoicePDF')
    invoiceGeneratorConfig.set('flag.generate', 'generate')
    invoiceGeneratorConfig.set('flag.inProgress', 'inProgress')
    invoiceGeneratorConfig.set('flag.error', 'error')
    invoiceGeneratorConfig.set('flag.success', 'success')
    invoiceGeneratorConfig.set('view.inProgress', '_design/couchapp/_view/invoiceGenerationInProgress')
    invoiceGeneratorConfig.set('view.pending', '_design/couchapp/_view/pendingInvoiceGeneration')

    invoiceGenerator = InvoiceGenerator(invoiceGeneratorConfig)
    
    from twisted.internet import reactor
    reactor.callLater(0, couchdb.Database.getDatabase(options.db).changes)
    reactor.callLater(0, invoiceGenerator.initialize)
