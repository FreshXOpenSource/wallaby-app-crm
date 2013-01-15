function(doc) {
  if(doc.customerID && doc.type == 'INVOICE' && doc.generateInvoicePDF == 'error') 
    emit([doc.customerID, doc.invoiceDate, doc.invoiceNumber], doc.invoiceGeneratorError);
}
