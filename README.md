# OSL Python Engineer test project.

## Getting Started.

You should fork this repo and commit your changes to the forked version.  A running version is not a requirement though we will favour entires that we can run and interact with.

## The Task

You’ve been asked to implement a RESTFul API micro service that will let its users create and manage teams for companies used by our platform. The service should accept JSON and return JSON responses.

Each team has an id, name and at least two members.
```
{
    'id': 'asdasdasdd',
    'name': 'Engineering',
    'members': [
        {...}
    ]
}
```

Each team member is a `User` object that should have the following attributes:
```
{
    'id': 'asdadssdasd',
    'name': 'Mike Waites',
    'email': 'mike@mike.com',
    'company': {...}
}
```

Every User in the service belongs to one company which is made up of the following attributes:

```
{
    'id': 'asdasdasd',
    'name': 'Old St Labs'
}
```

The service should make use of Flask and SqlAlchemy.  You can use any relational database of your choice to complete the task.

The service should support the following functionality:
* Create a new team
* View a list of all the teams
* View a list of all the teams for a specific company
* View a specific team


## Setting up

We've include a simple Dockerfile and basic flask app.py.  You don't have to use these if you'd prefer to run the app in another way.

assuming you have docker set up and runing you can simple do the following to get started.

`docker-compose build app`

`docker-compose run --service-ports app`

Now hit localhost:5000 in your browser and you should see a 404 template.
