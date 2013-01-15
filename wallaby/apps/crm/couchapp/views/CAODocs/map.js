function(doc) {
    if(doc.type == 'INVOICE' || doc.type == 'ARTICLE' || doc.type == 'CUSTOMER' || doc._id.slice(0, 3) == "CAO") emit(doc._id, doc);
}
