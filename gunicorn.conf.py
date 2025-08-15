#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إعدادات Gunicorn لـ Render
"""

import os

# Worker configuration
workers = 1
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 2

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', 10000)}"
backlog = 2048

# Debugging
reload = False
preload_app = True

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "employee_management_system"

# Server mechanics
daemon = False
pidfile = None
user = None
group = None
tmp_upload_dir = None

# SSL
keyfile = None
certfile = None
