function checkFunction(){
	var password = document.getElementById("password");
	var checkPassword = document.getElementById("checkPassword");

	console.log(password.value);
	console.log(checkPassword.value);
	var pswEquals = (password.value == checkPassword.value);
	if(pswEquals) {
		pswLabel.innerHTML = "Passwords match";
		btn.disabled = false;
	}
	else{
		pswLabel.innerHTML = "Passwords do not match";
	}
}