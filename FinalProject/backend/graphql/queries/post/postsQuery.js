import Post from '../../../models/Post.js';

const postsQuery = async () => {
	try {
		// Find all posts and return by sorting createdAt.
		return await Post.find().sort({ 'createdAt': 'asc' });
	}
	catch(err) {
		throw new Error(err);
	}
};

export default postsQuery;
