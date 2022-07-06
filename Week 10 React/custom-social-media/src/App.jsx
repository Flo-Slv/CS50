import { useReducer, createContext, useEffect } from 'react';
import Cookies from 'universal-cookie';

import HomePage from './Components/HomePage';
import LoginForm from './Components/LoginForm';

import './App.css';

const cookies = new Cookies();

export const UserContext = createContext({});

const actionTypes = {
	LOGIN: 'login',
	LOGOUT: 'logout'
};

const reducer = (state, action) => {
	switch (action.type) {
		case actionTypes.LOGIN: {
			const user = { ...state, email: action.payload };

			cookies.set('user', action.payload, { path: '/' });

			return user;
		}
		case actionTypes.LOGOUT: {
			const user = {};

			cookies.remove('user', { path: '/' });

			return user;
		}
		default: throw new Error(`${action.type} n'existe pas`);
	};
};

const logIn = (dispatch, email) => {
	dispatch({ type: actionTypes.LOGIN, payload: email });
};

const logOut = dispatch => dispatch({ type: actionTypes.LOGOUT });

const App = () => {
	const [user, dispatch] = useReducer(reducer, {});

	useEffect(() => {
		const email = cookies.get('user');

		if (email && !user?.email) logIn(dispatch, email);
	}, []);

	const handleLogIn = email => logIn(dispatch, email);

	const handleLogOut = () => logOut(dispatch);

	return (
		<>
			{cookies.get('user') ? (
				<UserContext.Provider value={{ user, handleLogOut }}>
					<HomePage />
				</UserContext.Provider>
			) : (
				<LoginForm submit={handleLogIn}/>
			)}
		</>
	);
};

export default App;
