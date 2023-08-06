# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Popup(Component):
    """A Popup component.


Keyword arguments:
- children (a list of or a singular dash component, string or number; optional)
- id (string; optional): The ID used to identify this compnent in Dash callbacks
- showTitle (boolean; optional)
- title (string; optional)
- visible (boolean; optional)
- dragEnabled (boolean; optional)
- closeOnOutsideClick (boolean; optional)
- closeOnBackButton (boolean; optional)
- loading_state (dict; optional): Object that holds the loading state object coming from dash-renderer. loading_state has the following type: dict containing keys 'is_loading', 'prop_name', 'component_name'.
Those keys have the following types:
  - is_loading (boolean; optional): Determines if the component is loading or not
  - prop_name (string; optional): Holds which property is loading
  - component_name (string; optional): Holds the name of the component that is loading"""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, showTitle=Component.UNDEFINED, title=Component.UNDEFINED, visible=Component.UNDEFINED, dragEnabled=Component.UNDEFINED, closeOnOutsideClick=Component.UNDEFINED, closeOnBackButton=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'showTitle', 'title', 'visible', 'dragEnabled', 'closeOnOutsideClick', 'closeOnBackButton', 'loading_state']
        self._type = 'Popup'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'showTitle', 'title', 'visible', 'dragEnabled', 'closeOnOutsideClick', 'closeOnBackButton', 'loading_state']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Popup, self).__init__(children=children, **args)
