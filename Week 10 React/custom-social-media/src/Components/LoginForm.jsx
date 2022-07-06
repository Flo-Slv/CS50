import { useState } from "react";

const LoginForm = ({ submit }) => {
	const [email, setEmail] = useState('');

	const handleChange = e => setEmail(e.target.value);

	const handleSubmit = e => {
		e.preventDefault();

		submit(email);
	};

	return (
		<form onSubmit={handleSubmit}>
			<label htmlFor="email">
				Email
				<input
					type="email"
					id="email"
					value={email}
					onChange={handleChange}
					required
				/>
			</label>

			<button type="submit">
				Login
			</button>
		</form>
	);
};

export default LoginForm;
