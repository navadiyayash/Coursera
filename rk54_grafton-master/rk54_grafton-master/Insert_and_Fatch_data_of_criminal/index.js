const { ApolloServer } = require('apollo-server');
const gql = require('graphql-tag');
const mongoose = require('mongoose');

const Post = require('./models/Post');
const Criminal_detail = require('./models/Criminal_detail');
//const { MONGODB } = require('./config.js');

const typeDefs = gql`
  type Post {
    id: ID!
    body: String!
    createdAt: String!
    username: String!
  },
  type Criminal_detail{
    criminal_name: String!
    criminal_type: String!
    captured_area: String!
    latitude: String!
    longitude: String!
    # location: [{
      # lat: String!   
      # lng: String!
    # }]
    #  time_stemp: String!
    occurances: Int!
  }
  input RegisterInput {
    
    criminal_name: String!
    criminal_type: String!
    captured_area: String!
    latitude: String!
    longitude: String!
    #  time_stemp: String!
    occurances: Int!
  }
  type Query {
    getPosts: [Post],
    getCriminal: [Criminal_detail]
  }
  type Mutation{
    register(registerInput: RegisterInput): Criminal_detail
  }
`;

const resolvers = {
  Mutation: {
    async register(
      _,
      {
           registerInput: { criminal_name, criminal_type, captured_area, occurances, latitude, longitude}
      },  
      context,
      info
      ) {
      const insert_detail = new Criminal_detail({
       criminal_name,
       criminal_type,
       captured_area,
       occurances,
       latitude, 
       longitude  
      });
    const res =  await insert_detail.save();
    return{ 
      ...res._doc,
      id: res._id
    }
    }
  }
  ,
  Query: {
    async getPosts() {
      try {
        const posts = await Post.find();
        return posts;
      } catch (err) {
        throw new Error(err);
      }
    },
    async getCriminal() {
      try {
        const criminals = await Criminal_detail.find();
        return criminals;
      } catch (err) {
        throw new Error(err);
      }
    }
  }
};

const server = new ApolloServer({
  typeDefs,
  resolvers
});

mongoose
  .connect('mongodb+srv://dhamopandav:Ql7GIeS9RoVKbJz6@cluster0.f0q1s.mongodb.net/rk54_grafton?retryWrites=true&w=majority', { useNewUrlParser: true })
  .then(() => {
    console.log('MongoDB Connected');
    return server.listen({ port: 5000 });
  })
  .then((res) => {
    console.log(`Server running at ${res.url}`);
  });
