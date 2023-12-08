Run the command Python main.py to run the project

Go to http://127.0.0.1:5000/graphql to check the endpoints

The below are the mutations that can be tried for create, get and get all operations for departments and users

#queries
query {
  department(id: 1) {
    id
    name
  }
  
  all_departments {
    edges {
      node {
        id
        name
      }
    }
  }
  
  user(id: 1) {
    id
    name
    department {
      id
      name
    }
  }
  
  all_users {
    edges {
      node {
        id
        name
        department {
          id
          name
        }
      }
    }
  }
}


#mutations
mutation {
  createDepartment(name: "IT") {
    department {
      id
      name
    }
  }
  
  createUser(name: "John Doe", departmentId: 1) {
    user {
      id
      name
      department {
        id
        name
      }
    }
  }
}
