import postsResolvers from './posts.js';
import usersResolvers from './users.js';

const resolvers = {
	Query: {
		...postsResolvers.Query,
		...usersResolvers.Query
	}
}

export default resolvers;
