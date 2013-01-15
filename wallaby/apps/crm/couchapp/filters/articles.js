function(doc, req) {
  if(doc.type == 'ARTICLE' || doc._deleted) {
      return true;
  } else {
      return false;
  }  
}
