import vanilla
from constants import GSSteppingTextField


class ArrowEditText(vanilla.EditText):
    nsTextFieldClass = GSSteppingTextField

    def _setCallback(self, callback):
        super(ArrowEditText, self)._setCallback(callback)
        if callback is not None and self._continuous:
            self._nsObject.setContinuous_(True)
            self._nsObject.setAction_(self._target.action_)
            self._nsObject.setTarget_(self._target)
