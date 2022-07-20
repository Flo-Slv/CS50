import createCommentMutation from '../mutations/comment/createCommentMutation.js';
import deleteCommentMutation from '../mutations/comment/deleteCommentMutation.js';

const commentResolver = {
	Mutation: {
		createComment: async (_, { body, postId }, context) => {
			return await createCommentMutation(body, postId, context);
		},
		deleteComment: async (_, { postId, commentId }, context) => {
			return await deleteCommentMutation(postId, commentId, context);
		}
	}
};

export default commentResolver;
