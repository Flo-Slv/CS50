import createCommentMutation from '../mutations/comment/createCommentMutation.js';
import deleteCommentMutation from '../mutations/comment/deleteCommentMutation.js';

const commentResolver = {
	Mutation: {
		createComment: async (_, { body }, context) => {
			return await createCommentMutation(body);
		},
		deleteComment: async (_, { body }, context) => {
			return await deleteCommentMutation(body);
		}
	}
};

export default commentResolver;
