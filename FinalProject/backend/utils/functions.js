import jwt from 'jsonwebtoken';

import { SECRET_KEY } from '../config.js';

const generateJwtToken = res => {
	return jwt.sign(
		{
			id: res.id,
			email: res.email,
			username: res.username
		},
		SECRET_KEY,
		{ expiresIn: '1h' }
	);
};

export {
	generateJwtToken
};
