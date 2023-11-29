async function postData(url = "", data = {}) {
    const response = await fetch(url, {
      method: "POST", headers: {
        "Content-Type": "application/json",
      }, body: JSON.stringify(data)
    });
    return response.json();
  }

let sendButton = document.getElementById("sendButton");
sendButton.addEventListener('click', async () => {
    let questionInput = document.getElementById("questionInput").value;
    document.getElementById("questionInput").value = "";
    document.getElementById("right1").style.display = "none";
    document.getElementById("right2").style.display = "block";

    question1.innerHTML = questionInput;
    question2.innerHTML = questionInput;

    let result = await postData("/api", {"question": questionInput})
    console.log(result.result)
    solution.innerHTML = result.result;
})
