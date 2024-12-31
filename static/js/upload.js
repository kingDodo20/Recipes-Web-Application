// Validate form fields on submit
document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");

  const fatInput = document.getElementById('fat');
  const carbsInput = document.getElementById('carbs');
  const proteinInput = document.getElementById('protein');
  const caloriesInput = document.getElementById('calories');

  const calculateCalories = () => {
      const fat = parseFloat(fatInput.value) || 0;
      const carbs = parseFloat(carbsInput.value) || 0;
      const protein = parseFloat(proteinInput.value) || 0;
      const calories = (fat * 9) + (carbs * 4) + (protein * 4);
      caloriesInput.value = calories.toFixed(2); 
  };

  [fatInput, carbsInput, proteinInput].forEach(input => {
      input.addEventListener('input', calculateCalories);
  });

  form.addEventListener("submit", function (e) {
      e.preventDefault();
      const ingredients = document.getElementById("ingredients").value.trim();

      if (!ingredients.includes(";")) {
          alert("Please separate ingredients using a semicolon (;).");
          return false;
      }

      alert("Recipe uploaded successfully!");
      form.submit();
  });
});