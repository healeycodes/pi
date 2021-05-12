const msgID = document.querySelector("#msg-id").dataset.msgId;
const animation = document.querySelector("#animation");

animation.innerHTML = "Waiting for printer";
function checkStatus() {
  fetch(`check-msg?${msgID}`)
    .then((res) => res.json())
    .then((json) => {
      if (!json.status.includes("printed")) {
        animation.innerHTML += "\n...";
        setTimeout(checkStatus, 500);
      } else {
        animation.innerHTML = json.status;
      }
    });
}
