function(doc) {
  if(doc.customerID && doc.type == 'INVOICE' && doc.status == 'OPEN') 
  {
    emit([doc.customerID, doc.invoiceNumber], {
        'title': doc.title,
        'customerID': doc.customerID,
        'netto': doc.netto,
        'vat': doc.vat,
        'brutto': doc.brutto
    });
  }
}
