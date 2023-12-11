# simple_crud

This is an example app that defines its own API routes for managing its models.

First initialize the database:

```
nextpy db init
nextpy db migrate
```

Then run the app:

```
nextpy init
nextpy run
```

In the UI, the list of known products is displayed on the left. On the right/main screen, user
can select HTTP Method, and enter API endpoint in the box immediately to the right of the drop down.

Endpoints are `products` for GET and POST, and `products/[id]` for GET, PUT, and DELETE.

The body of the response goes in the text area below.

In the bottom pane, the results of sending the HTTP request are shown.
