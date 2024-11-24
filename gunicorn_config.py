# # Error log
# errorlog = '/var/log/gunicorn_error.log'
# # Log level
# loglevel = 'debug'
# # Access log
# accesslog = '/var/log/gunicorn_access.log'
# # Access log format with request headers
# access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" "%(D)sμs" Request-Headers:"%({X-Forwarded-For}i)s %({X-Forwarded-Proto}i)s"'

forwarded_allow_ips = '*'
secure_scheme_headers = {'X-FORWARDED-PROTO': 'https'}