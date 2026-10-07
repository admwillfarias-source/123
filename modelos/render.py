"""Uso: python3 modelos/render.py entrada.html saida.jpg  (o HTML deve ficar dentro da pasta modelos/)"""
import sys, os
from playwright.sync_api import sync_playwright
src, out = os.path.abspath(sys.argv[1]), sys.argv[2]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width':1080,'height':1350})
    pg.goto('file://' + src); pg.wait_for_timeout(600)
    pg.screenshot(path=out, type='jpeg', quality=92); b.close()
