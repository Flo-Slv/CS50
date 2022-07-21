import likePostMutation from '../mutations/like/likePostMutation.js';

const likeResolver = {
	Mutation: {
		likePost: async (_, { postId }, context) => {
			return await likePostMutation(postId, context);
		}
	}
};

export default likeResolver;
