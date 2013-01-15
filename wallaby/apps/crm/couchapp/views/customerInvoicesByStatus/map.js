function(doc) {
  if(doc.customerID && doc.type == 'INVOICE' && doc.status != 'CONTRACT' && doc.status != 'OPEN') 
  {
    emit([doc.customerID, doc.status, doc.invoiceDate, doc.invoiceNumber], {
        'invoiceNumber': doc.invoiceNumber,
        'invoiceDate': doc.invoiceDate,
        'title': doc.title,
        'customerID': doc.customerID,
        'status': doc.status,
        'netto': doc.netto,
        'vat': doc.vat,
        'brutto': doc.brutto
    });
  }
}
