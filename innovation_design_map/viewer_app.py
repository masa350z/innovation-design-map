import streamlit as st
from innovation_design_map.database import get_session, Word
from innovation_design_map.manager import WordManager
from innovation_design_map.viewer import render_graph


def main():
    st.title("Innovation Design Map")
    st.write("Bind mount でソースコードを直接編集できます。")

    # セッション & マネージャーの準備
    session = get_session()
    manager = WordManager(session)

    # 単語追加 (前回の例)
    st.subheader("add word")
    col1, col2, col3 = st.columns([4, 2, 1])

    with col1:
        new_word = st.text_input(label="", placeholder="enter word here")

    with col2:
        attribute_options = ["0", "1", "2", "tagA", "tagB"]
        selected_attr = st.selectbox(label="", options=attribute_options)

    with col3:
        if st.button("add"):
            if new_word.strip():
                manager.add_word(new_word.strip(), selected_attr)
                st.experimental_rerun()

    # --- 新規追加: リレーション作成機能 ---
    st.subheader("make relation")

    # DB上の全単語を取得してプルダウン候補に
    words = [w.text for w in session.query(Word).all()]

    col_a, col_b, col_btn = st.columns([3, 3, 1])
    with col_a:
        selected_word1 = st.selectbox("Word1", words)

    with col_b:
        selected_word2 = st.selectbox("Word2", words)

    with col_btn:
        if st.button("make relation"):
            manager.add_relation(selected_word1, selected_word2)
            st.experimental_rerun()

    # リフレッシュボタン & グラフ描画
    if st.button("Refresh Data"):
        st.experimental_rerun()

    render_graph(session)


if __name__ == "__main__":
    main()
