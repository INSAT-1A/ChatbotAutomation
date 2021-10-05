from flask import Flask, request, jsonify
from word2number import w2n
import requests
import os
import json
import re
import datetime

app = Flask(__name__)
cf_port = os.getenv("PORT")


@app.route("/")
def index():
    return '<h1>SAP Conversational AI</h1><body>Calculator by SAP Conversational AI chatbots.<br><img src="static/283370-pictogram-purple.svg" width=260px>' \
          '<script src="https://cdn.cai.tools.sap/webchat/webchat.js" channelId="bb2f7c13-bb74-47ab-b277-57939e1d4f5f" token="c6ededdd84f55f412aa6d385e006aca9" id="cai-webchat"></script></body>'


@app.route("/calc", methods=['POST'])
def calc():
        try:
            bot_values = json.loads(request.get_data())
            num1 = bot_values['conversation']['memory']['number1']['scalar']
            num2 = bot_values['conversation']['memory']['number2']['scalar']
            operator = bot_values['conversation']['memory']['operator']['operator']
            memory = bot_values['conversation']['memory']

        except:
            num1 = 1
            num2 = 1
            operator = '+'
            memory = json.loads({})

        exp = str(num1) + " " + operator + " " + str(num2)
        result = eval(exp)
        fact_data = {'text': 'The Result is :' + str(result)}

        return jsonify(
            status=200,
            replies=[{'type': 'text', 'content': fact_data['text']}]

        )


@app.route('/spsl', methods=['POST'])
def special_numbers():
    print("hello world")

    try:
        bot_spsl = json.loads(request.get_data())
        spsl_num = bot_spsl['conversation']['memory']['special']['raw']
        print('Hello World 2')
        # Split on non-digit and keep the separators
        # pattern written in parentheses
        # spsl_list = re.split(r"(\D+)", spsl_num)

        if "/" in spsl_num:
            spsl_optr = "/"
            spsl_num1 = spsl_num.split("/")[0]
            spsl_num2 = spsl_num.split("/")[1]

        elif "-" in spsl_num:
            spsl_optr = "-"
            spsl_num1 = spsl_num.split("-")[0]
            spsl_num2 = spsl_num.split("-")[1]

        spsl_mem = bot_spsl['conversation']['memory']

    except:
        spsl_num1 = 111
        spsl_optr = '+'
        spsl_num2 = 111
        spsl_mem = json.load({})

    fact_data1 = {'number1': spsl_num1}
    fact_data2 = {'number2': spsl_num2}
    fact_data3 = {'operator': spsl_optr}
    # fact_data = {'text': 'The Result is :' + str(result)}
    spsl_mem['number1'] = {
        "raw": spsl_num1,
        "scalar": spsl_num1
    }
    spsl_mem['number2'] = {
        "raw": spsl_num2,
        "scalar": spsl_num2
    }
    spsl_mem['operator'] = {
        "raw": spsl_optr,
        "operator": spsl_optr
    }

    # Return message to display (replies) and update memory
    return jsonify(
        status=200,
        conversation={
            'memory': spsl_mem
        }
    )


@app.route("/friday", methods=['POST'])
def special_number():
    try:
        bot_special = json.loads(request.get_data())
        number01 = w2n.word_to_num(bot_special['conversation']['memory']['First_num']['value'])
        number = bot_special['conversation']['memory']['number']['scalar']
        operator = bot_special['conversation']['memory']['operator']['operator']
        memory = bot_special['conversation']['memory']

    except:
        number01 = 1
        number = 1
        operator = "+"
        memory = json.loads({})

    exp = str(number01) + " " + operator + " " + str(number)
    result = eval(exp)
    fact_data = {"text": "The result is" + str(result)}
    return jsonify(
        status=200,
        replies=[{'type': 'text',
                  'content': fact_data['text']}]

    )


if __name__ == '__main__':
    if cf_port is None:
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        app.run(host='0.0.0.0', port=int(cf_port), debug=True)
