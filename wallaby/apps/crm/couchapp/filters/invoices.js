function(doc, req) {
  if((doc.type == 'INVOICE' && doc.status != 'CONTRACT' && doc.status != 'OPEN') || doc._deleted) {
      return true;
  } else {
      return false;
  }  
}
