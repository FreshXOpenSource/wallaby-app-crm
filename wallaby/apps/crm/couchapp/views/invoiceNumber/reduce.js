function(keys, values, rereduce) {
  var max = 0;
  for( i in values ) {
    log("" + values[i] + "");
    if (values[i] > max) {
      max = values[i];
    }
  }
 
  return max;
}
