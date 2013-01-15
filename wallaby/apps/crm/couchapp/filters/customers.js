function(doc, req) {
  if(doc.type == 'CUSTOMER' || doc._deleted) {
      return true;
  } else {
      return false;
  }  
}
