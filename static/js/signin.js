document.querySelector('form').addEventListener('submit', function(event) {
  const emailInput = document.getElementById('email');
  const passwordInput = document.getElementById('password');
  const rememberMe = document.querySelector('input[name="remember_me"]').checked; 

  const email = emailInput.value;
  const password = passwordInput.value;

  if (!email.includes('@') || !email.endsWith('.com')) {
    alert('Please enter a valid email address.');
    return;
  }

  if (password.length < 8){
    alert('Password should at least have 8 characters.');
    return;
  }

  if (password.trim() === '') {
    alert('Password cannot be empty.');
    return;
  }

  if (rememberMe) {
    const expiryDate = new Date();
    expiryDate.setDate(expiryDate.getDate() + 7);  
    document.cookie = `email=${email}; password=${password}; expires=${expiryDate.toUTCString()}; path=/`;
  }

 
  if (!rememberMe) {
    document.cookie = `email=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/`;
    document.cookie = `password=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/`;
  }
});

window.onload = function() {
  
  const cookies = document.cookie.split(';').reduce((acc, cookie) => {
    const [key, value] = cookie.trim().split('=');
    acc[key] = value;
    return acc;
  }, {});

  if (cookies.email && cookies.password) {
    const email = cookies.email;
    const password = cookies.password;

    
    document.getElementById('email').value = email;
    document.getElementById('password').value = password;

  }
};
