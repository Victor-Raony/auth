def main():
    try:
        consulta_geral()
    except Exception as e:
        st.warning(f"Erro ao conectar ao banco de dados: {e}")
        cria_tabela()

    db_query = consulta_geral()

    registros = {'usernames': {}}
    for data in db_query:
        registros['usernames'][data[1]] = {'name' : data[0], 'password' : data[2]}

    COOKIE_EXPIRY_DAYS = 30
    authenticator = stauth.Authenticate(
        registros,
        'random_cookie_name',
        'random_signature_key',
        COOKIE_EXPIRY_DAYS,

    )
    if 'clicou_registrar' not in st.session_state:
        st.session_state['clicou_registrar'] = False

    if st.session_state['clicou_registrar'] == False:
        login_form(authenticator=authenticator)
    else:
        usuario_form()


def login_form(authenticator):
    name, authentication_status, username = authenticator.login('Login')
    if authentication_status:
        authenticator.logout('Logout', 'main')
        st.write(f'*{name.capitalize()} está logado!*')
        st.title('🔥 Running!')
    elif authentication_status == False:
        st.error('Usuário ou senha incorretos')
    elif authentication_status == None:
        st.warning('Insira um nome de usuário e uma senha')
        clicou_em_registrar = st.button("Registrar")
        if clicou_em_registrar:
            st.session_state['clicou_registrar'] = True
            st.rerun()


def confirmation_msg():
    hashed_password = stauth.Hasher([st.session_state.pswrd]).generate()
    if st.session_state.pswrd != st.session_state.confirm_pswrd:
        st.warning('Senhas não conferem')
        sleep(3)
    elif consulta(st.session_state.user):
        st.warning('Nome de usuário já existe.')
        sleep(3)
    else:
        add_registro(st.session_state.nome,st.session_state.user, hashed_password[0])
        st.success('Registro efetuado!')
        sleep(3)

def usuario_form():
    with st.form(key="test", clear_on_submit=True):
        nome = st.text_input("Nome", key="nome")
        username = st.text_input("Usuário", key="user")
        password = st.text_input("Password", key="pswrd", type="password")
        confirm_password = st.text_input("Confirm Password", key="confirm_pswrd", type="password")
        submit = st.form_submit_button(
            "Salvar", on_click=confirmation_msg,
        )
    clicou_em_fazer_login = st.button("Fazer Login")
    if clicou_em_fazer_login:
        st.session_state['clicou_registrar'] = False
        st.rerun()

if __name__ == "__main__":
    main()

