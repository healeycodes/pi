const store = {};

if (window.mods.includes("sky")) {
  const sky = document.querySelector("#sky");
  async function update() {
    const data = await fetch("/sky/get");
    const json = await data.json();

    sky.innerHTML = "<ul>";

    // Visible satellites first
    json.sort((sat1, sat2) => sat2.status - sat1.status);
    json.forEach((satellite) => {
      let color = "";
      let lastSeenMsg = "";
      if (satellite.status === 1) {
        color = "green";
        const timestamp = new Date(satellite.timestamp);
        const lastSeen = Math.round(
          new Date().getTime() / 1000 - timestamp.getTime() / 1000
        );
        lastSeenMsg = `(last seen ${lastSeen} seconds ago..)`;
      } else {
        color = "red";
      }

      sky.innerHTML += `<li style="color: ${color};">${satellite.description} ${lastSeenMsg}</li>`;
    });
    sky.innerHTML += "</ul>";
  }
  update();
}
if (window.mods.includes("weather")) {
  const weather = document.querySelector("#weather");
}
if (window.mods.includes("printer")) {
  const printer = document.querySelector("#printer");
}
