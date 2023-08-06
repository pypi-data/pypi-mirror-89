# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashWebSocket(Component):
    """A DashWebSocket component.
A simple interface to

Keyword arguments:
- open (dict; optional): This property is set with the content of the onopen event.
- message (dict; optional): When messages are received, this property is updated with the message content.
- error (dict; optional): This property is set with the content of the onerror event.
- close (dict; optional): This property is set with the content of the onclose event.
- send (dict; optional): When this property is set, a message is sent with its content.
- url (string; required): The websocket endpoint (e.g. wss://echo.websocket.org).
- protocols (list of strings; optional): Supported websocket protocols (optional).
- id (string; optional): The ID used to identify this component in Dash callbacks."""
    @_explicitize_args
    def __init__(self, open=Component.UNDEFINED, message=Component.UNDEFINED, error=Component.UNDEFINED, close=Component.UNDEFINED, send=Component.UNDEFINED, url=Component.REQUIRED, protocols=Component.UNDEFINED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['open', 'message', 'error', 'close', 'send', 'url', 'protocols', 'id']
        self._type = 'DashWebSocket'
        self._namespace = 'dash_extensions'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['open', 'message', 'error', 'close', 'send', 'url', 'protocols', 'id']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['url']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashWebSocket, self).__init__(**args)
