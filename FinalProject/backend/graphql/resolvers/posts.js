import postsQuery from '../queries/post/postsQuery.js';
import postQuery from '../queries/post/postQuery.js';

import createPostMutation from '../mutations/post/createPostMutation.js';
import deletePostMutation from '../mutations/post/deletePostMutation.js';

const postResolver = {
	Query: {
		getPosts: async () => {
			return await postsQuery();
		},
		getPost: async (_, args) => {
			return await postQuery(args);
		}
	},
	Mutation: {
		createPost: async (_, { body }, context) => {
			return await createPostMutation(body, context);
		},
		deletePost: async (_, { id }) => {
			return await deletePostMutation(id);
		}
	}
};

export default postResolver;
