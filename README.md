# pit-admin-tool
**Web base admin tool for the PIT**

**This is a restful api Django backend with a react front end application.**

For the development purposes runs on two docker containers, one for the Django side (see run_django_app.sh) and another for the react side (see run_react_app.sh).

This tool allows partner coordinators to set the start and end of Call for Proposals. 
Each partner can have at least one account, but possibly more and are password authenticated. 
These accounts can see the submitted proposals for the given partnership and they can performed a number of actions, such as: generate PDF, export to csv, etc

Because we are using the Django framework a superuser can have control of the account and token management.

Also any user with super user privileges will be able to see what all the partners can see and also have access to a broader set of actions.
