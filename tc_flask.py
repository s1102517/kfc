import request,json
from bs4 import BeautifuSoup

from flask import Flask, render_template, request, abort, make_response, jsonify
from datetime import datetime, timezone, timedelta

import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

from linebot import(
    Linebot, WebhookHandler
)
from linebot.exceptions import(
    InvalidSignatureError
)
from linebot.models import(
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)
line_bot_api = LineBotApi(masJq9DxN0JNm5qCnz8v5pXUqz9jTIO6sS/8EDYwjafouQEMEWxYOAgX2r5Je3VTYNON7H+wKeRvYH5YeYE6w6yH+OfTAkCGdVH1ubFxo7v3gtba0yFORlVaEHB/wE0sn4m+M/R+Cv6Qa0GgzSHnZwdB04t89/1O/w1cDnyilFU=)
handler = WebhookHandler(dfbf95a165ebe238e7d034ee20750e51)

app = Flask(__name__)

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]

    body = request.get_date(as_text=Ture)
    app.logger.info("Request body" + body)

    try:
        handler.handler(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    if(message[:6].upper() == 'KFC'):
        res = searchMenu(message[7:])
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = res))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text= "我是肯德基點餐機器人，請問您要點些什麼呢？" + event.message.text + "。")
        )
def searchMenu(keyword):
    info = "您要查詢餐點，關鍵字為:" + keyword + "\n"
    collection_ref = db.collection("KFC")
    docs = collection_ref.order_by("meal").get()
    fond = False
    for doc in docs:
        if keyword in doc.to_dict()["meal"]:
            found = True
            info += "餐點:" + doc.to_dict()["meal"] + "\n"
            info += "Meal:" + doc.to_dict()["ps"] + "\n"
            info += "餐點資訊:" + doc.to_dict()["more"] + "\n"

    if not found:
        info += "找不到符合搜尋字詞「" + keyword + "」的餐點。"
    return info

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(force=Ture)
    action = req.get("queryResult").get("action")

    if (action == "Subway_Menu"):
        cond = req.get("queryResult").get("parameters").get("Subway_Menu")
        info = ""
        result = jsonify({
            "fulfillmentText": info
            "fulfillmentMessage":[
                {"image":
                    {
                        "imageUri":"圖片.jpd"
                    }
                }
            ]
        })

    elif (action == "meal"):
        cond = req.get("queryResult").get("parameters").get("meal")

        collection_ref = db.collection("KFC")
        docs = collection_ref.get()
        found = False
        for doc in docs:
            if cond in doc.to_dict()["meal"]:
                found = True
                info = "您要查詢" + cond +"的什麼口味呢?"
        if not found:
            info = "找不到符合搜尋字詞「" + keyword + "」的口味。"
        result = jsonify({"fulfillmentText": info})

    elif (action == "taste"):
        cond = req.get("queryResult").get("parameters").get("meal") + "_"
        cond += req.get("queryResult").get("parameters").get("taste")
        info = ""
        collection_ref = db.collection("KFC")
        docs = collection_ref.get()
        found = False
        for doc in docs:
            if cond in doc.to_dict()["meal"]:
                found = True
                info += "餐點:" + doc.to_dict()["meal"] + "\n"
                info += "Meal:" + doc.to_dict()["ps"] + "\n"
                info += "餐點資訊:" + doc.to_dict()["more"] + "\n\n"
        info += "需要為您查詢" + cond +"的其他資訊嗎?" + "\n"
        if not found:
            info = "找不到符合搜尋字詞「" + keyword + "」的資訊。"
        result = jsonify({"fulfillmentText": info})

    elif (action == "other"):
        cond = req.get("queryResult").get("parameters").get("meal") + "_"
        cond += req.get("queryResult").get("parameters").get("taste")
        cond += req.get("queryResult").get("parameters").get("other")
        info = ""

        if (other == "kcal"):
            collection_ref = db.collection("KFC")
            docs = collection_ref.get()
            found = False
            for doc in docs:
                if cond in doc.to_dict()["meal"]:
                    found = True
                    info += "為您提供" + other + "的相關資訊:\n"
                    info += doc.to_dict()["meal"]
                    info += "卡路里:"+ str(doc.to_dict()["kcal"]) + "\n\n"
            if not found:
                info = "找不到符合搜尋字詞「" + keyword + "」的卡路里資訊。"
        elif (action == "money"):
            docs = collection_ref.get()
            found = False
            for doc in docs:
                if cond in doc.to_dict()["meal"]:
                    found = True
                    info += "為您提供" + other + "的相關資訊:\n"
                    info += doc.to_dict()["meal"]
                    info += "價錢:"+ str(doc.to_dict()["money"]) + "\n\n"
            if not found:
                info = "找不到符合搜尋字詞「" + keyword + "」的售價資訊。"
        elif (other == "other"):
            collection_ref = db.collection("KFC")
            docs = collection_ref.get()
            found = False
            for doc in docs:
                if cond in doc.to_dict()["meal"]:
                    found = True
                    info += "為您提供全部的相關資訊:\n"
                    info += doc.to_dict()["meal"]
                    info += "卡路里:"+ str(doc.to_dict()["kcal"]) + "\n"
                    info += "價錢:"+ str(doc.to_dict()["money"]) + "\n\n"
            if not found:
                info = "找不到符合搜尋字詞「" + keyword + "」的售價資訊。"
        result = jsonify({"fulfillmentText": info})
    elif (action == "searchMeal"):
        cond = req.get("queryResult").get("parameters").get("searchMeal")
        info = "您要查詢肯德基的" + cond + "\n\n"

        collection_ref = db.collection("KFC")
        docs = collection_ref.order_by("meal").get()
        found = False
        for doc in docs:
            if cond in doc.to_dict()["meal"]:
                found = True
                info += "餐點:" + doc.to_dict()["meal"] + "\n"
                info += "Meal:" + doc.to_dict()["ps"] + "\n"
                info += "卡路里:"+ str(doc.to_dict()["kcal"]) + "\n"
                info += "售價:"+ str(doc.to_dict()["money"]) + "\n"
                info += "餐點資訊:" + doc.to_dict()["more"]
        if not found:
            info = "找不到符合搜尋字詞「" + keyword + "」的資訊。"
        result = jsonify({"fulfillmentText": info})

    elif (action == "all_menu"):
        cond = req.get("queryResult").get("parameters").get("all_menu")
        info = "您要查詢肯德基全部的" + cond + "\n\n"

        collection_ref = db.collection("KFC")
        docs = collection_ref.order_by("meal").get()
        found = False
        for doc in docs:
            if cond in doc.to_dict()["meal"]:
                found = True
                info += doc.to_dict()["meal"] + "\n"
        if not found:
            info = "找不到符合搜尋字詞「" + keyword + "」的資訊。"
        result = jsonify({"fulfillmentText": info})
    return make_response(result)

if __name__ == "__main__":
    app.run()














