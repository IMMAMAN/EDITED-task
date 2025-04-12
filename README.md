# EDITED-task
### This Flask application provides a service for crawling websites, taking screenshots of pages, and storeing them for later retrieval. The app is can be run inside the docker container.


## Endpoints
* Health check endpoint `GET` `/isalive`
* Screenshot endpoint `POST` `/screenshots/>`
* Screenshot retrieval `GET` `/screenshots/<id>`


## Docker instructions
### To start the service using docker follow the instructions below

```
docker build -t edited-task .
```
----
```
docker run -p 5000:5000 edited-task
```

## API instructions
```bash
curl http://localhost:5000/isalive
```
Should return `{"status":"OK"}`

---

```
curl -X POST http://localhost:5000/screenshots/ \
  -H "Content-Type: application/json" \
  -d '{"start_url": "https://edited.com", "num_links": 3}'
```
Should return `{"id":<uuid>}`

---
Using the uuid from the above api response

```
curl http://localhost:5000/screenshots/<uuid> -o zipfile
```
should download a .zip file with filename zipfile

---