-- Create master_satuan table
CREATE TABLE IF NOT EXISTS public.master_satuan (
    id BIGSERIAL PRIMARY KEY,
    nama_satuan VARCHAR(100) NOT NULL UNIQUE
);

-- Disable Row Level Security (RLS) - match other tables
ALTER TABLE public.master_satuan DISABLE ROW LEVEL SECURITY;

-- Insert some default units (skip if already exists)
INSERT INTO public.master_satuan (nama_satuan) VALUES
    ('pcs'),
    ('karton'),
    ('toples'),
    ('pouch'),
    ('pack'),
    ('bungkus'),
    ('keranjang')
ON CONFLICT (nama_satuan) DO NOTHING;