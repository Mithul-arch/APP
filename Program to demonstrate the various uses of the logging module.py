import logging
import logging.handlers
import sys
log = logging.getLogger("demo")
log.setLevel(logging.DEBUG)

console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO) 
console.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))

file_h = logging.handlers.RotatingFileHandler("demo.log", maxBytes=1000, backupCount=2)
file_h.setFormatter(logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s"))

log.addHandler(console)
log.addHandler(file_h)


class Redact(logging.Filter):  
    def filter(self, record):
        record.msg = str(record.msg).replace("hunter2", "******")
        return True


console.addFilter(Redact())


class Ctx(logging.LoggerAdapter):  
    def process(self, msg, kwargs):
        return f"[user={self.extra['user']}] {msg}", kwargs


log.debug("Debug goes to the file only")
log.info("Processing %d items", 3) 
log.warning("Password is hunter2")  
logging.getLogger("demo.db").error("Connection lost") 
Ctx(log, {"user": "alice"}).info("Adapter message")

try:
    1 / 0
except ZeroDivisionError:
    log.exception("Caught an error")  

print("\n--- demo.log ---")
print(open("demo.log").read())