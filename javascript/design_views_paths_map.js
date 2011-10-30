function(doc){
  for(i=0; i<doc.paths.length; i++){
      entry = doc.paths[i]
      key = [entry.node, entry.path]
      if(entry.node && entry.path){
        emit(key, doc._id)
      }
  }
}
