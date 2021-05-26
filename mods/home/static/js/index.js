const store = {};

if (window.mods.includes("weather")) {
  const weather = document.querySelector("#weather");
  async function update() {
    const data = await fetch("/weather/get");
    const json = await data.json();

    weather.innerHTML = `Weather data fresh as of ${moment(
      json.timestamp
    ).fromNow()} seconds ago..<br />
    <ul>
      <li>Temperature: ${json.temperature.toFixed(1)}°C</li>
      <li>Humidity: ${json.humidity.toFixed(1)}°C</li>
    </ul>`;
  }
  update();
}

if (window.mods.includes("printer")) {
  const printer = document.querySelector("#printer");
  async function update() {
    const data = await fetch("/printer/count-msgs");
    const json = await data.json();

    printer.innerHTML = `${json.msg_count} messages have been printed so far.`;
  }
  update();
}

if (window.mods.includes("sky")) {
  const sky = document.querySelector("#sky");
  async function update() {
    const data = await fetch("/sky/get");
    const json = await data.json();

    let lastSeenMinDate = new Date(0);
    json.map((satellite) => {
      lastSeenMinDate = Math.min(
        lastSeenMinDate,
        new Date(satellite.timestamp)
      );
    });
    sky.innerHTML = `Satellite data fresh as of ${moment(
      lastSeenMinDate
    ).fromNow()} seconds ago..<br />
    <ul>`;

    // Visible satellites first
    json.sort((sat1, sat2) => sat2.status - sat1.status);
    json.forEach((satellite) => {
      let color = "";
      if (satellite.status === 1) {
        color = "green";
      } else {
        color = "red";
      }

      sky.innerHTML += `<li style="color: ${color};">${satellite.description}</li>`;
    });
    sky.innerHTML += "</ul>";
  }
  update();
}
