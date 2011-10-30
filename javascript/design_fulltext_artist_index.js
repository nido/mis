function(doc) {
  var ret=new Document();
  ret.add(doc.ffprobe.tags.artist);
  return ret;
}
