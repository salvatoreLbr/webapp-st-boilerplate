from webapp_st_boilerplate.auth.authorization import AuthManager
from webapp_st_boilerplate.front_end.cmd import FrontEnd


front_end_obj = FrontEnd(auth_manager=AuthManager())
front_end_obj.set_user_panel()
