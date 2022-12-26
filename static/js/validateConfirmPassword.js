function checkPassword(form){

    const password = form.password.value;
    const confirmPassword = form.confirmPassword.value;

    if (password != confirmPassword) 
    {
      alert("Error! Password did not match.");
      return false;
    } else {
      return true;
    }
}