import Post from '../../../models/Post.js';

const postQuery = async args => {
	const { postId } = args;

	try {
		const post = await Post.findById(postId);

		if (!post)
			throw new Error('Post not found !');

		return post;
	}
	catch(err) {
		throw new Error(err);
	}
};

export default postQuery;
