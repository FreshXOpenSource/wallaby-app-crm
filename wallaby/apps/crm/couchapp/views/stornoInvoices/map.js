function(doc) {
  if(doc.type == 'INVOICE' && (doc._id.indexOf('STORNO') != -1 || doc.status == '6' || doc.status == '30')) emit(null, doc);
}
