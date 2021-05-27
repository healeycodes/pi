const store = {};

if (window.mods.includes("weather")) {
  const weather = document.querySelector("#weather");
  function update() {
    fetch("/weather/get")
      .then((data) => data.json())
      .then((json) => {
        const m = moment(json.timestamp);
        m.add(1, "hours"); // Add offset
        weather.innerHTML = `Weather data fresh as of ${m.fromNow()}..<br />
<ul>
  <li>Temperature: ${json.temperature.toFixed(1)}°C</li>
  <li>Humidity: ${json.humidity.toFixed(1)}°C</li>
</ul>`;
      });
  }
  update();
}

if (window.mods.includes("printer")) {
  const printer = document.querySelector("#printer");
  function update() {
    fetch("/printer/count-msgs")
      .then((data) => data.json())
      .then((json) => {
        printer.innerHTML = `${json.msg_count} messages have been printed so far.`;
      });
  }
  update();
}

if (window.mods.includes("sky")) {
  const sky = document.querySelector("#sky");
  function update() {
    fetch("/sky/get")
      .then((data) => data.json())
      .then((json) => {
        let lastSeenMinDate = new Date(0);
        json.map((satellite) => {
          lastSeenMinDate = Math.max(
            lastSeenMinDate,
            new Date(satellite.timestamp)
          );
        });
        const m = moment(lastSeenMinDate);
        m.add(1, "hours"); // Add offset
        sky.innerHTML = `Satellite data fresh as of ${m.fromNow()}..<br /><ul>`;

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
      });
  }
  update();
}
