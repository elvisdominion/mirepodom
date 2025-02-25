from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

# Conexión a Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
