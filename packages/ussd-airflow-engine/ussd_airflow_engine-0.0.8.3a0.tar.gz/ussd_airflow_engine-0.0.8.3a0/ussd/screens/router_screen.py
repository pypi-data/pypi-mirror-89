from ussd.core import UssdHandlerAbstract
from ussd.graph import Link, Vertex
from ussd.screens.schema import UssdBaseScreenSchema, NextUssdScreenSchema, NextUssdScreenField, WithItemSchema
from marshmallow import fields, Schema


class RouterOptionSchema(NextUssdScreenSchema):
    expression = fields.Str(required=True)


class RouterSchema(UssdBaseScreenSchema, WithItemSchema):
    router_options = fields.List(
        fields.Nested(RouterOptionSchema),
        required=True
    )
    default_next_screen = NextUssdScreenField(required=False)


class RouterScreen(UssdHandlerAbstract):
    """
    This screen is invisible to the user. Sometimes you would like to
    direct user to different screens depending on some status.

    For instance you want to show different screen to users who are not
    registered and a different screen to users who have already registered.
    This is the screen to create.

    Fields used to create this screen:
        1. router_options
            This is a list of router option.
            Each router option has the following fields
                a. expression
                    This is a jinja expression that's is evaluating to boolean
                    It can reference anything in the session and parameters
                    in ussd_request
                b. next_screen
                    This is the screen to direct to if the above expression
                    is true
        2. default_next_screen (optional)
            This is the screen to direct to if all expression in router_options
            failed.

        3. with_items (optional)
            Sometimes you want to loop over something until an item
            passes the expression. In this case use with_items.
            When using with_items you can use variable item in the
            expression.

            see in the example below for more explanation

        Examples of router screens

            .. literalinclude:: .././ussd/tests/sample_screen_definition/valid_router_screen_conf.yml
    """

    screen_type = "router_screen"
    serializer = RouterSchema

    def handle(self):
        return self.route_options(
            self.screen_content.get("router_options")
        )

    def show_ussd_content(self, **kwargs):
        return "Routing screen: {}".format(self.handler)

    def get_next_screens(self):
        links = []

        for obj in self.screen_content['router_options']:
            links.append(
                Link(
                    Vertex(self.handler),
                    Vertex(obj['next_screen']),
                    obj['expression']
                )
            )

        if self.screen_content.get('default_next_screen'):
            links.append(
                Link(
                    Vertex(self.handler),
                    Vertex(self.screen_content['default_next_screen']),
                    'default'
                )
            )

        return links
