function(doc) {
  if(doc.type == "INVOICE" && doc.articles && doc.customerID != 'CAOCUSTOMER')
  { 
    var emitted = {};	
    for(i=0; i<doc.articles.length; i++)
    {
      item = doc.articles[i];
      if(item._id && !(item._id in emitted) && doc.status != 'OPEN' && doc.status != 'CONTRACT')
      {
        emitted[item._id] = true;
        emit([item._id, doc.invoiceDate], {
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
  }
}
