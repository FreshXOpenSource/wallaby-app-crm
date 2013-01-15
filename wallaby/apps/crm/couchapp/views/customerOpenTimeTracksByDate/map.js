function(doc) {
  if (doc.type == "timeTrack" && doc.status == "open"){
    if(doc.customerID != ""){
        if(doc.issueDescription && doc.issueDescription.length > 0) emit([doc.customerID, doc.updatedOn], { "updatedOn": doc.updatedOn, "description": doc.issueDescription, "hours": doc.hours })
        else if(doc.projectDescription && doc.porjectDescription.length > 0) emit([doc.customerID, doc.updatedOn], { "updatedOn": doc.updatedOn, "description": doc.projectDescription, "hours": doc.hours })
        else emit([doc.customerID, doc.updatedOn], { "updatedOn": doc.updatedOn, "description": doc.projectName, "hours": doc.hours })
    }
  }
}
