function(doc) {
  if(doc.type == 'INVOICE' && doc.status == 'CONTRACT' && doc.contract && doc.contract.nextInvoice)
  {
    emit([doc.contract.nextInvoice, doc.customerID], {
        'nextInvoice': doc.contract.nextInvoice,
        'interval': doc.interval,
        'title': doc.title,
        'customerID': doc.customerID,
        'netto': doc.netto,
        'vat': doc.vat,
        'brutto': doc.brutto
    });
  }
}
