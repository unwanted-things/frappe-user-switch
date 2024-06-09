frappe.require(["/assets/frappe_user_switch/js/nav_html.js"]);

function set_user_sid() {
  frappe.call({
    method: "frappe_user_switch.api.auth.get_current_frappe_users_sid_data",
    args: {
      sid_user_map: window.localStorage.getItem("users_token"),
    },
    callback: function (r) {
      if (r.message) {
        set_current_login_user_sid(r.message.user, r.message.sid_user_map);
        if (r.message.sid != "guest") {
          add_html(r.message.user, r.message.sid_user_array);
        }
      }
    },
  });
}

function switch_user_sid(user_name, redirect = null) {
  frappe.call({
    method: "frappe_user_switch.api.auth.switch_user_id",
    args: {
      user_name: user_name,
      sid_user_map: window.localStorage.getItem("users_token"),
    },
    callback: function (r) {
      window.localStorage.setItem("users_name", user_name);
      if (!redirect) {
        window.location.reload();
      } else {
        window.location.href = "/login";
      }
    },
  });
}

function add_new_user() {
  switch_user_sid("Guest", "/login");
}

function delete_user_id(user_name) {
  frappe.call({
    method: "frappe_user_switch.api.auth.delete_user_id",
    args: {
      user_name: user_name,
      sid_user_map: window.localStorage.getItem("users_token"),
    },
    callback: function (r) {
      window.location.href = "/login";
    },
  });
}

function delete_all_user_id() {
  frappe.call({
    method: "frappe_user_switch.api.auth.delete_all_user_id",
    args: {
      sid_user_map: window.localStorage.getItem("users_token"),
    },
    callback: function (r) {
      window.localStorage.removeItem("users_name");
      window.localStorage.removeItem("users_token");
      window.location.href = "/login";
    },
  });
}

function get_current_login_user_sid() {
  return window.localStorage.getItem("users_name");
}

function set_current_login_user_sid(user_name, sid_user_map) {
  if (user_name != "Guest") {
    window.localStorage.setItem("users_token", sid_user_map);
  }
  window.localStorage.setItem("users_name", user_name);
}

set_user_sid();
