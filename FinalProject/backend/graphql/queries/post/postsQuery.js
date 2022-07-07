import Post from '../../../models/Post.js';

const postsQuery = async () => {
	try {
		return await Post.find();
	}
	catch(err) {
		throw new Error(err);
	}
};

export default postsQuery;
