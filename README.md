# :pie: pi dashboard

This is the monorepo for my Raspberry Pi dashboard! It's me-ware, and you're unlikely to use it but I'm happy to help you set it up.

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

Toggle server modules in `serverconfig.py`.

1. Create a Heroku project.

2. Add a PostgreSQL database via the GUI.

3. Add a config var of `PW` via GUI.

4. Deploy from this GitHub repository.

That's it. No migrations or other setup required.

For local development, `pip install -r requirements.txt` and run `python app.py`.

#### Client

You'll need a Raspberry Pi connected to the internet. Depending on what modules you've enabled in `client/clientconfig.py` you may need hardware connected and setup e.g. to use the Sky module, your GPS device must be communicating with `gpsd`.

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

Licensed MIT
