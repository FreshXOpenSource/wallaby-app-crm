function(doc) {
  if(doc.type == 'CUSTOMER') emit(null, doc);
}
