import requests

class Facts:
    def dog():
        return requests.get("https://some-random-api.ml/facts/dog").json()

    def cat():
        return requests.get("https://some-random-api.ml/facts/cat").json()

    def panda():
        return requests.get("https://some-random-api.ml/facts/panda").json()

    def fox():
        return requests.get("https://some-random-api.ml/facts/fox").json()

    def bird():
        return requests.get("https://some-random-api.ml/facts/bird").json()

    def koala():
        return requests.get("https://some-random-api.ml/facts/koala").json()

class Img:
    def dog():
        return requests.get("https://some-random-api.ml/img/dog").json()

    def cat():
        return requests.get("https://some-random-api.ml/img/cat").json()
    
    def panda():
        return requests.get("https://some-random-api.ml/img/panda").json()

    def red_panda():
        return requests.get("https://some-random-api.ml/img/red_panda").json()

    def birb():
        return requests.get("https://some-random-api.ml/img/birb").json()

    def fox():
        return requests.get("https://some-random-api.ml/img/fox").json()

    def koala():
        return requests.get("https://some-random-api.ml/img/koala").json()

    def pikachu():
        return requests.get("https://some-random-api.ml/img/pikachu").json()

class Animu:
    def wink():
        return requests.get("https://some-random-api.ml/animu/wink").json()

    def pat():
        return requests.get("https://some-random-api.ml/animu/pat").json()

    def hug():
        return requests.get("https://some-random-api.ml/animu/hug").json()

class Canvas:
    def gay(avatar):
        return "https://some-random-api.ml/canvas/gay?avatar=" + avatar

    def glass(avatar):
        return "https://some-random-api.ml/canvas/glass?avatar=" + avatar

    def wasted(avatar):
        return "https://some-random-api.ml/canvas/wasted?avatar=" + avatar

    def triggered(avatar):
        return "https://some-random-api.ml/canvas/triggered?avatar=" + avatar

    def greyscale(avatar):
        return "https://some-random-api.ml/canvas/greyscale?avatar=" + avatar

    def invert(avatar):
        return "https://some-random-api.ml/canvas/invert?avatar=" + avatar

    def invertgreyscale(avatar):
        return "https://some-random-api.ml/canvas/invertgreyscale?avatar=" + avatar

    def brightness(avatar):
        return "https://some-random-api.ml/canvas/brightness?avatar=" + avatar

    def threshold(avatar):
        return "https://some-random-api.ml/canvas/threshold?avatar=" + avatar

    def sepia(avatar):
        return "https://some-random-api.ml/canvas/sepia?avatar=" + avatar

    def red(avatar):
        return "https://some-random-api.ml/canvas/red?avatar=" + avatar

    def green(avatar):
        return "https://some-random-api.ml/canvas/green?avatar=" + avatar

    def blue(avatar):
        return "https://some-random-api.ml/canvas/blue?avatar=" + avatar

    def color(avatar,color):
        return "https://some-random-api.ml/canvas/red?avatar=" + avatar + "&color=" + color 

    def pixelate(avatar):
        return "https://some-random-api.ml/canvas/pixelate?avatar=" + avatar

    def youtube_comment(avatar,comment,username):
        return "https://some-random-api.ml/canvas/red?avatar=" + avatar + "&comment=" + comment + "&username=" + username

    def colorviewer(hex_):
        return "https://some-random-api.ml/canvas/colorviewer?hex=" + hex_

    def hex(rgb):
        return requests.get("https://some-random-api.ml/canvas/hex?rgb=" + rgb).json()

    def rgb(hex_):
        return requests.get("https://some-random-api.ml/canvas/rgb?hex=" + hex_).json()

class Binary:
    def encode(text):
        return requests.get("https://some-random-api.ml/binary?text=" + text).json()

    def decode(text):
        return requests.get("https://some-random-api.ml/binary?decode=" + text).json()

class Base64:
    def encode(text):
        return requests.get("https://some-random-api.ml/base64?encode=" + text).json()

    def decode(text):
        return requests.get("https://some-random-api.ml/base64?decode=" + text).json()

def pokedex(pokemon):
    return requests.get("https://some-random-api.ml/pokedex?pokemon=" + pokemon).json()

def chatbot(message):
    return requests.get("https://some-random-api.ml/chatbot?message=" + message).json()

def minecraft(username):
    return requests.get("https://some-random-api.ml/mc?username=" + username).json()

def lyrics(title):
    return requests.get("https://some-random-api.ml/lyrics?title=" + title).json()

def meme():
    return requests.get("https://some-random-api.ml/meme").json()

def bottoken():
    return requests.get("https://some-random-api.ml/bottoken").json()