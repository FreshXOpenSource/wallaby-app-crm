function(doc) {
  if(doc.customerID && doc.type == 'INVOICE' && doc.status == 'CONTRACT') 
  {
      if(doc.contract)
          nextInvoice = doc.contract.nextInvoice;
      else
          nextInvoice = [2099, 1, 1];

    emit([doc.customerID, doc.invoiceNumber], {
        "title": doc.title,
        "interval": doc.interval,
        "nextInvoice": nextInvoice
    });
  }
}
