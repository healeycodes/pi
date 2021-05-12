# 🥧 pi architecture

I'm currently setting up my living room Raspberry Pi.

The first add-on is a POS58 receipt printer that accepts messages via HTTP.

This is so friends and family (and presumably spam bots too since I haven't hidden the URL) can ping me their thoughts.

![Receipt with "test!" and "Hello GitHub" on a bookshelf](https://github.com/healeycodes/pi/blob/main/client/preview.png)

The messages end up in a queue built on PostgreSQL. Calling it a 'queue' is probably too generous. They're printed in order – let's leave it at that.

The server runs on Heroku's free-tier.

## Run

#### Server

Create a Heroku project.

Add a PostgreSQL database via the GUI.

Add a config var of `PRINTER_PW` via GUI.

Deploy from this GitHub repository.

That's it. No migrations or other setup required.

#### Client

You'll need a Raspberry Pi connected to the internet with a POS58 receipt printer attached via USB.

```
cd client/
pip install -r requirements.txt
python python poller.py https://your-url.herokuapp.com password_here 
```

I run that last command on boot via `/etc/rc.local`.

## Tests

TODO.

Some end to end ones with an in-memory PostgreSQL database should be enough.

<br>

Licensed MIT
