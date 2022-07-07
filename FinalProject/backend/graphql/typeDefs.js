import gql from 'graphql-tag';

const typeDefs = gql`
	type Post {
		id: ID!
		body: String!
		createdAt: String!
		username: String!
	}

	type User {
		id: ID!
		username: String!
		email: String!
		token: String!
		createdAt: String!
	}

	input RegisterInput {
		username: String!
		password: String!
		confirmPassword: String!
		email: String!
	}

	input LoginInput {
		username: String!
		password: String!
	}

	type Query {
		getPosts: [Post]
	}

	type Mutation {
		register(registerInput: RegisterInput): User!
		login(loginInput: LoginInput): User!
	}
`;

export default typeDefs;
