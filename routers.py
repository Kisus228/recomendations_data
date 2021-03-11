from views import Ping, Execution, Healthcheck

routes = [
    ("GET", "/pingmodel", Ping, "ping"),
    ("POST", "/execmodel", Execution, "exec"),
    ("GET", "/healthcheck", Healthcheck, "healthcheck")
]
