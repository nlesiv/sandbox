from graphene import Field, Schema, ObjectType, String, Int, List, Mutation

class UserType(ObjectType):
    id = Int()
    name = String()
    age = Int()
    
class CreateUser(Mutation):
    class Arguments:
        name = String(required=True)
        age = Int(required=True)

    user = Field(UserType)

    @staticmethod
    def mutate(self, info, name, age):
        user = {"id": len(Query.users) + 1, "name": name, "age": age}
        Query.users.append(user)
        # Graphql mutation expects the return of a mutation to be the same type as the mutation itself (CreateUser)
        return CreateUser(user=user)
    
class Query(ObjectType):
    #Query Parameter that has a defined type and a default value.
    # hello = String(name=String(default_value="world"))
    # def resolve_hello(self, info, name):
    #     # Rsolver function takes in the query parameteres and resolves the data using those parameters.
    #     return f"Hello, {name}!"
    # return a single user object
    user = Field(UserType, userId=Int())

    # return a list of user objects - Resolver function has to match, the the GraphQL query filter function has to match.
    users_by_min_age = List(UserType, minAge=Int())


    users = [
        {"id":1, "name":"John Doe", "age":30},
        {"id":2, "name":"John Doasdfsfe", "age":30},
        {"id":3, "name":"aa Doe", "age":30},
        {"id":4, "name":"Jggdaohn ss", "age":30},
 
    ]

    # Resolver function for the field
    @staticmethod
    def resolve_user(root, info, userId):
        print(root)
        matched_users = [user for user in Query.users if user["id"] == userId]
        return matched_users[0] if matched_users else None
    
    @staticmethod
    def resolve_users_by_min_age(root, info, minAge):
        return [user for user in Query.users if user['age'] >= minAge]

class UpdateUser(Mutation):
    class Arguments:
        id = Int(required=True)
        name = String()
        age = Int()
    
    user = Field(UserType)

    @staticmethod
    def mutate(root, info, id, name=None, age=None):
        user = None
        for u in Query.users:
            if u['id'] == id:
                user = u
                break
        if not user:
            return None
        
        if name is not None:
            user['name'] = name
        if age is not None:
            user['age'] = age
        return UpdateUser(user=user)
    
class DeleteUser(Mutation):
    class Arguments:
        id = Int(required=True)

    user = Field(UserType)

    @staticmethod
    def mutate(rood, info, id):
        user = None
        for idx, u in enumerate(Query.users):
            if u['id'] == id:
                user = u
                del Query.users[idx]
                break
        
        return DeleteUser(user=user)

class Mutation(ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()


schema = Schema(query=Query, mutation=Mutation)

# gql = '''
# {
#   hello(name: "GraphQL")
# }
# '''

# gql = '''
# {
#   user(userId: 2) {
#     id
#     name
#     age
#   }
# }
# '''


# gql = '''
# {
#   usersByMinAge(minAge: 3) {
#     id
#     name
#     age
#   }
# }
# '''

gql = '''
mutation {
  createUser(name: "New user", age: 23) {
    user {
      id
      name
      age
    }
  }
}
'''

gqlQuery = '''
{
  usersByMinAge(minAge: 23) {
    id
    name
    age
  }
}
'''

gqlUpdate = '''
mutation {
  updateUser(name: "New user", age: 23, id: 1) {
    user {
      id
      name
      age
    }
  }
}
'''

gqlDelete = '''
mutation {
  deleteUser(id: 1) {
    user {
      id
      name
      age
    }
  }
}
'''

if __name__ == '__main__':
    # result = schema.execute(gql)
    # print(result)

    result = schema.execute(gqlQuery)
    print(result)

    result = schema.execute(gqlUpdate)
    print(result)

    result = schema.execute(gqlQuery)
    print(result)

    result = schema.execute(gqlDelete)
    print(result)

