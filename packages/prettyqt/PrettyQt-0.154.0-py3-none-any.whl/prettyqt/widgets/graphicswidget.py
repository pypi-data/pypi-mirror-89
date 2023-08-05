from typing import Literal, Union

from qtpy import QtWidgets

from prettyqt import constants, gui, widgets
from prettyqt.utils import InvalidParamError


QtWidgets.QGraphicsWidget.__bases__ = (widgets.GraphicsObject, widgets.GraphicsLayoutItem)

LayoutStr = Literal["grid", "horizontal", "vertical", "anchor"]


class GraphicsWidget(QtWidgets.QGraphicsWidget):
    def serialize_fields(self):
        return dict(
            autofill_background=self.autoFillBackground(),
            font=gui.Font(self.font()),
            window_title=self.windowTitle(),
            preferred_size=self.preferredSize(),
            maximum_size=self.maximumSize(),
            palette=gui.Palette(self.palette()),
            focus_policy=self.get_focus_policy(),
        )

    def set_layout(self, layout: Union[LayoutStr, QtWidgets.QGraphicsLayout, None]):
        if layout is None:
            return None
        if isinstance(layout, QtWidgets.QGraphicsLayout):
            self.box = layout
        elif layout == "grid":
            self.box = widgets.GraphicsGridLayout()
        elif layout == "anchor":
            self.box = widgets.GraphicsAnchorLayout()
        elif layout in ("horizontal", "vertical"):
            self.box = widgets.GraphicsLinearLayout(layout)
        else:
            raise ValueError("Invalid Layout")
        self.setLayout(self.box)

    def set_focus_policy(self, policy: constants.FocusPolicyStr) -> None:
        """Set the way the widget accepts keyboard focus.

        Args:
            policy: Focus policy

        Raises:
            InvalidParamError: Description
        """
        if policy not in constants.FOCUS_POLICY:
            raise InvalidParamError(policy, constants.FOCUS_POLICY)
        self.setFocusPolicy(constants.FOCUS_POLICY[policy])

    def get_focus_policy(self) -> constants.FocusPolicyStr:
        """Return way the widget accepts keyboard focus.

        Returns:
            str: Focus policy
        """
        return constants.FOCUS_POLICY.inverse[self.focusPolicy()]


if __name__ == "__main__":
    widget = GraphicsWidget()
    widget.set_layout("vertical")
