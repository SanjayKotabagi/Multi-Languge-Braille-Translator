import streamlit as st
import utils as utl
from views import eng2br, home,about, kan2br,tel2br, mar2br
import base64


st.set_page_config(layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)
utl.inject_custom_css()
utl.navbar_component()
def navigation():
    route = utl.get_current_route()
    if route == "home":
        home.load_view()
    elif route == "about":
        about.load_view()
    elif route == "mar2br":
        mar2br.load_view()
    elif route == "eng2br":
        eng2br.load_view()
    elif route == "kan2br":
        kan2br.load_view()
    elif route == "tel2br":
        tel2br.load_view()
    elif route == None:
        home.load_view()
        
navigation()