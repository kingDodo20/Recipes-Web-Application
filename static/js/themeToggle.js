 document.getElementById("themeToggle").addEventListener("click", function () {
  const body = document.body;

   
  body.classList.toggle("dark-theme");

   
  if (body.classList.contains("dark-theme")) {
    localStorage.setItem("theme", "dark");
  } else {
    localStorage.setItem("theme", "light");
  }
});
 
window.addEventListener("DOMContentLoaded", (event) => {
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "dark") {
    document.body.classList.add("dark-theme");
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const toggleButton = document.querySelector(".menu-toggle");
  const menu = document.querySelector("nav ul");

  toggleButton.addEventListener("click", function () {
    menu.classList.toggle("active");
  });
});


