for i in {0..10}
  do
  	let i=i*10000
  	let j=i+9999
     echo "$i to $j"
     curl 'http://localhost:8983/solr/resumes/dataimport?optimize=false&indent=true&clean=true&commit=true&verbose=false&command=full-import&debug=false&wt=json&minrun='$i'&maxrun='$j''
done