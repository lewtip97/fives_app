import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://aopzycsjuigsxhfaivao.supabase.co'
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFvcHp5Y3NqdWlnc3hoZmFpdmFvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDczMzgxNjMsImV4cCI6MjA2MjkxNDE2M30.t3Sn2Y9zA259k774UFz4lIS1zY0xjyHu3b0xW4w-Skg'

export const supabase = createClient(supabaseUrl, supabaseAnonKey)