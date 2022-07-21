import { UserInputError } from 'apollo-server';

import Post from '../../../models/Post.js';

import checkAuth from '../../../utils/check-auth.js';

const likePostMutation = async (postId, context) => {
	const { username } = checkAuth(context);

	const post = await Post.findById(postId);

	if (post) {
		if (post.likes.find(like => like.username === username) ) {
			// Post already liked, so unlike it (kind of toggle).
			post.likes = post.likes.filter(like => like.username !== username);
		}
		else {
			// Post not yet liked, so like it (kind of toggle).
			post.likes.push({
				username,
				createdAt: new Date().toLocaleString()
			});
		}

		await post.save();
		return post;
	} else throw new UserInputError('Post does not exist');
};

export default likePostMutation;
