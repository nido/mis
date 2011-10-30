function(doc) {
  if(doc.ffprobe.tags.title){
    if(doc.ffprobe.tags.artist){
      emit(doc.ffprobe.tags.artist, doc.ffprobe.tags.title);
    } else {
      emit(null, doc.ffprobe.tags.title);
    }
  } else if(doc.ffprobe.container.filename) {
    if(doc.ffprobe.tags.artist){
      emit(doc.ffprobe.tags.artist,
doc.ffprobe.container.filename);
    } else {
      emit(null, doc.ffprobe.container.filename);
    }
  } else if (doc.paths[0].path){
    if(doc.ffprobe.tags.artist){
      emit(doc.ffprobe.tags.artist, doc.paths[0].path)
    } else {
      emit(null, doc.paths[0].path)
    }
  }
}
