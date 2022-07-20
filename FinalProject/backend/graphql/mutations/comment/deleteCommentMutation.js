import { AuthenticationError, UserInputError } from "apollo-server";

import Post from "../../../models/Post.js";

import checkAuth from "../../../utils/check-auth.js";

const deleteCommentMutation = async (postId, commentId, context) => {
	const { username } = checkAuth(context);

	const post = await Post.findById(postId);

	if (post) {
		const commentIndex = post.comments.findIndex(comment =>
			comment.id === commentId
		);

		if (post.comments[commentIndex].username === username) {
			// Remove comment from the array.
			post.comments.splice(commentIndex, 1);
			await post.save();

			return post;
		} else throw new AuthenticationError('Action not allowed');
	} else throw new UserInputError('Post not found');
};

export default deleteCommentMutation;
