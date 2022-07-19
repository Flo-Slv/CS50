import { UserInputError } from 'apollo-server';

import Post from '../../../models/Post.js';

import checkAuth from '../../../utils/check-auth.js';

const createCommentMutation = async (body, postId, context) => {
	const { username } = checkAuth(context);

	// If try to post empty comment.
	if (body.trim() === '')
		throw new UserInputError('Empty comment', {
			errors: {
				body: 'Comment must not be empty !'
			}
		});

	const post = await Post.findById(postId);

	if (post) {
		// Add comment to the top.
		post.comments.unshift({
			body,
			username,
			createdAt: new Date().toLocaleString()
		});

		await post.save();
		return post;
	} else throw new UserInputError('Post not found');
};

export default createCommentMutation;
