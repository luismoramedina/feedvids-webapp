HOWTO:

Install deps in heroku client environment:
sudo easy_install paste webapp2 webob pymongo

Mongodb:

    mongodb://heroku_app22042562:q3j2h6h3sdmrqafuja24e4n774@ds033079.mongolab.com:33079/heroku_app22042562
    mongodb://heroku_app22042562_A:<dbpassword>@ds033079.mongolab.com:33079/heroku_app22042562

_______________

TODO:

- Subir a PRO la llamada a la función:
    function changeTitle(videoTitle) {
        document.title = videoTitle + ' - Feedvids';
    }

- Llamar a gdata.yt con un id de app para que no se sobrepase el limite gratuito

_______________

A video item:

{
    "item_id": "401650016",
    "resolved_id": "401650016",
    "given_url": "http://www.youtube.com/watch?v=kzMk2wrEUu8",
    "given_title": "http://www.youtube.com/watch?v=kzMk2wrEUu8",
    "favorite": "0",
    "status": "0",
    "time_added": "1374745006",
    "time_updated": "1374745006",
    "time_read": "0",
    "time_favorited": "0",
    "sort_id": 112,
    "resolved_title": "Mondo Cane / Mike Patton (Documental) 7MO Vicio",
    "resolved_url": "http://www.youtube.com/watch?v=kzMk2wrEUu8",
    "excerpt": "http://www.fnm4ever.com/ Este es un documental realizado por el programa 7MO Vicio, emitido por el canal chileno de cable Via X. Definido como un experimento...",
    "is_article": "0",
    "is_index": "0",
    "has_video": "2",
    "has_image": "1",
    "word_count": "0"
}
