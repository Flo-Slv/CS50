import postsQuery from '../queries/post/postsQuery.js';
import postQuery from '../queries/post/postQuery.js';

const postResolver = {
	Query: {
		getPosts: async () => {
			return await postsQuery();
		},
		getPost: async (_, args) => {
			return await postQuery(args);
		}
	}
};

export default postResolver;
