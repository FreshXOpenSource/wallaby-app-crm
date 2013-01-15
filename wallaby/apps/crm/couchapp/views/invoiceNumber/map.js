function(doc) {
  if(doc.invoiceDate && doc.type == 'INVOICE')
  { 
    lst = doc.invoiceDate;
    // lst = new Array(lst[0], lst[1], lst[2]);
    if(doc.increment)
    {
      inc = doc.increment;
    }else
    {
      inc = 1;
    }
    emit(lst, inc);
  }
}
