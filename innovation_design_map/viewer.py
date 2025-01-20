import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from sqlalchemy.orm import Session
from innovation_design_map.database import Word, Relation


def render_graph(session: Session):
    words = session.query(Word).all()
    relations = session.query(Relation).all()

    G = nx.Graph()

    for w in words:
        G.add_node(w.text, attribute=w.attribute)

    for r in relations:
        w1 = session.get(Word, r.from_word_id)
        w2 = session.get(Word, r.to_word_id)
        if w1 and w2:
            G.add_edge(w1.text, w2.text)

    fig, ax = plt.subplots(figsize=(8, 6))

    # 色分け例: attribute=='1' は lightgreen, それ以外は lightblue
    color_map = []
    for node in G.nodes(data=True):
        attr = node[1].get("attribute", "")
        if attr == "1":
            color_map.append("lightgreen")
        else:
            color_map.append("lightblue")

    pos = nx.spring_layout(G, seed=42)
    nx.draw_networkx(G, pos, node_color=color_map, ax=ax, font_family="Meiryo")

    st.pyplot(fig)
