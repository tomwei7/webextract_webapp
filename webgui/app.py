#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from flask import Flask, render_template, request, redirect
from webextract import extract
app = Flask(__name__, template_folder="./templates", static_folder="./static")
url_reg = re.compile(r"^https{0,1}://.*$")


def url_check(url):
    return True if url_reg.match(url) else False


@app.route('/')
def index():
    return render_template("index.phtml")


@app.route('/extract')
def extracthtml():
    url = request.args.get("url", None)
    show_type = request.args.get("show_type", "text")
    if not url or not url_check(url):
        return redirect('/')
    else:
        body_text = extract(url, show_type=show_type)
        if show_type == "text":
            body_text = body_text.replace('\n', "<br>")
        return render_template("extract.phtml", body_text=body_text)
