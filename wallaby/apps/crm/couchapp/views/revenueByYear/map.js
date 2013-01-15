function(doc) {
  if(doc.type == 'INVOICE' && doc.status == 'PAID') 
  {
    year  = doc.invoiceDate[0];
    month = doc.invoiceDate[1];
    name  = doc.customer.name;
    value = parseFloat(doc.brutto);

    emit([year, month, name], value);
  }
}
