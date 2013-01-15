function(doc){
  if(doc.type == "redmineConfig"){
    emit(doc.type, doc);
  }
}
