from playwright.sync_api import sync_playwright


# URL da página com os frames
PAGINA_URL = "https://the-internet.herokuapp.com/nested_frames"


# função principal
def extrair_texto_dos_frames():
    # Inicia o Playwright
    with sync_playwright() as playwright:
        # Abre o navegador (não headless para visualização)
        navegador = playwright.chromium.launch(headless=False)
        pagina = navegador.new_page()

        # Navega até a página definida anteriormente.
        pagina.goto(PAGINA_URL)

        # Acessa os frames principais
        frame_superior = pagina.frame(name="frame-top")
        frame_inferior = pagina.frame(name="frame-bottom")

        # Função para extrair e exibir o conteúdo de um frame
        def exibir_conteudo_frame(frame, nome_frame): # Localiza a tag <body> dentro do frame
            try:
                corpo = frame.locator("body") #é onde o conteúdo principal da página está.
                if corpo.count() > 0: #  Verifica se o <body> existe.
                    texto = corpo.inner_text() # Pega o texto dentro do <body>.
                    print(f"\nConteúdo do {nome_frame}:\n{texto}")
                else:
                    print(f"\nO {nome_frame} não contém um <body> acessível.")
            except Exception as erro:
                print(f"\nErro ao acessar o {nome_frame}: {str(erro)}")
                
                #Se caso ocorra  algum erro, ele será tratado e exibido.

        # Extrai e exibe o conteúdo do frame inferior
        exibir_conteudo_frame(frame_inferior, "Frame Inferior")

        # Verifica se o frame superior existe
        if frame_superior:
            # Acessa os subframes dentro do frame superior
            subframes = {
                "frame-left": "Subframe Esquerdo",
                "frame-middle": "Subframe Meio",
                "frame-right": "Subframe Direito"
            }
            # Percorre cada subframe (esquerdo, meio e direito).
            for subframe_nome, subframe_descricao in subframes.items():
                subframe = frame_superior.child_frames # Obtém todos os subframes dentro do frame superior.
                subframe_encontrado = None

                # Procura o subframe pelo nome
                for frame in subframe:
                    if frame.name == subframe_nome:
                        subframe_encontrado = frame
                        break

                if subframe_encontrado:
                    #Se encontrado, exibe o conteúdo usando a função
                    exibir_conteudo_frame(subframe_encontrado, subframe_descricao)  
                else:
                    print(f"\n{subframe_descricao} não encontrado.")
        else:
            print("\nFrame Superior não encontrado.")

        # Fecha o navegador
        navegador.close()

# Executa a função principal
if __name__ == "__main__":
    extrair_texto_dos_frames()