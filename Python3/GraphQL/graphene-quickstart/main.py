from graphene import Schema, ObjectType, String


class Query(ObjectType):
    #Query Parameter that has a defined type and a default value.
    hello = String(name=String(default_value="world"))
    def resolve_hello(self, info, name):
        # Rsolver function takes in the query parameteres and resolves the data using those parameters.
        return f"Hello, {name}!"

schema = Schema(query=Query)

gql = '''
{
  hello(name: "GraphQL")
}
'''

if __name__ == '__main__':
    result = schema.execute(gql)
    print(result)