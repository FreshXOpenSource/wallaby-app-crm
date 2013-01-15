function(doc) {
  if(doc.type == 'timeTrack' && doc.status == 'open') 
  {
    idescr = '-';
    pdescr = '-';
    if(doc.issueDescription && doc.issueDescription.length > 0) idescr = doc.issueDescription;
    
    if(doc.projectDescription && doc.projectDescription.length > 0) pdescr = doc.projectDescription;
    else pdescr = doc.projectName;

    year  = doc.updatedOn[0];
    month = doc.updatedOn[1];
    value = parseFloat(doc.hours);

    if(doc.customerID == '' || doc.customerID == "56672101214e44388e4691e69694196b")
        emit(["Intern", doc.customerID, pdescr, year, month, idescr], value);
    else
        emit(["Extern", doc.customerID, pdescr, year, month, idescr], value);
  }
}
