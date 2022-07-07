import bcrypt from 'bcryptjs';
import { UserInputError } from 'apollo-server';

import User from '../../../models/User.js';
import { generateJwtToken } from '../../../utils/functions.js';
import { validateRegisterInput } from '../../../utils/validators.js';

const registerMutation = async args => {
	const {
		registerInput: { username, email, password, confirmPassword }
	} = args;

	// Validation of user input fields.
	const { errors, valid } = validateRegisterInput(
		username,
		email,
		password,
		confirmPassword
	);

	if (!valid)
		throw new UserInputError('Errors', { errors });

	// Check if user unique, if not, throw error.
	const user = await User.findOne({ username });

	if (user)
		// We use apollo error to display in frontend w/ apollo-client.
		throw new UserInputError('username is taken', {
			errors: {
				username: 'This username is already taken !'
			}
		});

	// 12 rounds is pretty sure..
	let pwd = await bcrypt.hash(password, 12);

	// Create new user and save in DB.
	const newUser = new User({
		email,
		username,
		password: pwd,
		createdAt: new Date().toISOString()
	});
	const res = await newUser.save();

	// Create Jsonwebtoken.
	const token = generateJwtToken(res);

	return {
		...res._doc,
		id: res._id,
		token
	};
};

export default registerMutation;
