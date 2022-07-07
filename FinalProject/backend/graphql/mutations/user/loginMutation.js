import bcrypt from 'bcryptjs';

import { UserInputError } from 'apollo-server';

import User from '../../../models/User.js';
import { generateJwtToken } from '../../../utils/functions.js';
import { validateLoginInput } from '../../../utils/validators.js';

const loginMutation = async args => {
	const { loginInput: { username, password }} = args;

	// Validatation of login input fields.
	const { valid, errors } = validateLoginInput(username, password);

	if (!valid)
		throw new UserInputError('Errors', { errors });

	// Throw error if user does not exist in DB.
	const user = await User.findOne({ username });

	if (!user)
		throw new UserInputError('user not found in DB', {
			'errors': { 'general': 'User not found !' }
		});

	// Compare password.
	const match = await bcrypt.compare(password, user.password);

	if (!match)
		throw new UserInputError('wrong password', {
			errors: { 'password': 'Wrong password !' }
		});

	const token = generateJwtToken(user);

	return {
		...user._doc,
		id: user._id,
		token
	};
};

export default loginMutation;
