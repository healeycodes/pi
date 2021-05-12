const msgID = document.querySelector("#msg-id").dataset.msgId;
const animation = document.querySelector("#animation");

animation.innerHTML = "waiting for printer";
function checkStatus() {
  anim.innerHTML += "\n...";
  fetch(`check-msg?${msgid}`)
    .then((res) => res.json())
    .then((json) => {
      if (!json.status.includes("printed")) {
        setTimeout(checkStatus, 400);
      } else {
        anim.innerHTML = json.status;
      }
    });
}
