[![Flask tests](https://github.com/healeycodes/pi/actions/workflows/python-app.yml/badge.svg)](https://github.com/healeycodes/pi/actions/workflows/python-app.yml)

# :pie: pi dashboard

> My blog post: [Listening to Satellites with my Raspberry Pi](https://healeycodes.com/listening-to-satellites-with-my-raspberry-pi/)

<br>

This is the monorepo for my Raspberry Pi dashboard!

It includes: a module system allows different features to be toggled on and off so you don't need my exact hardware setup. It also allows multiple Pis to use the same server.

- :house: a Windows 98 themed dashboard.
- :satellite: view the list of visible GPS satellites from a GPS hardware device.
- :printer: receive printer messages to a POS58 compatible printer.
- :thermometer: live temperature/humidity collected from an AMxx compatible sensor.

<br>

![The dashboard home page with weather, printer, and sky modules enabled.](https://github.com/healeycodes/pi/blob/main/client/preview.png)

<br>

## Run

#### Server

Toggle server modules in `server/config.py`.

1. Create a Heroku project.

2. Add a PostgreSQL database via the GUI.

3. Add a config var of `PW` via GUI.

4. Deploy from this GitHub repository.

That's it. No migrations or other setup required.

<br>

For local development:

```bash
pip install -r requirements.txt
export FLASK_APP=wsgi:app ;python3.9 -m flask run
```

A SQLite database is automatically created and used instead of PostgreSQL. If no `PW` environment variable is provided, no password is required for client requests.

#### Client

The client is written with a Raspberry Pi in mind and has been tested with the latest Raspbian (v10) and the bundled Python 3 that comes with it.

Depending on what modules you've enabled in `client/clientconfig.py` you may need hardware connected and setup e.g. to use the sky module, your GPS device must be communicating with `gpsd`.

```
cd client/
pip install -r requirements.txt
sudo python3 poller.py https://your-url.herokuapp.com password_here 
```

I run that last command on boot via `/etc/rc.local`.

## Tests

End to end tests that make sure the server + all mods are working correctly.

`pip install -r requirements.txt`

`python -m pytest`


<br>

## License

Licensed MIT
