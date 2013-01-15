function(doc) {

  if (doc.type == "timeTrack" && doc.status == "open"){
    
    if (doc.issueID == null){
      emit(["PID"+doc.projectID], doc);
    }
    else{
      emit(["IID"+doc.issueID],doc);
    }
  }
}
