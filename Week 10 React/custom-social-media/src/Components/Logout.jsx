import { useContext } from 'react';

import { UserContext } from '../App';

const Logout = () => {
	const context = useContext(UserContext);

	const logOut = () => context.handleLogOut();

	return (
		<button onClick={logOut}>
			Logout
		</button>
	);
};

export default Logout;
