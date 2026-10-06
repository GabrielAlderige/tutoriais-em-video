"""Mapeia telas para escrever roteiros: títulos, botões, links, rótulos e placeholders.

Uso:
  python mapear.py http://localhost:3000 clientes,pedidos --usuario demo@x.com --senha 123
(rotas sem a barra inicial: no Git Bash do Windows, "/clientes" vira um caminho de pasta)
Grava mapa.txt e um print de cada tela na pasta mapa/.
"""
import argparse
import asyncio
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from playwright.async_api import async_playwright  # noqa: E402

from motor import Config, login_por_formulario  # noqa: E402


def limpa(xs):
    return [re.sub(r"\s+", " ", x).strip() for x in xs if x and x.strip()]


async def main(a):
    os.makedirs("mapa", exist_ok=True)
    cfg = Config(base_url=a.base.rstrip("/"), usuario=a.usuario or "", senha=a.senha or "")
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1536, "height": 864})
        if a.usuario:
            await login_por_formulario(pg, cfg, a.usuario)
        linhas = []
        for rota in a.rotas.split(","):
            # o Git Bash do Windows transforma "/clientes" em "C:/Program Files/Git/clientes"
            rota = re.sub(r"^[A-Za-z]:/.*?/Git/", "", rota.strip()).lstrip("/")
            await pg.goto(cfg.base_url + "/" + rota)
            await pg.wait_for_timeout(2000)
            corpo = pg.locator("main") if await pg.locator("main").count() else pg.locator("body")
            ph = [await i.get_attribute("placeholder") for i in await corpo.locator("[placeholder]").all()]
            linhas += [
                f"===== {rota}  ({pg.url})",
                "TÍTULOS: " + " | ".join(limpa(await corpo.locator("h1,h2,h3").all_inner_texts())),
                "BOTÕES: " + " | ".join(limpa(await corpo.get_by_role("button").all_inner_texts())[:50]),
                "LINKS: " + " | ".join(limpa(await corpo.get_by_role("link").all_inner_texts())[:30]),
                "ABAS: " + " | ".join(limpa(await corpo.get_by_role("tab").all_inner_texts())),
                "RÓTULOS: " + " | ".join(limpa(await corpo.locator("label").all_inner_texts())[:40]),
                "PLACEHOLDERS: " + " | ".join(x for x in ph if x),
                "",
            ]
            nome = re.sub(r"[^a-z0-9]+", "_", rota.lower()).strip("_") or "inicio"
            await pg.screenshot(path=os.path.join("mapa", nome + ".png"), full_page=True)
        open(os.path.join("mapa", "mapa.txt"), "w", encoding="utf-8").write("\n".join(linhas))
        print("\n".join(linhas))
        await b.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("base")
    ap.add_argument("rotas", help="rotas separadas por vírgula")
    ap.add_argument("--usuario")
    ap.add_argument("--senha")
    asyncio.run(main(ap.parse_args()))
