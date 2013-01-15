function(doc, req) {
  if(doc.type == 'ARTICLE' || doc.type == 'CUSTOMER' || doc.type == 'INVOICE' || doc._deleted) {
      return true;
  } else {
      return false;
  }  
}
