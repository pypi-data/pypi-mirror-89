import typing
import numpy as np

from ovl.math.image import image_size
from ovl.helpers.types import RangedNumber
from ovl.math import contours
from ..direction_modifiers.direction_modifier import DirectionModifier


class StopIfCloseModifier(DirectionModifier):
    """
    A Direction monitor that stops when the target found is large enough (close enough).
    Like other DirectionMonitor objects, it monitors the directions returned.
    """

    def __init__(self, minimum_size: RangedNumber(0, 1), value_sent: typing.Any, priority: bool = False):
        """
        :param minimum_size: relative size in percent of the size of the image that considers the object "close" enough
                            it depends on your object size, but 40% of the image size is usually enough
                            so for an image the size of 320 x 240 it will be 320 * 240 * 0.4
        :param value_sent: the value returned if the object is close enough
        :param priority: a boolean that notes if this monitor should take priority (and stop consecutive monitors from
                         being called)
        WARNING: Setting priority to true can cause 'unexpected' behaviour as a result of stopping
        """
        self.minimum_size = minimum_size
        self.value_sent = value_sent
        self._priority = priority

    @property
    def priority(self):
        return self._priority

    def monitor(self, directions: typing.Any, targets: typing.List[np.ndarray],
                image: np.ndarray) -> typing.Any:
        """

        :param directions: the directions received from directing function / from the previous direction monitors
        :param targets: the objects found in the image
        :param image: the image where the objects where found in
        :return:
        """
        if contours.target_size(targets) / image_size(image) >= self.minimum_size:
            return self.value_sent
        return directions
