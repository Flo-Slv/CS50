import { AuthenticationError } from 'apollo-server';

import Post from "../../../models/Post.js";

import checkAuth from "../../../utils/check-auth.js";

const deletePostMutation = async (postId, context) => {
	const user = checkAuth(context);

	try {
		const post = await Post.findById(postId);

		if (user.username == post.username) {
			await post.delete();
			return 'Post succesfully deleted !';
		}
		else throw new AuthenticationError(`You are not allowed to delete this post !`)
	} catch(err) {
		throw new Error(err);
	}
};

export default deletePostMutation;
