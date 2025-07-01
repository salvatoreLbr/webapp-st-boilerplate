import streamlit as st

from webapp_st_boilerplate.cmd_handler import Cmd


cmd_obj = Cmd(user_id=-9, entity_id=-9)
cmd_obj.init_database()
st.switch_page("pages/1_home.py")
