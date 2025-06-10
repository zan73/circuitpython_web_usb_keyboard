import board, digitalio, socketpool, time, wifi

class WebServer:
    def __init__(self, yield_timeout=1.0, buffer_bytes=2048, max_login_attempts=3, ban_duration=60):
        self.routes = {}  # {(path, method): callback}
        self.auth_sessions = {}  # ip -> True/False
        self.login_attempts = {}  # ip -> {fail_count, banned_until}
        self.yield_timeout = yield_timeout
        self.buffer_bytes = buffer_bytes
        self.max_login_attempts = max_login_attempts
        self.ban_duration = ban_duration * 60

    def route(self, path, method="GET"):
        """Decorator to register route callbacks."""
        def decorator(func):
            self.routes[(path, method.upper())] = func
            return func
        return decorator

    def too_many_attempts(self, ip):
        if ip in self.auth_sessions:
            del self.auth_sessions[ip]
        retVal = False
        info = self.login_attempts.get(ip, {"fail_count": 0, "banned_until": 0})
        info["fail_count"] += 1
        if info["fail_count"] > self.max_login_attempts:
            info["banned_until"] = time.time() + self.ban_duration
            print(f"Banned IP: {ip}")
            retVal = True
        self.login_attempts[ip] = info
        return retVal

    def auth_ip(self, ip):
        self.auth_sessions[ip] = True

    def reset_attempts(self, ip):
        if ip in self.login_attempts:
            del self.login_attempts[ip]

    def _url_decode(self, s):
        result = ""
        i = 0
        while i < len(s):
            if s[i] == "+":
                result += " "
                i += 1
            elif s[i] == "%" and i + 2 < len(s):
                try:
                    result += chr(int(s[i+1:i+3], 16))
                    i += 3
                except ValueError:
                    result += "%"
                    i += 1
            else:
                result += s[i]
                i += 1
        return result

    def _parse_form(self, body):
        form = {}
        for pair in body.split("&"):
            if "=" in pair:
                k, v = pair.split("=", 1)
                form[self._url_decode(k)] = self._url_decode(v)
        return form

    def start(self, port=80):
        try:
            pool = socketpool.SocketPool(wifi.radio)
            server = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
            server.setsockopt(pool.SOL_SOCKET, pool.SO_REUSEADDR, 1)
            server.bind(("0.0.0.0", port))
            server.listen(1)
            server.settimeout(self.yield_timeout)
            print(f"Web server listening on port {port}")
        except Exception as e:
            print(f"Web server start failed: {e}")
            return

        # Setup LED
        led = digitalio.DigitalInOut(board.LED)
        led.direction = digitalio.Direction.OUTPUT
        led_state = False
        last_toggle = time.monotonic()

        while True:
            try:
                conn = None

                # Toggle LED every 1 second
                now = time.monotonic()
                if now - last_toggle >= 1.0:
                    led_state = not led_state
                    led.value = led_state
                    last_toggle = now

                conn, addr = server.accept()
                client_ip = addr[0]                
                
                print(f"Client connected from {client_ip}")
                request = bytearray(self.buffer_bytes)
                conn.recv_into(request)
                request_str = request.rstrip(b"\x00").decode("utf-8")

                lines = request_str.split("\r\n")
                if not lines:
                    continue
                
                request_line = lines[0]
                method, path, _ = request_line.split()
                body = request_str.split("\r\n\r\n", 1)[-1] if "\r\n\r\n" in request_str else ""
                form_data = self._parse_form(body) if method.upper() == "POST" else {}

                callback = self.routes.get((path, method.upper()), None)
                if callback:
                    result = callback(path, form_data, client_ip)
                else:
                    result = "<h1>404 Not Found</h1>"

                if isinstance(result, tuple):
                    content_type, body = result
                else:
                    content_type, body = ("text/html", result)

                http_response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n{body}"
                conn.send(http_response.encode("utf-8"))

            except OSError as e:
                if hasattr(e, "errno") and e.errno not in (11, 116):  # EAGAIN, ETIMEDOUT
                    print(f"Socket error: {e}")
            except Exception as e:
                print(f"Error handling request: {e}")
            finally:
                if conn:
                    conn.close()