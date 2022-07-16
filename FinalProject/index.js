import { ApolloServer } from 'apollo-server';
import mongoose from 'mongoose';

import { MONGODB } from './backend/config.js';

import typeDefs from './backend/graphql/typeDefs.js';
import resolvers from './backend/graphql/resolvers/index.js';

// tutorial: 1'18'43

const server = new ApolloServer({
	typeDefs,
	resolvers,
	context: ({ req }) => ({ req })
});

mongoose
	.connect(MONGODB, { useNewUrlParser: true })
	.then(() => {
		console.log('MongoDB connected');
		return server.listen({ port: 5000 })
	})
	.then(res => {
		console.log(`Server running at ${res.url}`);
	});
