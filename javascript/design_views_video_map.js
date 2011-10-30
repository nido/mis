function(doc) {
  if(doc.ffprobe.tags.title){
    emit(doc.ffprobe.tags.title);
  } else if(doc.ffprobe.container.filename) {
    emit(doc.ffprobe.container.filename);
  } else {
    emit(doc.paths[0].path)
  }
}
