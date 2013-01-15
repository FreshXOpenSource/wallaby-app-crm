function(doc) {
  if(doc.type == 'INVOICE' && doc.status != 'CONTRACT' && doc.status != 'OPEN') 
    emit([doc.status], {
        'invoiceNumber': doc.invoiceNumber,
        'invoiceDate': doc.invoiceDate,
        'title': doc.title,
        'customerID': doc.customerID,
        'status': doc.status,
        'netto': doc.netto,
        'vat': doc.vat,
        'brutto': doc.brutto
    })
}
