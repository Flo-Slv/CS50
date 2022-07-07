import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';

import { SECRET_KEY } from '../../config.js';
import User from '../../models/User.js';

const userResolver = {
	Mutation: {
		async register(parent, args, context, info) {
			const {
				registerInput: { username, email, password, confirmPassword }
			} = args;

			// 12 rounds is pretty enough.
			password = await bcrypt.hash(password, 12);

			// Create new user and save in DB.
			const newUser = new User({
				email,
				username,
				password,
				createdAt: new Date().toISOString()
			});
			const res = await newUser.save();

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
		}
	}
};

export default userResolver;
