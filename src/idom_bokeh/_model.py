from bokeh.core.properties import Any, Dict, Either, String, Null, Tuple
from bokeh.events import ModelEvent
from bokeh.models import HTMLBox


class IDOMEvent(ModelEvent):

    event_name = 'idom_event'

    def __init__(self, model, data=None):
        self.data = data
        super().__init__(model=model)


class IDOM(HTMLBox):

    importSourceUrl = String()

    event = Tuple(Any, Any)
