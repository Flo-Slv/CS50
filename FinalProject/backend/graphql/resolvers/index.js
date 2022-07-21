import postsResolvers from './posts.js';
import usersResolvers from './users.js';
import commentsResolvers from './comments.js';
import likesResolvers from './likes.js';

const resolvers = {
	Query: {
		...postsResolvers.Query,
	},
	Mutation: {
		...usersResolvers.Mutation,
		...postsResolvers.Mutation,
		...commentsResolvers.Mutation,
		...likesResolvers.Mutation
	}
}

export default resolvers;
