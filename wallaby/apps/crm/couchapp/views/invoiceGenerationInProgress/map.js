function(doc) {
  if(doc.customerID && doc.type == 'INVOICE' && doc.generateInvoicePDF == 'inProgress') 
    emit([doc.customerID, doc.invoiceDate, doc.invoiceNumber], doc.customerID);
}
