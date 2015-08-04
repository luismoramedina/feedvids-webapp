me queda probar que se puede poner el receiver en una ruta local lan
hay que copiar el receiver al dropbox

foreman start -e local.env

run client -> http://localhost:8080/feedvids-cast-sender.html
    messages:
        {"command":"load", "data": ["a_426RiwST8"]}

debug server -> http://192.168.0.205:9222
view server -> http://dl.dropboxusercontent.com/u/1368598/receiver.html
get vids -> http://localhost:5000/pocket-json-list?list=yes

Pro:
http://feedvids.herokuapp.com/pocket-playlist

