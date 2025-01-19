import streamlit as st
from innovation_design_map.database import get_session
from innovation_design_map.viewer import render_graph

def main():
    st.title("Innovation Design Map")
    st.write("Bind mount でソースコードを直接編集できます。")

    if st.button("Refresh Data"):
        st.experimental_rerun()

    session = get_session()
    render_graph(session)

if __name__ == "__main__":
    main()
