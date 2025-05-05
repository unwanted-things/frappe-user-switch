import frappe
import jwt
from frappe.sessions import delete_session, get_expiry_in_seconds
from frappe.utils.password import get_encryption_key


@frappe.whitelist(allow_guest=True)
def get_current_frappe_users_sid_data(sid_user_map):
    from frappe import local

    if frappe.session.user == "Guest":
        return {
            "sid": "Guest",
            "user": "Guest",
        }

    sid = local.session.get("sid")
    user = frappe.db.get_value("User", frappe.session.user, "name")

    sid_user_map, user_name = get_updated_sid_user_map(sid_user_map)

    sid_user_map[sid] = user

    sid_user_array = []

    for key in sid_user_map:
        sid_user_array.append(sid_user_map[key])

    return {
        "sid": sid,
        "user": user,
        "sid_user_array": sid_user_array,
        "sid_user_map": jwt.encode(
            sid_user_map, get_encryption_key(), algorithm="HS256"
        ),
    }


@frappe.whitelist()
def switch_user_id(user_name, sid_user_map):
    user_sid = get_sid_from_token(user_name, sid_user_map)

    frappe.local.cookie_manager.set_cookie(
        "sid", user_sid, max_age=get_expiry_in_seconds(), httponly=True
    )


@frappe.whitelist()
def delete_user_id(user_name, sid_user_map):
    user = frappe.session.user
    user_sid = get_sid_from_token(user_name, sid_user_map)
    delete_session(user_sid, user=user, reason="User Manually Logged Out")

    frappe.local.login_manager.clear_cookies()

    if frappe.request:
        frappe.local.login_manager.login_as_guest()

    switch_user_id("Guest", sid_user_map)

    return {"Done"}


@frappe.whitelist()
def delete_all_user_id(sid_user_map):
    get_updated_sid_user_map(sid_user_map, is_delete=True)
    switch_user_id("Guest", sid_user_map)


def get_sid_from_token(user_name, sid_user_map):
    sid_user_map = jwt.decode(sid_user_map, get_encryption_key(), algorithms=["HS256"])

    for key in sid_user_map:
        if sid_user_map[key] == user_name:
            return key

    return "Guest"


def get_updated_sid_user_map(sid_user_map, is_delete=False):
    if not sid_user_map:
        sid_user_map = {}
    else:
        sid_user_map = jwt.decode(
            sid_user_map, get_encryption_key(), algorithms=["HS256"]
        )

    updated_map = {}

    users_name = []

    for key in sid_user_map:
        if is_delete or (key in updated_map):
            delete_session(key, user="", reason="User Manually Logged Out")
            continue

        if sid_user_map[key] in users_name:
            delete_session(key, user="", reason="User Manually Logged Out")
            continue

        handle_seesion_exits(key, sid_user_map[key])

        updated_map[key] = sid_user_map[key]
        users_name.append(sid_user_map[key])

    return updated_map, users_name


def handle_seesion_exits(sid, user):
    import json

    from frappe_user_switch.overwrite.session import MySession

    session = frappe.qb.DocType("Sessions")
    session_id = frappe.qb.from_(session).where(session.sid == sid)
    query = session_id.select(session.sid, session.sessiondata)
    data = query.run()

    is_exists = len(data) != 0

    if is_exists:
        session_data = data[0]
        sid = session_data[0]
        session_data = json.loads(
            session_data[1].replace("'", '"').replace("None", "null")
        )
        return sid, session_data

    full_name, user_type = frappe.db.get_value("User", user, ["full_name", "user_type"])
    session_object = MySession(sid, user, full_name=full_name, user_type=user_type)

    return sid, session_object.data
