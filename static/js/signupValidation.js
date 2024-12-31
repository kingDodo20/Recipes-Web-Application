document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('signupForm');

  form.addEventListener('submit', function(e) {

    let email = form.email.value;
    let password = form.password.value;
    let confirmPassword = form.confirm_password.value;
    let dateOfBirth = form.date_of_birth.value;

    
    if (!email.includes('@') || !email.endsWith('.com')) {
      alert('Please enter a valid email address.');
      e.preventDefault();
      return;
    }
    if (password.length < 8){
      alert('Password should at least have 8 characters.');
      e.preventDefault();
      return;
    }
    
    if (password.trim() === '') {
      alert('Password cannot be empty.');
      e.preventDefault();
      return;
    }

    
    if (password !== confirmPassword) {
      alert('Passwords do not match.');
      e.preventDefault();
      return;
    }

   
    if (new Date(dateOfBirth) > new Date()) {
      alert('Date of Birth cannot be in the future.');
      e.preventDefault();
      return;
    }
  });
});
