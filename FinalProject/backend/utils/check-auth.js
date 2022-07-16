import { AuthenticationError } from 'apollo-server';
import jwt from 'jsonwebtoken';

import { SECRET_KEY } from '../config.js';

const checkAuth = context => {
	const authHeader = context.req.headers.authorization;
	
	if (authHeader) {
		const token = authHeader.split('Bearer ')[1];

		if (token)
			try {
				return user = jwt.verify(token, SECRET_KEY);
			} catch(err) {
				throw new AuthenticationError('Invalid/expired token !');
			}

		throw new Error('Wrong token: \'Bearer [token]');
	}

	throw new Error('Authenticaton header must be provided !');
};

export default checkAuth;
