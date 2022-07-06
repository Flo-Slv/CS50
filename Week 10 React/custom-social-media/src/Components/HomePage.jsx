import { useContext } from "react";

import { UserContext } from '../App';
import Logout from './Logout';

const HomePage = () => {
	const context = useContext(UserContext);

	return (
		<Logout />
	);
};

export default HomePage;
