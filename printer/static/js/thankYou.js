const msgID = document.querySelector("#msg-id").dataset.msgId;
const animation = document.querySelector("#animation");

animation.innerHTML = "waiting for printer";
function checkStatus() {
  animation.innerHTML += "\n...";
  fetch(`check-msg?msg_id=${msgID}`)
    .then((res) => res.json())
    .then((json) => {
      if (!json.status.includes("printed")) {
        setTimeout(checkStatus, 400);
      } else {
        animation.innerHTML =
          json.status + '<p><a href="/"><button>Print another</button></a></p>';
      }
    });
}
checkStatus();
