from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from bs4 import BeautifulSoup as bs

import ask_sdk_core.utils as ask_utils
import requests


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speak_output = 'Welcome to the ReplInfo skill! You can ask me about the Replit status, current price for Hacker, hottest talk, and current open position at Replit'

        return (handler_input.response_builder.speak(speak_output).ask(
            speak_output).response)


class GetReplitStatus(AbstractRequestHandler):
    replit_status = 'https://status.replit.com'

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("GetReplitStatus")(handler_input)

    def handle(self, handler_input):
        res = requests.get(GetReplitStatus.replit_status)
        soup = bs(res.text, 'html5lib')
        section = soup.find(id='current-status')
        speak_output = section.dl.dd.h2.getText()

        return (handler_input.response_builder.speak(speak_output).response)


class GetPriceHacker(AbstractRequestHandler):
    replit_pricing = 'https://replit.com/site/pricing'

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("GetPriceHacker")(handler_input)

    def handle(self, handler_input):
        res = requests.get(GetPriceHacker.replit_pricing)
        soup = bs(res.text, 'html5lib')
        price = soup.find_all(**{'class': 'price'})
        speak_output = f'The current price is {price[1].getText()}'

        return (handler_input.response_builder.speak(speak_output).response)


class GetHottestTalk(AbstractRequestHandler):
    replit_talk = 'https://replit.com/talk/all'
    classes = {
        'posts': 'posts-feed',
        'pinned': 'board-post-list-item-header-modifiers',
        'content_post': 'board-post-list-item-content',
        'content_title': 'board-post-list-item-post-title',
        'header_post': 'board-post-list-item-header',
        'header_content': 'board-post-list-item-header-content'
    }

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("GetHottestTalk")(handler_input)

    def handle(self, handler_input):
        res = requests.get(GetHottestTalk.replit_talk)
        speak_output = None
        soup = bs(res.text, 'html5lib')
        posts_feed = soup.find(**{'class': GetHottestTalk.classes['posts']})

        for post in posts_feed.div.children:
            content = post.find(
                **{'class': GetHottestTalk.classes['content_post']})
            header = content.find(
                **{'class': GetHottestTalk.classes['header_post']})
            if len(
                    list(
                        header.find(**{
                            'class': GetHottestTalk.classes['pinned']
                        }).children)) == 0:
                header_content = header.find(
                    **{'class': GetHottestTalk.classes['header_content']})
                content_title = content.find(
                    **{'class': GetHottestTalk.classes['content_title']})

                speak_output = f'{header_content.div.getText()}, written by {header_content.span.a["title"]}, titled,  {content_title.getText()}'

                break

        return (handler_input.response_builder.speak(speak_output).response)


class GetOpenPositions(AbstractRequestHandler):
    replit_careers = 'https://api.lever.co/v0/postings/replit?skip=0&limit=10&mode=json'

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("GetOpenPositions")(handler_input)

    def handle(self, handler_input):
        jobs = requests.get(GetOpenPositions.replit_careers).json()
        speak_output = ''

        for job in jobs:
            speak_output += f'{job["text"]},'

        return (handler_input.response_builder.speak(speak_output).response)


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "This intent handler is not finished yet!"

        return (handler_input.response_builder.speak(speak_output).ask(
            speak_output).response)


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input)
                or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        speak_output = "Goodbye!"

        return (handler_input.response_builder.speak(speak_output).response)


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # Any cleanup logic goes here.
        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder.speak(speak_output)
            # .ask("add a reprompt if you want to keep the session open for the user to respond")
            .response)


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """

    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (handler_input.response_builder.speak(speak_output).ask(
            speak_output).response)
