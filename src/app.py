import streamlit as st
from document_loader import load_document
from rag_pipeline import build_vectorstore, build_chain
import tempfile
import os

st.set_page_config(page_title='Private AI Assistant', page_icon='🔒', layout='wide')
st.title('🔒 Private Local AI Assistant')
st.caption('Todos os dados ficam no teu computador. Zero custos de API.')

uploaded = st.file_uploader('Carrega um documento', type=['pdf', 'txt', 'docx'])

if uploaded:
    with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded.name) as f:
        f.write(uploaded.getvalue())
        tmp_path = f.name

    with st.spinner('A processar documento...'):
        text = load_document(tmp_path)
        vs = build_vectorstore(text)
        chain = build_chain(vs)
        st.session_state['chain'] = chain
        os.unlink(tmp_path)

    st.success(f'Documento processado! {len(text)} caracteres indexados.')

if 'chain' in st.session_state:
    question = st.chat_input('Faz uma pergunta sobre o documento...')
    if question:
        with st.chat_message('user'):
            st.write(question)
        with st.chat_message('assistant'):
            with st.spinner('A pensar...'):
                answer = st.session_state['chain'].invoke(question)
                st.write(answer)