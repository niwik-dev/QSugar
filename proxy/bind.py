from functools import wraps

from QSugar.proxy.base import BaseClazzProxy
from QSugar.singleton.dispatcher import NotifySignalDispatcher
from QSugar.type.computed import Computed
from QSugar.type.reference import Ref
from QSugar.util.reflect import ReflectUtil


class BindClazzProxy(BaseClazzProxy):
    NoRepeatRequestSend = '__no_repeat_request_send__'
    """
    This property is used to ensure that the Dispatcher does not receive repeated requests.
    """
    @classmethod
    def get_ref_param(cls, key, *args, **kwargs):
        """
        Separate objects of reference type from parameters
        """
        refValue = None
        if key in kwargs:
            value = kwargs[key]
            if isinstance(value, Ref) or isinstance(value,Computed):
                refValue = value
                del kwargs[key]
        elif len(args) >= 2:
            value = args[1]
            if isinstance(value, Ref) or isinstance(value,Computed):
                refValue = value
                args = list(args)
                args.remove(value)
        return refValue, args, kwargs

    @classmethod
    def proxy_clazz_setter(cls, setter, setter_name:str, getter_name:str):
        """
        setter method proxy, which implements Responsive UI.
        """
        @wraps(setter)
        def setter_proxy(*args, **kwargs):
            self = args[0]
            valueRef, args, kwargs = cls.get_ref_param(getter_name, *args, **kwargs)
            if valueRef:
                prop_name = getter_name.removeprefix('is').lower()
                NotifySignalDispatcher().describe(
                    self, prop_name, valueRef
                )
            if len(args) == 1 and len(kwargs) == 0:
                return self

            if not getter_name:
                result = setter(*args, **kwargs)
                return result

            getter = getattr(self, getter_name)
            notify_signal_name = getter_name + 'Changed'

            if hasattr(self, notify_signal_name):
                notify_signal = getattr(self, notify_signal_name)
                if not hasattr(self, cls.NoRepeatRequestSend):
                    setattr(self, cls.NoRepeatRequestSend, True)
                    notify_signal.connect(
                        lambda: NotifySignalDispatcher().requestReceived.emit(self, getter_name, getter())
                    )
            else:
                oldValue = getter()
                newValue = kwargs.get(getter_name) or args[1]
                if oldValue != newValue:
                    NotifySignalDispatcher().requestReceived.emit(self, getter_name, newValue)
                setter(*args, **kwargs)

            return self

        return setter_proxy

    def __call__(self, clazz):
        super().__call__(clazz)
        mro_clazz_list = clazz.mro()
        for mro_clazz in mro_clazz_list:
            if mro_clazz == object:
                continue
            for setter_name, getter_name in ReflectUtil.scanSymmetricProps(mro_clazz):
                clazz_setter = getattr(mro_clazz, setter_name)
                proxy_setter = self.proxy_clazz_setter(clazz_setter, setter_name, getter_name)
                setattr(mro_clazz, setter_name, proxy_setter)
        return clazz


Bind = BindClazzProxy()
