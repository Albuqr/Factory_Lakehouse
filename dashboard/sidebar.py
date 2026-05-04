import streamlit as st
from datetime import datetime


def render_sidebar(description: str = ""):
    st.sidebar.title("🏭 Factory Lakehouse")
    st.sidebar.markdown("---")
    if description:
        st.sidebar.markdown(description)
        st.sidebar.markdown("---")
    st.sidebar.markdown(
        "[![GitHub](https://img.shields.io/badge/GitHub-Source-181717?logo=github&style=flat-square)]"
        "(https://github.com/Albuqr/Factory_Lakehouse)"
    )
    st.sidebar.caption(f"Last updated · {datetime.now().strftime('%b %d, %Y')}")
