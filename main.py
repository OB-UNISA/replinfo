from flask import Flask
from waitress import serve
from paste.translogger import TransLogger
from ask_sdk_core.skill_builder import SkillBuilder
from flask_ask_sdk.skill_adapter import SkillAdapter

import intents
import os

sb = SkillBuilder()
sb.add_request_handler(intents.LaunchRequestHandler())
sb.add_request_handler(intents.HelpIntentHandler())
sb.add_request_handler(intents.CancelOrStopIntentHandler())
sb.add_request_handler(intents.GetReplitStatus())
sb.add_request_handler(intents.GetPriceHacker())
sb.add_request_handler(intents.GetHottestTalk())
sb.add_request_handler(intents.GetOpenPositions())
sb.add_request_handler(intents.SessionEndedRequestHandler())
sb.add_request_handler(intents.IntentReflectorHandler())

skill_id = os.getenv('SKILL_ID')
app = Flask('')

skill_adapter = SkillAdapter(skill=sb.create(), skill_id=skill_id, app=app)


@app.route(f'/{os.getenv("ROUTE")}', methods=["GET", "POST"])
def invoke_skill():
    return skill_adapter.dispatch_request()


def run():
    format_logger = '[%(time)s] %(status)s %(REQUEST_METHOD)s %(REQUEST_URI)s'
    serve(TransLogger(app, format=format_logger),
          host='0.0.0.0',
          port=8080,
          url_scheme='https',
          ident=None)


run()
