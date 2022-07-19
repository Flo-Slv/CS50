import Post from '../../../models/Post.js';

import checkAuth from '../../../utils/check-auth.js';

const createPostMutation = async (body, context) => {
	const user = checkAuth(context);

	const newPost = new Post({
		body,
		user: user.id,
		username: user.username,
		createdAt: new Date().toLocaleString()
	});

	const post = await newPost.save();

	return post;
};

export default createPostMutation;
