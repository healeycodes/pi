const msgCount = document.querySelector("#message-count");
fetch("count-msgs")
  .then((res) => res.json())
  .then(
    (json) =>
      (msgCount.innerHTML = `${json.msg_count} messages printed so far!`)
  );
