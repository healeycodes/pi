# :pie: pi dashboard

This is the monorepo for my Raspberry Pi dashboard!

![The dashboard home page with weather, printer, and sky modules enabled.](https://github.com/healeycodes/pi/blob/main/client/preview.png)

A module system allows different features to be toggled on and off so you don't need my exact hardware setup. It also allows multiple Pis to use the same server.

The completed modules so far:

- :house: &nbsp; a Windows 98 themed dashboard.
- :satellite: &nbsp; view the list of visible GPS satellites from a GPS hardware device.
- :printer: &nbsp; receive printer messages to a POS58 compatible printer.
- :thermometer: &nbsp; live temperature/humidity collected from an AMxx compatible sensor.

## Run

#### Server

Toggle server modules in `config.py`.

1. Create a Heroku project.

2. Add a PostgreSQL database via the GUI.

3. Add a config var of `PW` via GUI.

4. Deploy from this GitHub repository.

That's it. No migrations or other setup required.

#### Client

You'll need a Raspberry Pi connected to the internet. Depending on what modules you've enabled in `client/config.py` you may need hardware connected and setup e.g. to use the Sky module, your GPS device must be communicating with `gpsd`.

```
cd client/
pip install -r requirements.txt
sudo python3 poller.py https://your-url.herokuapp.com password_here 
```

I run that last command on boot via `/etc/rc.local`.

## Tests

TODO.

Some end to end ones with an in-memory PostgreSQL database should be enough.

<br>

Licensed MIT
