const msgID = document.querySelector("#msg-id").dataset.msgId;
const animation = document.querySelector("#animation");

animation.innerHTML = "<p>waiting for printer</p>";
function checkStatus() {
  animation.innerHTML += "<p>...</p>";
  fetch(`check-msg?msg_id=${msgID}`)
    .then((res) => res.json())
    .then((json) => {
      if (!json.status.includes("printed")) {
        setTimeout(checkStatus, 1000);
      } else {
        animation.innerHTML +=
          json.status + '<p><a href="/"><button>Print another</button></a></p>';
      }
    });
}
checkStatus();
