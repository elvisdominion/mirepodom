import os

SUPABASE_URL = "https://mxwzqsuxyajmpydxsyxr.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im14d3pxc3V4eWFqbXB5ZHhzeXhyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDAxNTY3NzQsImV4cCI6MjA1NTczMjc3NH0.QKjfGeD0AFKIko0kz6vjIp-GK-yIn7aVYQ_J5stkGl8"


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecreto")
    SUPABASE_URL = SUPABASE_URL
    SUPABASE_KEY = SUPABASE_KEY
