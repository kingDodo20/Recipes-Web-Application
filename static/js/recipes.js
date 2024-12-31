document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("searchInput");
    const recipeCards = document.querySelectorAll(".card");

    if (searchInput) {
        searchInput.addEventListener("input", (event) => {
            const filterText = event.target.value.toLowerCase();

            recipeCards.forEach(card => {
                const titleElement = card.querySelector(".card-title");
                const descriptionElement = card.querySelector(".card-text");
                const titleText = titleElement.textContent.toLowerCase();
                const descriptionText = descriptionElement.textContent.toLowerCase();

                if (titleText.includes(filterText) || descriptionText.includes(filterText)) {
                    card.style.display = "block";
                } else {
                    card.style.display = "none";
                }
            });
        });
    }
});
