"""Aula de exemplo. Copie, troque a Config pelo seu sistema e os passos pela sua tela.

Rodar:  python exemplo/aula_exemplo.py
Sai em:  videos/01-cadastrar-cliente.mp4
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from motor import (Aula, Config, Passo, cartao, celular_chat, clicar, configurar, digitar, focar,  # noqa: E402
                   marcar, pausa, rodar, selecionar)

configurar(Config(
    base_url="http://localhost:3000",
    usuario="demo@exemplo.com",
    senha="senha-da-demo",
    # login=minha_funcao_de_login,   # se a tela de login não for e-mail + senha + botão "Entrar"
    marca={
        "produto": "MeuSistema", "destaque": "Sistema",        # "Sistema" sai na cor
        "cor": "#2563EB", "fundo": "#0B1020",
        "rodapeAbertura": "<b>Tutoriais do MeuSistema</b><span>meusistema.com</span>",
        "rodapeEncerramento": "<b>Dúvidas? suporte@meusistema.com</b>",
        "trocas": [["http://localhost:3000", "https://app.meusistema.com"]],
        "zoom": 1.25,
    },
    pasta=os.path.join(os.path.dirname(__file__), ".."),
    recriar_demo=None,   # ex.: "npm run seed:demo -- --reset"
))


# atalhos de localização: sempre pelo papel e nome acessível, como uma pessoa enxerga
def botao(nome):
    return lambda p: p.get_by_role("button", name=nome, exact=True).first


def campo(rotulo):
    return lambda p: p.get_by_role("dialog").get_by_label(rotulo, exact=True).first


AULA = Aula(
    slug="cadastrar-cliente", numero=1, modulo="Primeiros passos",
    titulo="Cadastrando um cliente",
    subtitulo="Só o nome é obrigatório.",
    abertura_fala="Nesta aula, você vai cadastrar um cliente em menos de um minuto.",
    inicio="/clientes",
    passos=[
        Passo("Para cadastrar, toque em Novo cliente.",
              [clicar(botao("Novo cliente"))]),
        Passo("Preencha o nome e o telefone.",
              [digitar(campo("Nome"), "Ricardo Almeida"), digitar(campo("Telefone"), "(11) 90000-0091")]),
        Passo("Escolha como ele conheceu a empresa.",
              [selecionar(campo("Origem"), "Indicação")]),
        Passo("Toque em Salvar. Pronto: o cliente já aparece na lista.",
              [clicar(botao("Salvar"), 1.4), focar(lambda p: p.get_by_text("Ricardo Almeida").first)],
              legenda="Cliente cadastrado."),
        Passo("Quando você mandar uma mensagem para ele, é assim que ela chega no celular.",
              [focar(None), celular_chat("MeuSistema", "Olá, Ricardo! Seu cadastro está pronto: https://app.meusistema.com"),
               pausa(1.5)]),
    ],
    encerramento_titulo="Cliente cadastrado.",
    encerramento_fala="Pronto! Na próxima aula: criar o primeiro pedido.",
    proxima="Criando o primeiro pedido",
)

if __name__ == "__main__":
    rodar(AULA)
