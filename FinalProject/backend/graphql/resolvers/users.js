import registerMutation from '../mutations/user/registerMutation.js';
import loginMutation from '../mutations/user/loginMutation.js';

const usersResolvers = {
	Mutation: {
		async register(_, args) {
			return await registerMutation(args);
		},
		async login(_, args) {
			return await loginMutation(args);
		}
	}
};

export default usersResolvers;
