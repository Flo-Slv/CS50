import Post from '../../../models/Post.js';

import checkAuth from '../../../utils/check-auth.js';

const createPostMutation = async (body, context) => {
	const user = checkAuth(context);

	const newPost = new Post({
		body,
		user: user.id,
		username: user.username,
		createdAt: new Date().toISOString()
	});

	return post = await newPost.save();
};

export default createPostMutation;
