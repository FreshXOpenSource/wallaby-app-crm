function(doc) {
  if(doc.type == 'INVOICE' && doc.status == 'CONTRACT' && doc.contract && doc.contract.nextInvoice)
  {
    emit([doc.contract.nextInvoice, doc.customerID], doc)
  }
}
