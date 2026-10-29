import gc
import sys
import weakref


def header(title):
    print(f"\n=== {title} ===")


class Node:
    def __init__(self, name):
        self.name, self.other = name, None

    def __del__(self):
        print(f"   [__del__] {self.name} destroyed")


def exp1_refcount():
    header("1. Reference counting (immediate)")
    a = Node("A")
    print("   refcount:", sys.getrefcount(a))
    b = a
    print("   after b = a:", sys.getrefcount(a))
    del b
    print("   deleting last reference:")
    del a  


def exp2_cycles():
    header("2. Cycles need the cyclic GC")
    gc.disable()
    x, y = Node("X"), Node("Y")
    x.other, y.other = y, x
    w = weakref.ref(x)
    del x, y
    print("   alive after del (leaked)?", w() is not None)
    print("   gc.collect() found:", gc.collect(), "objects")
    print("   alive after collect?", w() is not None)
    gc.enable()


def exp3_generations():
    header("3. Generations and thresholds")
    print("   threshold:", gc.get_threshold())
    print("   count    :", gc.get_count())
    for gen in (0, 1, 2):
        print(f"   gc.collect({gen}) ->", gc.collect(gen))


def exp4_callbacks():
    header("4. Automatic collections via gc.callbacks")
    events = []
    cb = lambda phase, info: phase == "stop" and events.append(info["generation"])
    gc.callbacks.append(cb)
    for _ in range(5000):
        l = []
        l.append(l)  
    gc.callbacks.remove(cb)
    print(f"   {len(events)} automatic collections ran")


def exp5_tracking():
    header("5. What does the GC track?")
    for label, obj in {"int": 42, "str": "hi", "list": [], "dict": {}, "Node": Node("tmp")}.items():
        print(f"   {label:5} tracked: {gc.is_tracked(obj)}")


def exp6_saveall():
    header("6. gc.DEBUG_SAVEALL")
    gc.collect()
    gc.set_debug(gc.DEBUG_SAVEALL)
    a, b = [], []
    a.append(b)
    b.append(a)
    del a, b
    gc.collect()
    print("   gc.garbage:", [type(o).__name__ for o in gc.garbage])
    gc.set_debug(0)
    gc.garbage.clear()


if __name__ == "__main__":
    print("Python", sys.version.split()[0])
    for f in (exp1_refcount, exp2_cycles, exp3_generations,
              exp4_callbacks, exp5_tracking, exp6_saveall):
        f()