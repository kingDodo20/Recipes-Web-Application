document.addEventListener("DOMContentLoaded", function () {
  const emailInput = document.getElementById("email");
  const updateButton = document.querySelector("button[type='submit']");

  
  const currentUserEmail = emailInput.value; 
  const lastUpdateKey = `lastEmailUpdate_${currentUserEmail}`;
  const lastUpdateDate = localStorage.getItem(lastUpdateKey);

  if (lastUpdateDate) {
      const daysSinceLastUpdate = Math.floor((new Date() - new Date(lastUpdateDate)) / (1000 * 60 * 60 * 24));
      if (daysSinceLastUpdate < 7) {
          emailInput.disabled = true;
          const message = document.createElement("p");
          message.textContent = `Email can only be updated in ${7 - daysSinceLastUpdate} days.`;
          emailInput.parentNode.insertBefore(message, emailInput.nextSibling);
      }
  }

  updateButton.addEventListener("click", function (event) {
    if (!emailInput.disabled && emailInput.value !== currentUserEmail) {
        const emailValue = emailInput.value;
        if (!emailValue.includes("@") || !emailValue.endsWith(".com")) {
            event.preventDefault();
            alert("Please enter a valid email address containing '@' and ending with '.com'.");
            return;
        }
        localStorage.setItem(lastUpdateKey, new Date().toISOString());
    }
  });
});
