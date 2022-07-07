const validateRegisterInput = (
	username,
	email,
	password,
	confirmPassword
) => {
	let errors = {};

	if (username.trim() === '')
		errors.username = 'Username must not be empty !';

	if (email.trim() === '')
		errors.email = 'Email must not be empty !';

	const regEx = /^([0-9a-zA-Z]([-.\w]*[0-9a-zA-Z])*@([0-9a-zA-Z][-\w]*[0-9a-zA-Z]\.)+[a-zA-Z]{2,9})$/;

	if (!email.match(regEx))
		errors.email = 'Email is not a valid email address !';

	if (password.trim() === '')
		errors.password = 'Password should not be empty !';

	if (confirmPassword.trim() === '')
		errors.secondPassword = 'Confirmation password should not be empty !';

	if (password.trim() !== confirmPassword.trim())
		errors.confirmPassword = 'Both password should be identical !';

	return {
		errors,
		valid: Object.keys(errors).length < 1
	};
};

const validateLoginInput = (username, password) => {
	let errors = {};

	if (username.trim() === '')
		errors.username = 'Username should not be empty !';

	if (password.trim() === '')
		errors.password = 'Password should not be empty !';

	return {
		errors,
		valid: Object.keys(errors).length < 1
	};
};

export {
	validateRegisterInput,
	validateLoginInput
};
