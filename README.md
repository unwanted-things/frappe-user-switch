## Frappe User Switch

Frappe User Switch reduces the hassle, at least on local or staging sites, for testing. It simplifies the process by allowing users to log in with multiple accounts simultaneously within a single browser session.

<br>

<div align="center">
<img src="https://github.com/user-attachments/assets/d9dfedca-1ba5-4deb-b994-fc468a9f1f39" />
</div>

<br>
<br>

> ⚠️ Warning: Since this method bypasses Frappe’s default authentication flow, it should only be used for local testing and debugging, not in production.

## Installation

Run the following command to install the app.

```bash
bench get-app https://github.com/unwanted-things/frappe-user-switch.git
bench --site [site-name] install-app frappe_user_switch
bench --site [site-name] migrate
bench restart
```

For local development, check out our dev-tool for seamlessly building Frappe apps: [frappe-manager](https://github.com/rtCamp/Frappe-Manager)  
NOTE: If using `frappe-manager`, you might require to `fm restart` to provision the worker queues.

## How Does It Work Behind the Scenes?

It’s simple! Frappe User Switch has its own way of [managing SIDs](https://modulezp.com/introducing-frappe-user-switch/).

![image](https://github.com/user-attachments/assets/f1fc5211-a9a5-4e93-ab01-e35252b2f07d)

#### License

This project is licensed under the [AGPLv3 License](./LICENSE)