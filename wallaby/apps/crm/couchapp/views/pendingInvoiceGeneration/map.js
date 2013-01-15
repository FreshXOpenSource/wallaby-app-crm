function(doc) {
  if(doc.customerID && doc.type == 'INVOICE' && doc.generateInvoicePDF == 'generate') 
    emit([doc.customerID, doc.invoiceDate, doc.invoiceNumber], doc.customerID);
}
