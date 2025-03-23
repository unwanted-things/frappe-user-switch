### This document includes the way the app manipulates the Frappe default login system to enable multiple user logins.

How Frappe login works

- After login is done, Frappe stores `sid`, `user_name`, and `user_token` in LocalStorage, and passes the values as cookies in calls to verify requests in the backend.

How the app changes the default behavior

- This app adds its own token which stores a JWT token that stores multiple `sid` values and changes the values of `sid`, `user_name`, and `user_token` from JavaScript where current.