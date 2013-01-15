function(doc) {
  if(doc.type == 'INVOICE') emit(null, doc);
}
