import frappe
from frappe.sessions import Session, get_expiry_period


class MySession(Session):
    def __init__(
        self,
        sid: str,
        user: str,
        resume: bool = False,
        full_name: str | None = None,
        user_type: str | None = None,
        session_end: str | None = None,
        audit_user: str | None = None,
    ):
        self.sid = sid
        self.user = user
        self.user_type = user_type
        self.full_name = full_name
        self.data = frappe._dict({"data": frappe._dict({})})
        self.time_diff = None
        self._update_in_cache = False

        # set local session
        frappe.local.session = self.data

        if resume:
            self.resume()

        else:
            if self.user:
                self.validate_user()
                self.start(session_end, audit_user)

    def start(self, session_end: str | None = None, audit_user: str | None = None):
        """start a new session"""
        sid = self.sid

        self.data.user = self.user
        self.sid = self.data.sid = sid
        self.data.data.user = self.user
        self.data.data.session_ip = frappe.local.request_ip

        if session_end:
            self.data.data.session_end = session_end

        if audit_user:
            self.data.data.audit_user = audit_user

        if self.user != "Guest":
            self.data.data.update(
                {
                    "last_updated": frappe.utils.now(),
                    "session_expiry": get_expiry_period(),
                    "full_name": self.full_name,
                    "user_type": self.user_type,
                }
            )

        # insert session
        if self.user != "Guest":
            self.insert_session_record()

            # update user
            user = frappe.get_doc("User", self.data["user"])
            user_doctype = frappe.qb.DocType("User")
            (
                frappe.qb.update(user_doctype)
                .set(user_doctype.last_login, frappe.utils.now())
                .set(user_doctype.last_ip, frappe.local.request_ip)
                .set(user_doctype.last_active, frappe.utils.now())
                .where(user_doctype.name == self.data["user"])
            ).run()

            user.run_notifications("before_change")
            user.run_notifications("on_update")
            frappe.db.commit()
