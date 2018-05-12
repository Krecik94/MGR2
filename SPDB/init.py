import osmapi
import urllib.request

api = osmapi.OsmApi()
#print(api.NotesSearch(123))
nodeToSearch = "node[\"name:en\"=\"Warsaw\"];out;"
contents = urllib.request.urlopen("http://overpass-api.de/api/interpreter?data=" + nodeToSearch).read()

print(contents)