document.addEventListener("DOMContentLoaded", () => {
    const urlInput = document.getElementById("url");
    const keywordInput = document.getElementById("keyword");
    const searchButton = document.querySelector("button[type='submit']");
    const messageBox = document.createElement("p");
    messageBox.style.marginTop = "10px";
    document.querySelector("form").appendChild(messageBox);

    
    searchButton.addEventListener("click", (e) => {
        if (!urlInput.value || !keywordInput.value) {
            e.preventDefault();
            messageBox.textContent = "Please fill in both fields.";
            messageBox.style.color = "red";
        } else {
            messageBox.textContent = "Processing your request...";
            messageBox.style.color = "blue";
        }
    });
});
