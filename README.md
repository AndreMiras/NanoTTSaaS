# NanoTTS SaaS service

Online Text To Speech service: https://nanottsaas.herokuapp.com/

Built with [NanoTTS](https://github.com/gmn/nanotts) and [Flask](https://github.com/pallets/flask) and running on Heroku.

## Online user interface
Play with the service online using a web browser.

https://nanottsaas.herokuapp.com/

## Remote API
Use the API from the command line.
```bash
# Using cURL and aplay
$ curl --data "text=from the terminal" https://nanottsaas.herokuapp.com/api | aplay

# Passing parameters e.g. voice
$ curl --data "text=depuis le terminal" --data "voice=fr-FR" https://nanottsaas.herokuapp.com/api | aplay

# Passing more parameters e.g. speed and pitch
$ curl --data "text=from the terminal" --data "speed=0.8" --data "pitch=1.5" https://nanottsaas.herokuapp.com/api | aplay
```
