from webapp_st_boilerplate.auth.authorization import AuthManager


def test_get_required_level():
    auth_manager_obj = AuthManager()
    required_level = auth_manager_obj.get_required_level(method_name="disable_user")
    assert required_level == 3, "!!! Error in get_required_level"


def test_can_access():
    auth_manager_obj = AuthManager()
    can_access = auth_manager_obj.can_access(user_current_level=1, method_name="disable_user")
    assert can_access is False, "!!! Error in can_access"
