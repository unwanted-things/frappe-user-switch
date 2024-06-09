function add_html(user, sid_user_array) {
  if (!sid_user_array) {
    return;
  }
  const html = `<li style="display: flex !important;" class="nav-item dropdown dropdown-help dropdown-mobile d-none d-lg-block"> <button class="btn-reset nav-link"
    data-toggle="dropdown" aria-controls="toolbar-help" aria-label="Help Dropdown" aria-expanded="false"> <span>
        ${user} <svg class="es-icon icon-xs">
            <use href="#es-line-down"></use>
        </svg> </span> </button>
<div class="dropdown-menu dropdown-menu-right" id="toolbar-help" role="menu">
${sid_user_array
  .map((user_name) => {
    if (user_name == user) {
      return "";
    }
    return `<a class="dropdown-item"
        href="javascript:void(0)"
        onclick="switch_user_sid('${user_name}')"> ${user_name} </a>`;
  })
  .join("")}
        <a class="dropdown-item"
        style="border-top: 1px solid #000; border-radius: 0;"
        href="javascript:void(0)"
        onclick="add_new_user()"> Add new user </a>
        <a class="dropdown-item"
        href="javascript:void(0)"
        onclick="delete_user_id('${user}')"> Logout from current user </a>
        <a class="dropdown-item"
        href="javascript:void(0)"
        onclick="delete_all_user_id()"> Logout from all users</a>
</div>
</li>`;

  const interval = setInterval(() => {
    if (!window.location.href.includes("/app")) {
      if (document.querySelector("#website-post-login")) {
        clearInterval(interval);
        const nav_bar = document.querySelector("#website-post-login");
        nav_bar.insertAdjacentHTML("beforebegin", html);
      }
    } else {
      if (document.querySelector(".dropdown-navbar-user")) {
        clearInterval(interval);
        const nav_bar = document.querySelector(".dropdown-navbar-user");
        nav_bar.insertAdjacentHTML("beforebegin", html);
      }
    }
  }, 100);
}
