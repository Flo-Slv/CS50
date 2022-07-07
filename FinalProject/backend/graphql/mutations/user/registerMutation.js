import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { UserInputError } from 'apollo-server';

import { SECRET_KEY } from '../../../config.js';
import User from '../../../models/User.js';
import { validateRegisterInput, validateLoginInput } from '../../../utils/validators.js';

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
	const token = jwt.sign(
		{
			id: res.id,
			email: res.email,
			username: res.username
		},
		SECRET_KEY,
		{ expiresIn: '1h' }
	);

	return {
		...res._doc,
		id: res._id,
		token
	};
};

export default registerMutation;
