function(doc) {
  if(doc.ffprobe.container.format_name){
    emit(doc.ffprobe.container.format_name, 1);
  }
}
