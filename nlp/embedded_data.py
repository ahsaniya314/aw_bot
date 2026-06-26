"""
Data NLP tertanam — dihasilkan dari files/ via scripts/embed_nlp_data.py
Jangan edit manual kecuali patch kecil; regenerate dengan skrip di atas.
"""

NORMALIZATION_DICT = {
    "metadata": {
        "title": "Kamus Normalisasi & Sinonim untuk NLP Sales Chatbot (Merged)",
        "language": "id",
        "description": "Kamus untuk normalisasi teks sebelum diproses NLP, termasuk koreksi typo, sinonim, dan singkatan",
    },
    "typo_corrections": {
        "depang": "depan",
        "tampilan": "tampilkan",
        "edti": "edit",
        "paking": "paling",
        "cokalat": "coklat",
        "terbangak": "terbanyak",
        "kmarin": "kemarin",
        "kmrin": "kemarin",
        "kmaren": "kemarin",
        "bsk": "besok",
        "bsok": "besok",
        "plg": "paling",
        "hri": "hari",
        "laproan": "laporan",
        "lapuran": "laporan",
        "kemren": "kemarin",
        "lsa": "lusa",
        "bulu": "bulus",
        "ctn": "karton",
        "kartn": "karton",
        "krtn": "karton",
        "krton": "karton",
        "mnggu": "minggu",
        "snin": "senin",
        "slasa": "selasa",
        "rbu": "rabu",
        "kams": "kamis",
        "jmt": "jumat",
        "sbtu": "sabtu",
        "ahd": "ahad",
        "prmen": "permen",
        "wiilo": "willo",
        "tamhbahkan": "tambah",
        "wilo": "willo",
        "bembeng": "bemmbeng",
        "brownis": "brownies",
        "bngkus": "bungkus",
        "topls": "toples",
        "prduk": "produk",
        "brg": "barang",
        "hrga": "harga",
        "tuni": "tunai",
        "tghan": "tagihan",
        "taghn": "tagihan",
        "csh": "cash",
        "dbayar": "dibayar",
        "lgsung": "langsung",
        "dicicil": "dicicil",
        "ciciln": "cicilan",
        "kntan": "kontan",
        "tggakan": "tunggakan",
        "tggakn": "tunggakan",
        "hutng": "hutang",
        "blm": "belum",
        "sdh": "sudah",
        "udh": "sudah",
        "dah": "sudah",
        "udah": "sudah",
        "msh": "masih",
        "msih": "masih",
        "yg": "yang",
        "brp": "berapa",
        "jmlah": "jumlah",
        "smua": "semua",
        "sluruh": "seluruh",
        "pesen": "pesan",
        "pesnan": "pesanan",
        "ambl": "ambil",
        "bli": "beli",
        "byar": "bayar",
        "jt": "juta",
        "rb": "ribu",
        "tampilin": "tampilkan",
        "lhat": "lihat",
        "liatin": "lihat",
        "tamplkan": "tampilkan",
        "tampl": "tampilkan",
        "daftrkan": "daftarkan",
        "msukin": "masukkan",
        "perbahrui": "perbaharui",
        "perbarui": "perbaharui",
        "updte": "update",
        "gmn": "bagaimana",
        "bgmn": "bagaimana",
        "pnjualan": "penjualan",
        "penjulan": "penjualan",
        "tranksaksi": "transaksi",
        "trnsaksi": "transaksi",
        "ordr": "order",
        "riwyt": "riwayat",
        "cklat": "coklat",
        "bngkos": "bungkus",
        "lnas": "lunas",
        "suda": "sudah",
        "trus": "terus",
        "jngan": "jangan",
        "trbnyak": "terbanyak",
        "trbsar": "terbesar",
        "trbyk": "terbanyak",
        "nma": "nama",
        "pndapatan": "pendapatan",
        "pmasukan": "pemasukan",
        "ung": "uang",
        "penjlan": "penjualan",
        "oredre": "order",
        "oder": "order",
        "orde": "order",
        "ordder": "order",
        "ambi": "ambil",
        "ambill": "ambil",
        "nambil": "ambil",
        "ngambil": "ambil",
        "prmn": "permen",
        "permin": "permen",
        "premen": "permen",
        "borwnis": "brownis",
        "browni": "brownis",
        "brwnis": "brownis",
        "brownies": "brownis",
        "har": "hari",
        "haari": "hari",
        "luans": "lunas",
        "lunaz": "lunas",
        "lunass": "lunas",
        "tf": "transfer",
        "trf": "transfer",
        "tranfer": "transfer",
        "trnsfer": "transfer",
        "tnai": "tunai",
        "tuna": "tunai",
        "tunia": "tunai",
        "cash": "tunai",
        "ccil": "cicil",
        "cicl": "cicil",
        "cici": "cicil",
        "besokk": "besok",
        "kemrin": "kemarin",
        "kemarim": "kemarin",
        "mggu": "minggu",
        "minggu": "minggu",
        "topless": "toples",
        "topl": "toples",
        "bungks": "bungkus",
        "bungkuss": "bungkus",
        "bks": "bungkus",
        "bngks": "bungkus",
        "bungkos": "bungkus",
        "dpan": "depan",
        "dpen": "depan",
        "dpn": "depan",
    },
    "synonyms": {
        "aksi_tambah": [
            "tambah",
            "masukin",
            "input",
            "catat",
            "bikin",
            "tmb",
            "add",
            "tmbhin",
            "tambahkan",
            "masukkan",
            "daftarkan",
            "buat",
            "create",
            "simpan",
            "rekam",
            "tulis",
        ],
        "aksi_tampilkan": [
            "tampilkan",
            "lihat",
            "cek",
            "liat",
            "tampilin",
            "show",
            "tampilan",
            "tampil",
            "liatin",
            "rincian",
            "munculkan",
            "keluarkan",
            "display",
            "buka",
        ],
        "aksi_hapus": ["hapus", "delete", "buang", "del", "hilangin", "batalin", "apush", "remove", "clear", "hilangkan", "cancel"],
        "aksi_edit": [
            "edit",
            "ubah",
            "update",
            "ganti",
            "ralat",
            "edti",
            "updet",
            "updt",
            "perbaharui",
            "perbarui",
            "revisi",
            "koreksi",
            "modifikasi",
            "change",
        ],
        "aksi_cek": ["cek", "check", "lihat", "tampilkan", "info", "status", "berapa", "siapa", "apa", "gimana", "bagaimana"],
        "status_lunas": [
            "lunas",
            "sudah bayar",
            "dibayar",
            "cash",
            "tunai",
            "udah bayar",
            "dah bayar",
            "kontan",
            "sudah lunas",
            "sudah dibayar",
            "udah lunas",
            "telah dibayar",
            "telah lunas",
            "bayar penuh",
            "paid",
        ],
        "status_belum_lunas": [
            "belum lunas",
            "hutang",
            "utang",
            "ngutang",
            "bon",
            "cicil",
            "nyicil",
            "blm lunas",
            "blom lunas",
            "kasbon",
            "belum bayar",
            "belum dibayar",
            "masih hutang",
            "masih nyicil",
            "dp",
            "uang muka",
            "belum dilunasi",
            "masih ada sisa",
            "kurang bayar",
        ],
        "metode_cash": ["tunai", "cash", "kontan", "langsung", "bayar langsung", "bayar di tempat", "bayar tunai", "dibayar langsung"],
        "metode_transfer": [
            "transfer",
            "tf",
            "bank",
            "m-banking",
            "trf",
            "trnsfr",
            "via transfer",
            "via tf",
            "bayar transfer",
            "bayar tf",
            "dibayar transfer",
            "kirim",
            "kirim uang",
        ],
        "satuan_produk": {
            "permen": ["pcs", "bungkus", "toples", "dus", "buah", "pack", "sachet"],
            "brownis": ["bungkus", "toples", "buah", "pcs", "pack", "loyang"],
            "roti_pia": ["bungkus", "toples", "buah", "pcs", "pack"],
            "serbuk": ["bungkus", "sachet", "pcs", "dus", "pack"],
        },
        "waktu": {
            "hari_ini": ["hari ini", "hri ini", "sekarang", "today", "saat ini"],
            "kemarin": ["kemarin", "kmarin", "kemren", "hari kemarin", "yesterday"],
            "besok": ["besok", "bsok", "hari esok", "tomorrow"],
            "lusa": ["lusa", "lsa", "besok lusa", "2 hari lagi", "dua hari lagi"],
            "minggu_depan": ["minggu depan", "mnggu depan", "minggu depang", "pekan depan", "next week", "1 minggu lagi"],
            "kemarin_lusa": ["kemarin lusa", "2 hari lalu", "dua hari lalu"],
        },
        "sapaan_pelanggan": ["pak", "bu", "ibu", "bapak", "mas", "mba", "mbak", "bang", "kak", "om", "tante", "saudara", "bro", "sis"],
        "kata_produk": ["barang", "produk", "item", "dagangan", "jualaan", "komoditas", "stock", "stok"],
        "kata_transaksi": ["transaksi", "penjualan", "pembelian", "order", "pesanan", "pemesanan", "belanja", "beli", "ambil"],
        "kata_hutang": ["hutang", "utang", "tunggakan", "piutang", "tagihan", "cicilan", "sisa bayar", "sisa hutang", "belum lunas"],
    },
    "abbreviations": {
        "tf": "transfer",
        "trf": "transfer",
        "tgl": "tanggal",
        "bln": "bulan",
        "thn": "tahun",
        "brg": "barang",
        "jml": "jumlah",
        "pk": "pak",
        "bpk": "pak",
        "dp": "down payment",
        "lunas": "sudah lunas",
        "blm": "belum",
        "sdh": "sudah",
        "udh": "sudah",
        "udah": "sudah",
        "dah": "sudah",
        "msh": "masih",
        "yg": "yang",
        "brp": "berapa",
        "jt": "juta",
        "rb": "ribu",
        "k": "ribu",
        "pcs": "pieces",
        "lgsung": "langsung",
        "kntan": "kontan",
        "dg": "dengan",
        "dgn": "dengan",
        "utk": "untuk",
        "ttg": "tentang",
        "hr": "hari",
        "mgg": "minggu",
    },
    "entity_patterns": {
        "satuan": {
            "valid_units": [
                "dus",
                "karton",
                "pcs",
                "bks",
                "bungkus",
                "bal",
                "renceng",
                "box",
                "kg",
                "toples",
                "pack",
                "buah",
                "botol",
                "sachet",
                "loyang",
                "lusin",
                "pouch",
                "ctn",
                "paket",
            ],
        },
        "nama_pelanggan": {
            "description": "Pola untuk mengekstrak nama pelanggan dari teks",
            "prefix_patterns": ["pak", "bu", "ibu", "bapak", "mas", "mba", "mbak", "bang", "kak"],
            "action_keywords": ["ambil", "beli", "order", "pesan", "bayar", "transaksi", "pesanan", "tagihan", "hutang"],
        },
        "produk": {
            "description": "Daftar produk yang dikenal sistem",
            "known_products": [
                "permen",
                "permen coklat",
                "brownis",
                "brownies",
                "roti pia",
                "roti pia bulus",
                "serbuk",
                "permen cokalat",
                "willo",
                "beem-beeng",
                "adangrow",
                "siiperquuen",
                "chocholetus",
                "miksu",
                "lolipop",
                "coklat kubus",
                "piramide",
                "piramid",
                "mesis",
                "salju",
                "serbuk jelli",
            ],
        },
        "nominal_uang": {
            "description": "Pola untuk mengekstrak nominal uang",
            "patterns": ["\\d+", "\\d+ juta", "\\d+ ribu", "\\d+jt", "\\d+rb", "\\d+.\\d+", "\\d+,\\d+"],
            "multipliers": {
                "juta": 1000000,
                "jt": 1000000,
                "ribu": 1000,
                "rb": 1000,
                "k": 1000,
            },
        },
        "tanggal": {
            "description": "Pola untuk mengekstrak tanggal",
            "patterns": ["tanggal \\d+", "tgl \\d+", "\\d+ \\w+ \\d{4}", "\\d{2}/\\d{2}/\\d{4}", "\\d{2}-\\d{2}-\\d{4}"],
        },
    },
}

INTENT_PATTERNS = {
    "greeting": [
        "hallo",
        "halo",
        "helo",
        "hello",
        "hai",
        "hi",
        "hey",
        "hei",
        "selamat pagi",
        "selamat siang",
        "selamat sore",
        "selamat malam",
        "assalamualaikum",
        "assalamualaikum wr wb",
        "met pagi",
        "met siang",
        "met sore",
        "permisi",
        "halo bot",
        "hai bot",
        "hallo semuanya",
        "halo ada yang bisa bantu",
        "hai bisa bantu saya",
        "hei ada orang",
        "apa kabar",
        "p kabar",
        "apakabar",
        "helo bos",
        "halo bro",
        "hai kak",
        "hei gan",
        "hlo",
        "hlw",
        "haloo",
        "halloo",
        "halooo",
        "om swastiastu",
        "salam",
        "salam kenal",
        "p",
        "wuy",
        "pagi",
        "siang",
        "sore",
        "malam",
        "assalamu'alaikum",
        "wassalamu'alaikum",
        "ada orang",
        "helloo",
        "haii",
        "hie",
        "slmat pagi",
        "selamat apgi",
        "helo bot",
        "hai bott",
    ],
    "cek_penjualan_hari_ini": [
        "cek penjualan hari ini",
        "total penjualan hari ini",
        "omzet hari ini",
        "berapa laku hari ini",
        "cek data penjualan",
        "tampilkan data penjualan",
        "tampilan data penjualan hari ini",
        "tampilan data penjualan kemarin",
        "tampilan data penjualan lusa",
        "gimana penjualan hari ini",
        "penjualan hari ini gimana",
        "laporan penjualan hari ini",
        "ringkasan penjualan hari ini",
        "summary penjualan hari ini",
        "rekap penjualan hari ini",
        "penjualan hari ini bagaimana",
        "update penjualan hari ini",
        "info penjualan hari ini",
        "cek pnjualan hari ini",
        "gmn penjualan hri ini",
        "laporan pnjualan hri ini",
        "rekap pnjualan hri ini",
        "hari ini penjualan gimana",
        "ada berapa penjualan hari ini",
        "penjualan hari ini ada berapa",
        "tampilkan data penjualan hari ini",
        "lihat data penjualan hari ini",
    ],
    "tampilkan_semua_transaksi": [
        "tampilkan semua data penjualan",
        "lihat semua transaksi",
        "cek semua pesanan",
        "tampilkan seluruh data",
        "lihat semua data",
        "tampilan semua transaksi",
        "tampilan semua data",
        "tampilan semua pembelian",
        "tampilkan semua transaksi pak andi",
        "hapus/tampilkan semua data",
        "cek data penjualan",
        "cek penjualan",
        "lihat data penjualan",
        "tampilkan data penjualan",
        "tampilkan semua data",
        "tampilkan semua penjualan",
        "tampil semua transaksi",
        "show semua transaksi",
        "list semua penjualan",
        "daftar penjualan semua",
        "tampilkan daftar transaksi",
        "cek semua transaksi",
        "cek semua penjualan",
        "tampilkan rekap penjualan",
        "rekap semua transaksi",
        "tampilkan riwayat transaksi",
        "riwayat penjualan semua",
        "tampilin semua transaksi",
        "tampilin data penjualan",
        "liatin semua transaksi",
        "munculkan semua transaksi",
        "keluarkan data penjualan semua",
        "tampilkan seluruh transaksi",
        "tampilkan sluruh penjualan",
        "tamplkan semua transaksi",
        "tampilan smua transaksi",
        "lhat semua transaksi",
        "cek smua penjualan",
        "rekap tranksaksi semua",
        "daftar penjlan semua",
        "tampilin daftar tranksaksi",
        "liat smua transaksi",
        "tampilkan semua data transaksi",
        "tampilkan seluruh data penjualan",
        "tampilkan histori transaksi",
        "show all transaksi",
        "data penjualan semua",
        "semua data transaksi",
        "semua transaksi ada apa aja",
        "tampilkan semua daftar penjualan",
        "tampil semua daftar penjualan",
        "lihat semua daftar penjualan",
        "tampilkan semua transaksi",
        "tampilkan data penjualan lusa",
        "tampilkan semua transaksi/data/pembelian pak andi",
        "tampilkan semua data pak andi",
        "tampilkan semua pembelian pak andi",
        "tampilkaan semua data penjualan",
        "liht semua daftar penjualan",
        "tampilkan semua tranksi",
        "tampilkan dat penjualan",
        "liat semua transaksi",
        "print semua data penjualan",
        "tampung semua transaksi",
        "daftar semua penjualan",
        "list semua transaksi",
    ],
    "tampilkan_transaksi_hari_ini": [
        "tampilkan transaksi hari ini",
        "cek pesanan hari ini",
        "lihat data hari ini",
        "siapa yang pesan hari ini",
        "cek pesanan hari ini",
        "siapa yang order hari ini",
        "lihat transaksi hari ini",
        "cek transaksi hari ini",
        "transaksi hari ini apa saja",
        "siapa beli hari ini",
        "siapa yang beli hari ini",
        "siapa yang ambil barang hari ini",
        "daftar penjualan hari ini",
        "rekap hari ini",
        "penjualan hari ini",
        "laporan hari ini",
        "data penjualan hari ini",
        "order hari ini",
        "pembelian hari ini",
        "transaksi hri ini",
        "cek penjulan hri ini",
        "tampilin transaksi hri ini",
        "lhat penjualan hri ini",
        "cek pesanan hri ini",
        "siapa yg pesan hri ini",
        "siapa yg order hri ini",
        "daftar penjulan hri ini",
        "penjulan hari ini",
        "rekap hri ini",
        "laporan hri ini",
        "data penjulan hri ini",
        "order hri ini",
        "hari ini ada transaksi apa",
        "hari ini siapa yang beli",
        "siapa yg beli hri ini",
        "transaksi apa aja hari ini",
        "hari ini ada order apa aja",
        "siapa pesan barang hari ini",
        "lihat pesanan hari ini",
        "tampilkan pesanan hari ini",
        "liat transaksi hari ini",
    ],
    "tampilkan_transaksi_kemarin": [
        "tampilkan data penjualan kemarin",
        "tampilan data penjualan kemarin",
        "cek transaksi kemarin",
        "lihat transaksi kemarin",
        "daftar penjualan kemarin",
        "rekap kemarin",
        "penjualan kemarin",
        "order kemarin ada apa aja",
        "siapa yang beli kemarin",
        "siapa yang order kemarin",
        "laporan kemarin",
        "transaksi kemarin",
        "cek penjualan kemarin",
        "tampilkan transaksi kemarin",
        "data penjualan kemarin",
        "kemarin ada order apa",
        "kemarin siapa yang beli",
        "pembelian kemarin",
        "tampilin transaksi kmarin",
        "lhat penjualan kmarin",
        "cek transaksi kmarin",
        "daftar penjulan kmarin",
        "rekap kmarin",
        "penjulan kmarin",
        "kemren ada order apa",
        "kemren siapa yg beli",
        "laporan kmarin",
        "transaksi kmarin",
        "cek penjulan kmarin",
        "data penjulan kmarin",
    ],
    "tampilkan_transaksi_tanggal": [
        "cek/tampilkan pesanan tanggal 21 04 2026",
        "cek pesanan tanggal 21",
        "tampilkan transaksi tanggal 28",
        "lihat penjualan tanggal 15",
        "transaksi tanggal 20",
        "penjualan tanggal 25",
        "rekap tanggal 10",
        "data penjualan tanggal 5",
        "order tanggal 14",
        "cek transaksi tanggal 21",
        "tampilkan penjualan tanggal 21 april",
        "data tanggal 21 04",
        "transaksi tanggal 21 bulan 4",
        "penjualan 21 april 2026",
        "tampilkan data tanggal 28",
        "cek data tanggal 15",
        "lihat transaksi tanggal 20 april",
        "tampilkan order tanggal 25",
        "rekap penjualan tanggal 10",
        "data pembelian tanggal 5 mei",
        "cek pesnan tanggal 21 04 2026",
        "cek pesnan tanggal 21",
        "tampilkan transaksi tgl 28",
        "lhat penjualan tgl 15",
        "transaksi tgl 20",
        "penjulan tgl 25",
        "rekap tgl 10",
        "data penjulan tgl 5",
        "order tgl 14",
        "cek transaksi tgl 21",
        "tampilkan penjulan tgl 21 april",
        "data tgl 21 04",
        "transaksi tgl 21 bln 4",
        "penjulan 21 april 2026",
        "tampilkan data tgl 28",
        "cek data tgl 15",
        "tanggal 21 ada transaksi apa",
        "tanggal 28 ada order apa",
        "tgl 21 siapa yang beli",
        "tgl 28 ada pesanan apa",
        "cek pesanan tanggal 21 april 2026",
        "tampilkan pesanan tanggal 21 april",
        "lihat transaksi tanggal 28",
        "data tanggal 28",
        "pesanan tanggal 28",
        "tampiln transaksi tanggal 28",
    ],
    "cek_pesanan_pelanggan": [
        "cek pesanan pak budi",
        "tampilkan transaksi udin",
        "lihat pesanan pak edi",
        "pesanan pak ardi",
        "cek pesanan pak andi",
        "tampilkan jumlah pesanan dari pak andi",
        "cek pesanan udin",
        "cek transaksi udin",
        "tampilan semua transaksi pak andi",
        "tampilkan semua transaksi pak andi",
        "lihat pesanan pak andi",
        "tampilkan pesanan pak andi",
        "data transaksi pak andi",
        "riwayat pesanan pak andi",
        "order pak andi",
        "pesanan pak budi",
        "cek pesanan pak hendra",
        "tampilkan transaksi pak joko",
        "data pembelian pak rudi",
        "lihat order pak doni",
        "pesanan ibu sari",
        "cek transaksi ibu maya",
        "data pesanan mba rina",
        "tampilan smua transaksi pak andi",
        "tampilkan smua transaksi pak andi",
        "cek pesnan pak andi",
        "cek pesnan pak ardi",
        "pesnan pak ardi",
        "cek pesnan udin",
        "lhat pesanan pak andi",
        "tampilin pesanan pak andi",
        "riwayat pesnan pak andi",
        "pesnan pak budi",
        "cek pesnan pak hendra",
        "lhat order pak doni",
        "pesnan ibu sari",
        "data pesnan mba rina",
        "berapa pesanan pak andi",
        "total pesanan pak budi",
        "berapa transaksi pak ardi",
        "transaksi pak ardi apa aja",
        "pak andi beli apa saja",
        "tampilkan jumlah pesanan pak andi",
        "riwayat pesanan pak ardi",
        "Cek pesanan/transaksi udin",
        "lihat transaksi udin",
        "riwayat udin",
        "pesanan pak ardi hari ini",
        "liat pesanan udin",
        "lht riwayat pak andi",
    ],
    "tambah_transaksi_lunas_cash": [
        "hari ini pak andi order barang 50 pcs berupa permen",
        "hari ini pak agus ambil permen coklat 2 dus",
        "kemarin pak ardi ambil barang 100 buah brownis sudah dibayar tunai",
        "besok pak ardi ambil barang 100 buah brownis sudah dibayar",
        "lusa pak ardi ambil barang 100 buah brownis sudah dibayar tunai",
        "hari ini udin ambil permen 30 dus sudah lunas",
        "hari ini rara ambil permen coklat 13 dus dibayar lunas secara cash",
        "hari ini supri ambil permen 20 toples sudah lunas",
        "hari ini rudi order permen 600 toples sudah lunas",
        "pak andi beli permen 50 pcs hari ini lunas",
        "pak agus pesan permen coklat 2 dus hari ini cash",
        "hari ini nana beli brownis 10 bungkus bayar tunai",
        "tadi pak budi ambil roti pia 5 toples bayar cash",
        "siang ini pak soni order permen 100 toples sudah bayar",
        "hari ini pak doni ambil brownis 20 bungkus lunas tunai",
        "pak hendra pesan permen coklat 3 dus hari ini sudah lunas cash",
        "hari ini ibu sari beli permen 50 toples bayar langsung",
        "ibu ani ambil brownis 15 bungkus hari ini bayar cash lunas",
        "hari ini mas yudi order permen 30 pcs sudah dibayar",
        "pak joko ambil permen 25 toples hari ini bayar di tempat",
        "hari ini pak rahmat beli brownis 10 bungkus lunas bayar kontan",
        "hari ini pak umar pesan permen 45 pcs bayar tunai",
        "hari ini ibu dewi order brownis 12 bungkus lunas cash",
        "budi beli permen 30 tples lunas tdi",
        "pak andi pesan prmen 50 pcs hari ini udah lunas csh",
        "hri ini supri ambil prmen 20 topls sudah lunas",
        "pak agus ambl permen cklat 2 dus hri ini cash",
        "hari ini pak dedi order peremen 100 pcs lunas bayar langsung",
        "hr ini pak soni ambil brownis 25 bungkos lunas tunai",
        "pak jono ambl permen 30 toples hri ini dah bayar",
        "hari ini mba lina pesan permen coklat 5 dus bayar tuni",
        "pak tono beli brownis 8 bungkos hr ini lunas cash",
        "hari ini pak andi pesan permen 50 pcs",
        "hari ini pak agus ngambil permen coklat 2 dus",
        "hari ini rara ambil permen coklat 13 dus lunas cash",
        "hari ini udin ngambil permen 30 dus lunas",
        "hari ini rudi order permen 600 toples lunas",
        "hari ini supri ambil permen 20 toples lunas",
        "minggu dpan ardi ambil brownis 100 lunas",
        "hari ini pak andi oredre permen 50 pcs",
        "hri ini pak andi order prmen 50 pcs",
        "hari ini paka andi order permen 50 pcs",
        "hari ni pak andi order permen 50 pcs lunas",
        "hari ini budi ambl brownis 30 bungkus luans",
        "kemrin ardi ambil brownis 100 udah bayar tnai",
        "minggu dpan ardi ambl brownis 100 lunas tunai",
        "hari ini supri ambil permen 20 topls sudah lunas",
        "tadi andi beli permen 50 pcs lunas cash",
        "pak agus pesan permen coklat 2 dus hari ini",
        "pak agus beli permen coklat 2 dus hari ini",
        "pak agus transaksi permen coklat 2 dus hari ini lunas",
        "catat pesanan pak andi permen 50 pcs hari ini lunas cash",
        "input transaksi pak andi permen 50 pcs hari ini lunas",
        "tambah transaksi pak andi permen 50 pcs hari ini",
        "simpan transaksi pak andi permen 50 pcs hari ini lunas",
        "rekap pak andi beli permen 50 pcs hari ini lunas",
    ],
    "tambah_transaksi_lunas_transfer": [
        "hari ini naha ambil permen 50 dus sudah lunas dibayar secara transfer",
        "hari ini nala ambil serbuk 100 lunas dibayar secara transfer",
        "hari ini udin ambil permen 30 dus sudah lunas",
        "hari ini rudi order permen 600 toples sudah lunas",
        "pak budi beli brownis 20 bungkus hari ini lunas transfer",
        "hari ini ibu siti ambil permen 40 toples lunas bayar tf",
        "hari ini pak hadi pesan brownis 15 bungkus sudah lunas via transfer",
        "mba rina order permen coklat 10 dus hari ini lunas tf",
        "hari ini pak deni ambil brownis 30 bungkus sudah dibayar transfer",
        "pak wahyu pesan permen 60 toples hari ini lunas via tf",
        "hari ini ibu maya beli brownis 25 bungkus lunas transfer",
        "pak yanto order permen 80 toples hari ini sudah bayar transfer",
        "hari ini mba nita ambil permen coklat 8 dus lunas tf",
        "pak tanto beli brownis 12 bungkus hri ini lunas tranfer",
        "hari ini ibu wati pesan prmen 35 toples sudah lunas tf",
        "pak rendi order brownis 18 bungkus hr ini lunas via transfr",
        "naha ambil permen 50 dus hri ini lunas dibayar tranfer",
        "udin ambil prmen 30 dus hri ini lunas",
        "pak hdi pesen brownis 15 bungkus hari ini lunas trf",
        "mba rina order prmen cklat 10 dus hr ini lunas tf",
        "pak deni ambil brownis 30 bngkus hari ini dah dibayar transfer",
        "hari ini pak sobri pesan permen 100 toples sudah lunas tf",
        "bu lestari ambil brownis 20 bungkus hari ini lunas transfer",
        "hari ini mas fajar beli permen 45 pcs sudah lunas via tf",
        "pak mulyono order brownis 50 bungkus hari ini lunas bayar tf",
        "hari ini naha ambil permen 50 dus lunas transfer",
        "hari ini nala ambil serbuk 100 lunas tf",
        "hari ini nala ambl srbuk 100 lunas transfer",
    ],
    "tambah_transaksi_cicilan_cash": [
        "hari ini rudi order permen 600 toples dicicil 200000 sudah dibayar",
        "hari ini rudi order permen 600 toples dicicil 200000 cash",
        "hari ini budi order permen 30 toples dicicil 200000 dibayar langsung",
        "hari ini andi order permen 600 toples dicicil 200000 tunai",
        "hari ini rudi order permen 600 toples dicicil 200000 bayar langsung",
        "pak soni beli brownis 50 bungkus dp 100000 bayar cash",
        "hari ini pak doni order permen 80 toples cicil 150000 tunai",
        "mba ani pesan brownis 25 bungkus dicicil 50000 bayar langsung",
        "hari ini pak hendra beli permen 100 toples cicilan 200000 cash",
        "pak joko order brownis 30 bungkus dicicil 75000 bayar kontan",
        "hari ini pak umar pesan permen 45 toples dp 100000 tunai",
        "ibu sari ambil brownis 20 bungkus cicil 50000 bayar langsung",
        "hari ini pak rahmat order permen 60 toples dicicil 120000 cash",
        "pak yudi beli brownis 15 bungkus dicicil 30000 bayar tunai",
        "hari ini pak rudi beli permen 200 toples dicicil 500000 bayar cash",
        "budi order prmen 30 topls dicicil 200000 dbayar lgsung",
        "andi order prmen 600 topls dicicil 200000 tuni",
        "rudi order prmen 600 topls dicicil 200000 csh",
        "pak soni bli brownis 50 bngkus dp 100000 byar cash",
        "pak doni order prmen 80 topls cicil 150000 tuni",
        "mba ani pesen brownis 25 bngkus dicicil 50000 byar lgsung",
        "hri ini pak hendra beli prmen 100 topls ciciln 200000 csh",
        "pak joko order brownis 30 bngkus dicicil 75000 byar kntan",
        "hari ini pak sumar pesan permen 200 toples dicicil 400000 bayar kontan",
        "bu endah ambil brownis 40 bungkus cicil 80000 tunai",
        "hari ini rudi order permen 600 toples cicil 200000 lunas",
        "hari ini rudi order permen 600 toples cicil 200000 tunai",
        "hari ini budi order permen 30 toples cicil 200000 cash langsung",
        "hari ini andi order permen 600 toples cicil 200000 cash",
        "hari ini rudi order permen 600 toples cicil 200000 langsung",
    ],
    "tambah_transaksi_cicilan_transfer": [
        "hari ini nala ambil permen 70 dus dicicil 2000000 dibayar secara transfer",
        "hari ini nala ambil brownis 100 bungkus dicicil 1000000 dibayar secara transfer",
        "hari ini rudi order permen 600 toples dicicil 200000 tf",
        "hari ini rudi order permen 600 toples dicicil 200000 sudah dibayar",
        "pak wahyu beli brownis 50 bungkus dicicil 500000 bayar tf",
        "hari ini ibu maya pesan permen 80 toples cicil 200000 via transfer",
        "pak hadi order brownis 30 bungkus dicicil 150000 bayar transfer",
        "hari ini mba nita beli permen 60 toples dicicil 120000 tf",
        "pak rendi pesan brownis 40 bungkus cicilan 200000 transfer",
        "hari ini pak tanto order permen 100 toples dicicil 300000 via tf",
        "bu wati ambil brownis 25 bungkus dicicil 75000 bayar tf",
        "hari ini pak yanto beli permen 90 toples cicil 180000 transfer",
        "nala ambil prmen 70 dus dicicil 2000000 dbayar secra tranfer",
        "nala ambil brownis 100 bngkus dicicil 1000000 dbayar secra tranfer",
        "rudi order prmen 600 topls dicicil 200000 tf",
        "rudi order prmen 600 topls dicicil 200000 sudh dibayar",
        "pak wahyu bli brownis 50 bngkus dicicil 500000 byar tf",
        "ibu maya pesen prmen 80 topls cicil 200000 via transfr",
        "pak hadi order brownis 30 bngkus dicicil 150000 byar tranfer",
        "mba nita bli prmen 60 topls dicicil 120000 tf",
        "pak rendi pesen brownis 40 bngkus ciciln 200000 transfr",
        "pak tanto order prmen 100 topls dicicil 300000 via tf",
        "hari ini pak samsudin pesan brownis 200 bungkus dicicil 500000 tf",
        "bu kartini ambil permen 150 toples cicil 300000 via transfer",
        "hari ini nala ambil permen 70 dus cicil 2000000 tf",
        "hari ini nala ambil brownis 100 bungkus cicil 1000000 transfer",
        "hari ini rudi order permen 600 toples cicil 200000 transfer",
        "hri ini rudi ordr permen 600 toples cicil 200000 tf",
    ],
    "tambah_transaksi_tanggal_spesifik": [
        "kemarin pak ardi ambil barang 100 buah brownis sudah dibayar tunai",
        "besok pak ardi ambil barang 100 buah brownis sudah dibayar",
        "lusa pak ardi ambil barang 100 buah brownis sudah dibayar tunai",
        "3 hari yang lalu pak ardi ambil barang 100 buah brownis udah dibayar tunai",
        "3 hari kedepan pak ardi ambil barang 100 buah brownis udah dibayar tunai",
        "minggu depan pak ardi ambil barang 100 buah brownis udah dibayar tunai",
        "minggu depang pak ardi ambil barang 100 buah brownis udah dibayar tunai",
        "hari minggu pak ardi ambil barang 100 buah brownis udah dibayar tunai",
        "hari senin pak ardi ambil barang 100 buah brownis udah dibayar tunai",
        "1 minggu lagi pak ardi ambil barang 100 buah brownis udah dibayar tunai",
        "kemarin pak budi beli permen 50 toples lunas tunai",
        "kemarin ibu sari pesan brownis 20 bungkus sudah bayar cash",
        "besok pak doni ambil permen 30 toples sudah lunas",
        "lusa pak hendra order brownis 15 bungkus lunas transfer",
        "minggu depan pak wahyu beli permen 100 toples sudah dibayar tf",
        "2 hari lalu pak rudi ambil brownis 50 bungkus lunas tunai",
        "kemren pak ardi ambl brownis 100 buah udah dibayar",
        "bsok pak ardi ambil brownis 100 buah sudah dibayar",
        "lusa pak ardi ambil brownis 100 buah lunas",
        "3 hri lalu pak ardi ambl brownis 100 buah udah dibayar tuni",
        "3 hri kedepan pak ardi ambil brownis 100 buah lunas",
        "mnggu depan pak ardi ambl brownis 100 buah sudah dibayar tf",
        "hari mnggu pak ardi ambil brownis 100 buah dah dibayar",
        "hari snin pak ardi ambil brownis 100 buah udah lunas",
        "1 mnggu lagi pak ardi ambil brownis 100 buah sudah dibayar",
        "3 hari ke depan pak soni pesan permen 60 toples lunas tf",
        "minggu depan ibu dewi ambil brownis 25 bungkus sudah bayar",
        "kemarin pak ardi beli brownis 100 buah lunas cash",
        "kemarin ardi ambil brownis 100 udah bayar tunai",
        "besok ardi ambil brownis 100 buah lunas",
        "lusa ardi ambil brownis 100 buah lunas cash",
        "3 hari lalu ardi ambil brownis 100 lunas tunai",
        "2 hari yang lalu budi ambil permen 50 dus lunas",
        "3 hari ke depan ardi ambil brownis 100 lunas",
        "1 minggu ke depan ardi ambil brownis 100 lunas",
        "hari selasa pak ardi ambil brownis 100 lunas",
        "hari rabu naha ambil permen 50 dus lunas transfer",
    ],
    "hapus_transaksi": [
        "hapus semua data penjualan",
        "hapus semua daftar penjualan",
        "hapus semua transaksi",
        "hapus pesanan udin dengan status pembayaran belum lunas",
        "hapus pesanan udin",
        "hapus transaksi udin",
        "delete semua transaksi",
        "hapus data penjualan",
        "hapus transaksi pak andi",
        "hapus pesanan pak budi",
        "hapus order pak rudi",
        "hapus data pak hendra",
        "hapus transaksi pak joko",
        "hapus semua order",
        "hapus seluruh transaksi",
        "hapus rekap penjualan",
        "hapus smua data penjualan",
        "hapus smua data transaksi",
        "hapus pesnan udin dg status pembayaran blm lunas",
        "hapus pesnan udin",
        "hapus transaksi udin",
        "hapus smua transaksi",
        "hapus data penjulan",
        "hapus transaksi pak andi",
        "hapus pesnan pak budi",
        "hapus order pak rudi",
        "hapus data pak hendra",
        "hapus transaksi pak joko",
        "hapus smua order",
        "hapus seluruh transaksi",
        "delete smua transaksi",
        "buang semua data penjualan",
        "buang transaksi pak andi",
        "clear semua transaksi",
        "hapus histori penjualan",
        "hapus riwayat transaksi",
        "hapus riwayat pesanan pak ardi",
        "Hapus semua data penjualan/transaksi",
        "hapus semua data/daftar penjualan",
        "hapus semua data",
        "hapus seluruh data penjualan",
        "hapus semua rekap penjualan",
        "hapus pesanan udin belum lunas",
        "hapus transaksi udin belum lunas",
        "hapus pesanan/transaksi udin",
        "Hapus/tampilkan semua data",
        "hapus data udin",
        "hapus pesanan pak ardi",
        "hapus data pak andi",
        "hapus pembelian pak andi",
        "hapus semwa data penjualan",
        "hapus semu transaksi",
        "hapus penjualan udin",
        "hapus pesenan udin",
        "hpus semua data penjualan",
        "hapus pesanaan pak ardi",
        "hps semua transaksi",
        "hapus semua dat penjualan",
        "hapus transaks udin",
        "remove pesanan udin",
        "clear semua data penjualan",
        "bersihkan semua data penjualan",
        "hilangkan semua transaksi",
        "hapusin semua data penjualan",
        "hapusin pesanan udin",
    ],
    "update_transaksi": [
        "update pesanan naha",
        "update transaksi naha",
        "perbaharui pesanan pak naha",
        "ubah pesanan pak naha",
        "edit pesanan pak naha",
        "perbaharui transaksi zio",
        "ubah transaksi pak andi",
        "edit transaksi pak budi",
        "update transaksi pak rudi",
        "perbaharui order pak hendra",
        "edit order pak joko",
        "ubah order pak doni",
        "ganti data transaksi pak soni",
        "perbarui pesanan ibu sari",
        "ubah data pesanan pak wahyu",
        "edit data transaksi ibu maya",
        "update order mba rina",
        "perbaharui data pembelian pak rendi",
        "perbarui data pak tanto",
        "update data pesnan naha",
        "perbahrui pesnan pak naha",
        "perbahrui transaksi zio",
        "ubah pesnan pak naha",
        "edit pesnan pak naha",
        "ubah transaksi pak andi",
        "edit transaksi pak budi",
        "update transaksi pak rudi",
        "perbahrui order pak hendra",
        "edit order pak joko",
        "ubah order pak doni",
        "ganti data transaksi pak soni",
        "perbarui pesnan ibu sari",
        "ubah data pesnan pak wahyu",
        "edit data transaksi ibu maya",
        "update order mba rina",
        "Update pesanan/transaksi naha",
        "Perbaharui/ubah/edit pesanan pak naha",
        "edit transaksi zio",
        "ubah transaksi zio",
        "update data pak ardi",
        "ubah data pesanan pak ardi",
        "edit data pesanan pak andi",
        "perbarui pesanan pak andi",
        "ganti status pesanan pak andi",
        "ganti status bayar pak andi jadi lunas",
        "ubah status bayar naha jadi lunas",
        "edit status pembayaran udin",
        "zio bayar 27000000 tf",
        "updaet pesanan naha",
        "update pesanaan naha",
        "perbaharui pesenan pak naha",
        "edti transaksi zio",
        "edit transaks zio",
        "ubah transksi pak ardi",
        "update dat pak ardi",
        "zio byr hutang 27 juta tf",
        "modify pesanan naha",
        "revisi pesanan pak naha",
        "koreksi transaksi zio",
        "change data pesanan pak ardi",
        "ganti data transaksi pak andi",
    ],
    "tampilkan_produk": [
        "daftar barang",
        "lihat produk",
        "cek stok barang",
        "tampilkan semua barang",
        "cek/tampilkan harga barang/produk",
        "tampilkan semua produk",
        "tampilkan daftar harga barang",
        "cek harga permen",
        "cek harga barang",
        "tampilkan harga barang",
        "tampilkan harga produk",
        "cek tampilkan harga barang",
        "daftar produk",
        "lihat barang",
        "tampilkan produk",
        "tampilkan barang",
        "list produk",
        "list barang",
        "cek produk",
        "cek barang",
        "produk apa saja",
        "barang apa saja yang ada",
        "ada barang apa saja",
        "tampilkan katalog produk",
        "cek harga prmen",
        "cek harga brg",
        "tampilkan harga brg",
        "tampilkan harga prduk",
        "tampilkan daftar harga brg",
        "tampilkan smua brg",
        "tampilkan smua prduk",
        "daftar prduk",
        "daftar brg",
        "lhat prduk",
        "lhat brg",
        "tampilin prduk",
        "tampilin brg",
        "list prduk",
        "list brg",
        "cek prduk",
        "cek brg",
        "prduk apa aja",
        "brg apa aja yang ada",
        "ada brg apa aja",
        "tampilkan katalog prduk",
        "cek harga produk",
        "tampil semua barang/produk",
        "lihat daftar harga barang",
        "lihat semua produk",
        "produk apa yang paling mahal",
        "cek hraga permen",
        "tampilkan hrga barang",
        "cek hrga produk",
        "berapa hraga permen",
        "berapa hrga brownis",
        "tampilkan semua barng",
        "liat semua produk",
        "tampilkn daftar harga",
        "show harga barang",
        "print daftar produk",
        "info harga barang",
        "info produk",
    ],
    "cek_harga_produk_spesifik": [
        "cek harga permen",
        "tampilkan harga brownis",
        "berapa harga permen",
        "berapa harga produk tertinggi",
        "harga brownis",
        "berapa harga brownis",
        "harga permen",
        "cek harga brownis",
        "berapa harga roti pia",
        "harga roti pia",
        "cek harga roti pia",
        "berapa harga permen coklat",
        "harga permen coklat",
        "berapa harga serbuk",
        "harga serbuk",
        "cek harga serbuk",
        "produk paling mahal",
        "barang paling mahal",
        "harga tertinggi",
        "produk termahal",
        "harga terendah",
        "produk termurah",
        "brp harga permen",
        "brp harga brownis",
        "harga brownis brp",
        "hrga brownis",
        "hrga permen",
        "cek hrga brownis",
        "brp harga roti pia",
        "hrga roti pia",
        "cek hrga roti pia",
        "brp harga permen coklat",
        "hrga permen coklat",
        "brp harga serbuk",
        "hrga serbuk",
        "cek hrga serbuk",
        "brp harga prduk tertinggi",
        "prduk paling mahal",
        "brg paling mahal",
        "harga brownis berapa",
        "lihat harga brownis",
        "harga produk tertinggi",
        "harga termahal",
        "liat harga permen",
    ],
    "tambah_produk": [
        "tambah barang permen coklat",
        "tambah produk permen coklat",
        "tambah barang",
        "tambah produk",
        "tambah produk permen coklat harga 13.000",
        "tambah barang brownis harga 2500 per toples",
        "tambah barang brownis harga 2500 per bungkus",
        "tambah barang roti pia bulus",
        "tambah barang permen cokalat",
        "tambah barang produk permen coklat",
        "tambah produk permen coklat harga 13000",
        "tambah produk baru",
        "tambah barang baru",
        "daftarkan produk permen",
        "daftarkan barang brownis",
        "input produk permen coklat 13000",
        "input barang brownis 2500",
        "masukkan produk baru permen coklat",
        "masukkan barang baru brownis",
        "add produk permen",
        "add barang brownis",
        "tambahkan produk permen coklat harga 13000",
        "tambahkan barang brownis harga 2500",
        "buat produk baru permen coklat 13000",
        "tamb barang prmen coklat",
        "tamb barang prduk prmen coklat",
        "tamb prduk prmen coklat hrga 13000",
        "tamb barang brownis hrga 2500 per topls",
        "tamb barang brownis hrga 2500 per bngkus",
        "tamb barang roti pia bulus",
        "tamb prduk baru",
        "tamb brg baru",
        "daftrkan prduk prmen",
        "daftrkan brg brownis",
        "input prduk prmen coklat 13000",
        "input brg brownis 2500",
        "msukin prduk baru prmen coklat",
        "msukin brg baru brownis",
        "tambah barang prmen cklat harga 13.000",
        "tambah produk brownis harga 2.500",
        "Tambah barang/produk permen coklat",
        "tambah barang/produk",
        "tambah barang permen coklat harga 13000",
        "tambah barang brownis harga 2500 toples",
        "tambah produk brownis 2500 per toples",
        "tambah barang brownis harga 2500 bungkus",
        "tambah produk roti pia bulus",
        "input produk baru permen coklat harga 13000",
        "input barang baru brownis 2500",
        "tambah item permen coklat harga 13000",
        "daftarkan produk permen coklat harga 13000",
        "masukkan barang brownis harga 2500",
        "tambh barang permen coklat",
        "tambah barang premen coklat",
        "tamabah produk permen coklat",
        "tamabah barang brownis harga 2500",
        "tambah brg brownis harga 2500",
        "tambah barang bornwis harga 2500",
        "tambah produk rmeni coklat harga 13000",
        "tamabh barang roti pia",
        "tambah barang/produk permen cokalat",
        "add barang permen coklat harga 13000",
        "buat produk baru permen coklat",
        "create produk permen coklat 13000",
        "register barang brownis 2500 toples",
    ],
    "edit_produk": [
        "edit barang",
        "edit produk",
        "edit harga barang",
        "update harga barang",
        "ubah harga barang",
        "ganti harga brownis jadi 2000",
        "update harga produk",
        "ubah harga produk",
        "edti harga barang",
        "ganti harga permen jadi 14.000",
        "edit barang produk",
        "perbaharui harga barang",
        "ganti harga permen coklat",
        "edit nama barang",
        "ubah nama produk",
        "ganti nama barang",
        "update nama produk",
        "edit produk brownis",
        "ubah produk permen",
        "update produk roti pia",
        "ganti harga brownis",
        "edit harga brownis",
        "update harga permen",
        "ubah harga permen",
        "ganti harga serbuk",
        "edit harga roti pia",
        "edit brg prduk",
        "edit hrga brg",
        "ganti hrga brownis jdi 2000",
        "ganti hrga prmen jdi 14000",
        "update hrga brg",
        "ubah hrga brg",
        "perbahrui hrga brg",
        "edit hrga prduk",
        "update hrga prduk",
        "ubah hrga prduk",
        "ganti hrga prmen coklat",
        "edit nma brg",
        "ubah nma prduk",
        "ganti nma brg",
        "update nma prduk",
        "edit prduk brownis",
        "ubah prduk prmen",
        "update prduk roti pia",
        "harga brownis diganti 2000",
        "harga permen diubah 14000",
        "harga brownis jadi berapa sekarang setelah update",
        "edit barang/produk",
        "Edit/update/ubah/hapus harga barang",
        "Update/ubah/edti harga barang/produk",
        "ubah harga brownis jadi 2000",
        "update harga brownis 2000",
        "edit harga brownis 2000",
        "ganti harga permen jadi 14000",
        "ubah harga permen jadi 14000",
        "update harga permen 14000",
        "edit harga permen 14000",
        "hapus/edit/ubah/ganti/update/perbaharui/tampilkan/tambah harga barang/produk",
        "edit/ubah/ganti/update/perbaharui nama barang",
        "ganti nama brownis jadi brownies premium",
        "ubah nama permen jadi permen original",
        "edti barang permen",
        "ganti hraga brownis jadi 2000",
        "ubah hrga permen jadi 14000",
        "updaet harga barang",
        "edti harga prmen",
        "ganti harga brownis jdi 2000",
        "ubah harga brownis jd 2000",
        "update hrga barang",
        "edit produk brwnis",
        "modify harga brownis 2000",
        "change harga permen 14000",
        "revisi harga brownis 2000",
        "koreksi harga barang",
    ],
    "hapus_produk": [
        "hapus barang",
        "hapus produk",
        "hapus harga barang",
        "hapus barang produk",
        "hapus produk permen",
        "hapus barang brownis",
        "hapus produk roti pia",
        "hapus barang permen coklat",
        "delete produk brownis",
        "delete barang permen",
        "remove produk roti pia",
        "hapus produk serbuk",
        "hapus brg prduk",
        "hapus prduk prmen",
        "hapus brg brownis",
        "hapus prduk roti pia",
        "hapus brg prmen coklat",
        "delete prduk brownis",
        "delete brg prmen",
        "remove prduk roti pia",
        "hapus prduk serbuk",
        "hapus barang yang tidak aktif",
        "hapus semua barang",
        "hapus daftar produk",
        "hapus barang permen",
        "hapus produk brownis",
        "hapus/edit/ubah/ganti/update/perbaharui/tampilkan/tambah nama barang/produk",
        "buang produk permen",
        "delete produk permen",
        "remove barang brownis",
        "hilangkan barang roti",
        "hapus brang permen",
        "hpus produk permen",
        "hapus prdk permen",
        "hapus barang brwnis",
        "hapus produk browni",
        "remove produk brownis",
        "buang produk brownis",
        "clear barang permen",
    ],
    "filter_belum_lunas": [
        "apa yang belum lunas",
        "siapa yang masih nyicil",
        "siapa yang masih hutang",
        "siapa yang belum bayar",
        "siapa tunggakan paling banyak",
        "siapa hutang terbanyak",
        "tampilkan yang belum lunas",
        "cek yang belum lunas",
        "lihat yang belum bayar",
        "daftar hutang",
        "daftar tunggakan",
        "siapa yang masih punya hutang",
        "siapa yang belum lunas",
        "tampilkan daftar hutang",
        "cek hutang pelanggan",
        "piutang pelanggan",
        "cek piutang",
        "tampilkan piutang",
        "siapa masih ada cicilan",
        "siapa yang cicilan",
        "yang belum bayar siapa",
        "apa yg blm lunas",
        "siapa yg msh nyicil",
        "siapa yg blm bayar",
        "siapa yg msh hutang",
        "siapa tggakn paling banyak",
        "siapa hutang trbanyak",
        "tampilin yg blm lunas",
        "cek yg blm lunas",
        "lhat yg blm bayar",
        "daftar hutng",
        "daftar tggakan",
        "siapa yg msh punya hutang",
        "siapa yg blm lunas",
        "tampilin daftar hutng",
        "cek hutng pelanggan",
        "piutng pelanggan",
        "cek piutng",
        "tampilin piutng",
        "siapa yang masih cicil",
        "siapa yang punya hutang",
        "Siapa tunggakan paking banyak",
        "siapa yang bayar dengan transfer",
        "siapa yang msh nyicil",
        "siapa yang masih nyicill",
        "siapa yang masih ntang",
        "siapa yg masih hutang",
        "siapa paling banyak hutng",
        "siapa yang blm lunas",
        "siapa yang outstanding",
        "siapa yang kredit",
        "siapa yang debt",
        "siapa yang nunggak",
        "siapa yang punya tagihan",
    ],
    "filter_bayar_cash": [
        "siapa yang bayar cash",
        "siapa yang bayar tunai",
        "siapa yang bayar langsung",
        "yang bayar cash siapa",
        "yang bayar tunai siapa",
        "tampilkan yang bayar cash",
        "cek yang bayar tunai",
        "daftar yang bayar cash",
        "pembeli yang bayar tunai",
        "siapa yang kontan",
        "yang kontan siapa",
        "tampilkan transaksi cash",
        "cek transaksi tunai",
        "siapa bayar di tempat",
        "yang bayar di tempat siapa",
        "siapa yg bayar cash",
        "siapa yg bayar tuni",
        "siapa yg bayar lgsung",
        "yg bayar csh siapa",
        "yg bayar tuni siapa",
        "tampilin yg bayar csh",
        "cek yg bayar tuni",
        "daftar yg bayar csh",
        "pembeli yg bayar tuni",
        "siapa yg kntan",
        "yg kntan siapa",
        "tampilin transaksi csh",
        "cek transaksi tuni",
        "siapa yang bayar cash/tunai/langsung",
        "siapa bayar cash",
        "siapa yg byr cash",
    ],
    "filter_bayar_transfer": [
        "siapa yang bayar transfer",
        "yang bayar transfer siapa",
        "tampilkan yang bayar transfer",
        "cek yang bayar via tf",
        "daftar yang bayar tf",
        "pembeli yang bayar transfer",
        "siapa yang tf",
        "yang tf siapa",
        "tampilkan transaksi transfer",
        "cek transaksi via transfer",
        "siapa bayar via tf",
        "siapa yg bayar transfr",
        "yg bayar transfr siapa",
        "tampilin yg bayar transfr",
        "cek yg bayar via tf",
        "daftar yg bayar tf",
        "pembeli yg bayar transfr",
        "siapa yg tf",
        "yg tf siapa",
        "tampilin transaksi transfr",
        "cek transaksi via transfr",
        "siapa bayar transfer",
        "siapa yang byr transfer",
    ],
    "total_transaksi": [
        "berapa total transaksi hari ini",
        "siapa transaksi terbangak hari ini",
        "tampilkan total transaksi hari ini",
        "siapa pembeli paling banyak hari ini",
        "pembeli paling banyak hari ini",
        "siapa pembeli terbanyak",
        "siapa pembeli terbanyak hari ini",
        "total transaksi hari ini",
        "berapa total transaksi",
        "total transaksi",
        "hitung total transaksi",
        "jumlah transaksi hari ini",
        "jumlah transaksi",
        "total order hari ini",
        "total pembelian hari ini",
        "berapa banyak transaksi hari ini",
        "berapa transaksi hari ini",
        "brp total transaksi hri ini",
        "tampilkan total transaksi hri ini",
        "total transaksi hri ini",
        "brp total transaksi",
        "hitung total transaksi",
        "jmlah transaksi hri ini",
        "jmlah transaksi",
        "total order hri ini",
        "total pembelian hri ini",
        "brp banyak transaksi hri ini",
        "brp transaksi hri ini",
        "berapa transaksi kemarin",
        "total transaksi kemarin",
        "berapa total transaksi bulan ini",
        "total transaksi minggu ini",
        "berapa total transaks hari ini",
        "total transakis hari ini",
        "brp total transaksi hari ini",
        "total uang taagihan hari ini",
        "total tunggakaan hari ini",
        "berapa pemassukan hari ini",
        "rekap transaksi hari ini",
        "summary transaksi hari ini",
        "laporan hari ini",
    ],
    "total_uang_masuk": [
        "berapa total uang masuk hari ini",
        "total uang masuk",
        "cek pemasukan hari ini",
        "tampilkan pemasukan hari ini",
        "berapa pemasukan hari ini",
        "tampilkan uang masuk kemarin",
        "berapa uang masuk hari ini",
        "uang masuk hari ini berapa",
        "pemasukan kemarin",
        "uang masuk kemarin",
        "berapa uang masuk kemarin",
        "total pendapatan hari ini",
        "pendapatan hari ini",
        "total pemasukan",
        "berapa pendapatan hari ini",
        "rekap uang masuk",
        "brp total ung masuk hri ini",
        "total ung masuk",
        "brp ung masuk hri ini",
        "ung masuk hri ini brp",
        "cek pmasukan hri ini",
        "brp pmasukan hri ini",
        "tampilin pmasukan hri ini",
        "tampilin ung masuk kmarin",
        "pmasukan kmarin",
        "ung masuk kmarin",
        "brp ung masuk kmarin",
        "total pndapatan hri ini",
        "pndapatan hri ini",
        "total pmasukan",
        "brp pndapatan hri ini",
        "rekap ung masuk",
        "total cash masuk hari ini",
        "total transfer masuk hari ini",
        "total uang masuk hari ini",
        "Cek/tampilkan/berapa pemasukan hari ini",
        "pemasukan hari ini",
        "total uang masuk hari ni",
        "brp uang masuk hari ini",
        "omzet hari ini",
    ],
    "total_tagihan": [
        "berapa total hutang",
        "cek sisa tagihan",
        "total piutang",
        "tampilkan semua hutang",
        "total cicilan penjual hari ini",
        "berapa total uang tagihan hari ini",
        "berapa total uang tagihan kemarin",
        "berapa total uang tagihan tanggal 21",
        "berapa total tagihan hari ini",
        "total tagihan hari ini",
        "berapa total tagihan kemarin",
        "berapa tagihan hari ini",
        "tagihan hari ini berapa",
        "cek tagihan hari ini",
        "tampilkan tagihan",
        "total tagihan",
        "tagihan pelanggan",
        "berapa yang masih tagihan",
        "brp total ung tagihan hri ini",
        "brp total tagihan hri ini",
        "total tagihan hri ini",
        "brp total ung tagihan kmarin",
        "brp total tagihan kmarin",
        "brp total ung tagihan tgl 21",
        "brp tagihan hri ini",
        "tagihan hri ini brp",
        "cek tagihan hri ini",
        "tampilin tagihan",
        "total piutng",
        "brp piutng hri ini",
        "total taghn",
        "taghn pelanggan",
        "brp yg msh tagihan",
        "total uang tagihan hari ini",
        "total uang tagihan kemarin",
        "total uang tagihan tanggal 21",
        "Total cicilan penjualan hari ini",
        "total cicilan hari ini",
        "berapa cicilan hari ini",
    ],
    "total_tunggakan": [
        "berapa total tunggakan hari ini",
        "siapa tunggakan paking banyak",
        "siapa hutang terbanyak",
        "total tunggakan hari ini",
        "total tunggakan",
        "berapa tunggakan hari ini",
        "tunggakan hari ini",
        "cek tunggakan",
        "tampilkan tunggakan",
        "berapa total hutang pelanggan",
        "total hutang",
        "hutang pelanggan berapa",
        "berapa total cicilan",
        "total cicilan",
        "total cicilan penjualan hari ini",
    ],
    "Pelunasan_Hutang": [
        "zio bayar hutang 27000000 transfer",
        "zio bayar tagihan 27 juta",
        "pak andi bayar hutang 500000 cash",
        "pak budi bayar cicilan 200000 tunai",
        "pak rudi bayar sisa 300000 transfer",
        "ibu sari lunasi hutang 1000000 tf",
        "pak hendra bayar tagihan 750000 cash",
        "pak joko bayar cicilan 150000 langsung",
        "mba rina bayar hutang 2000000 transfer",
        "pak wahyu lunasi tagihan 500000 tunai",
        "pak doni bayar 100000 cash",
        "pak soni bayar hutang 3000000 tf",
        "zio bayar hutng 27000000 transfr",
        "zio bayar taghn 27 juta",
        "pak andi bayar hutng 500000 csh",
        "pak budi bayar ciciln 200000 tuni",
        "catat pelunasan pak zio 27 juta tf",
        "pak zio udah bayar 27 juta transfer",
        "zio transfer 27 jt buat lunasin hutang",
        "bayar hutang zio 200rb transfer",
        "catat pelunasan hutang 200rb qris",
        "zio bayar hutang 27 juta transfer",
        "zio bayar tagihan 27000000",
        "zio lunasin tagihan 27 juta",
        "zio bayar cicilan 27 juta transfer",
    ],
    "pembeli_terbanyak": [
        "siapa pembeli paling banyak hari ini",
        "siapa transaksi terbanyak hari ini",
        "siapa pembeli terbanyak",
        "siapa pembeli terbanyak hari ini",
        "siapa pembeli terbanyak kemarin",
        "pembeli paling banyak hari ini",
        "pelanggan paling banyak beli",
        "siapa yang paling banyak order",
        "siapa yang paling banyak pesan",
        "customer terbanyak",
        "pelanggan terbanyak",
        "yang paling sering beli siapa",
        "siapa pembeli terbesar",
        "top pembeli",
        "ranking pembeli",
        "siapa yg paling banyak order hri ini",
        "Siapa yang pesan hari ini",
        "siapa saja yang pesan hari ini",
        "siapa yang order hari ini",
        "siapa yang paling banyak beli hari ini",
        "Siapa transaksi terbangak hari ini",
        "siapa yang paling banyak transaksi hari ini",
        "siapa yang paling banyak beli",
        "Siapa pembeli terbanyak hari ini/kemarin/tanggal sekian",
        "siapa pembeli terbanyak tanggal 21",
        "siapa yang pesn hari ini",
        "siapa saja yg order hari ini",
        "siapa pemeli paling banyak hari ini",
        "siapa pembeli trbanyak",
        "siapa yang paling bnyak beli",
        "siapa pmbeli terbanyak hari ini",
        "pelanggan terbanyak hari ini",
        "customer terbanyak hari ini",
        "pembeli top hari ini",
        "siapa yang belanja terbanyak",
    ],
    "hutang_terbanyak": [
        "siapa tunggakan paling banyak",
        "siapa hutang terbanyak",
        "siapa yang paling banyak hutang",
        "hutang terbesar siapa",
        "tunggakan terbesar siapa",
        "siapa yang paling banyak tunggakan",
        "siapa punya hutang paling besar",
        "cek hutang terbesar",
        "tampilkan hutang terbesar",
        "siapa yang paling banyak cicilan",
        "siapa cicilan terbesar",
        "siapa tggakn paling banyak",
        "siapa hutng trbanyak",
    ],
    "bantuan": [
        "bantuan",
        "help",
        "tolong",
        "cara pakai",
        "cara menggunakan",
        "perintah apa saja",
        "apa saja yang bisa dilakukan",
        "fitur apa saja",
        "menu",
        "panduan",
        "tutorial",
        "info",
        "informasi",
        "bantuaan",
        "hlp",
        "helpp",
        "bantu dong",
        "cara pake",
        "cara nggunain",
        "perintah apa aj",
        "menu apa aj",
    ],
}

NLP_TRAINING_EXAMPLES = [{
    "text": "1 minggu lagi pak ardi ambil barang 100 buah brownis udah dibayar tunai",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {
        "pelanggan": "pak ardi",
        "produk": "brownis",
        "jumlah": "100",
        "satuan": "buah",
        "bayar": "tunai",
        "status": "lunas",
        "waktu": "1 minggu lagi",
    },
}, {
    "text": "3 hari kedepan pak ardi ambil barang 100 buah brownis udah dibayar tunai",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {
        "pelanggan": "pak ardi",
        "produk": "brownis",
        "jumlah": "100",
        "satuan": "buah",
        "bayar": "tunai",
        "status": "lunas",
        "waktu": "3 hari kedepan",
    },
}, {
    "text": "3 hari yang lalu pak ardi ambil barang 100 buah brownis udah dibayar tunai",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {
        "pelanggan": "pak ardi",
        "produk": "brownis",
        "jumlah": "100",
        "satuan": "buah",
        "bayar": "tunai",
        "status": "lunas",
        "waktu": "3 hari lalu",
    },
}, {
    "text": "Berapa harga brownis",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
        "barang": "Brownis",
    },
}, {
    "text": "Berapa harga permen",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
        "barang": "Permen",
    },
}, {
    "text": "Berapa total transaksi hari ini",
    "intent": "total_transaksi",
    "entities": {},
}, {
    "text": "Berapa total tunggakan hari ini",
    "intent": "total_tunggakan",
    "entities": {},
}, {
    "text": "Berapa total uang masuk hari ini",
    "intent": "total_uang_masuk",
    "entities": {},
}, {
    "text": "Berapa total uang tagihan hari ini",
    "intent": "total_tagihan",
    "entities": {},
}, {
    "text": "Berapa total uang tagihan kemarin",
    "intent": "total_tagihan",
    "entities": {},
}, {
    "text": "Berapa total uang tagihan tanggal 21",
    "intent": "total_tagihan",
    "entities": {
        "tanggal": "21",
    },
}, {
    "text": "Cek harga permen",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
        "barang": "Permen",
    },
}, {
    "text": "Cek pemasukan hari ini",
    "intent": "total_uang_masuk",
    "entities": {},
}, {
    "text": "Cek penjualan hari ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {},
}, {
    "text": "Cek pesanan hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {},
}, {
    "text": "Cek pesanan pak andi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "Andi",
    },
}, {
    "text": "Cek pesanan tanggal 21",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
        "tanggal": "21",
    },
}, {
    "text": "Cek pesanan udin",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "Udin",
    },
}, {
    "text": "Cek/tampilkan harga barang",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "Cek/tampilkan pesanan tanggal 21 04 2026",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
        "tanggal": "21-04-2026",
    },
}, {
    "text": "Edit harga barang",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "Ganti harga brownis jadi 2000",
    "intent": "edit_produk",
    "entities": {
        "barang": "Brownis",
        "harga": "2000",
    },
}, {
    "text": "Ganti harga permen jadi 14.000",
    "intent": "edit_produk",
    "entities": {
        "barang": "Permen",
        "harga": "14000",
    },
}, {
    "text": "Hapus pesanan udin dengan status pembayaran belum lunas",
    "intent": "hapus_transaksi",
    "entities": {
        "pelanggan": "Udin",
        "status": "Hutang",
    },
}, {
    "text": "Hapus semua data penjualan",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "Hapus/tampilkan semua data",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "Hari ini Udin ambil permen 30 dus sudah lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "pelanggan": "Udin",
        "barang": "Permen",
        "jumlah": "30",
        "satuan": "dus",
        "status": "Lunas",
    },
}, {
    "text": "Hari ini andi order permen 600 toples dicicil 200000 tunai",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
        "pelanggan": "Andi",
        "barang": "Permen",
        "jumlah": "600",
        "satuan": "toples",
        "status": "Cicil",
        "nominal_bayar": "200000",
        "metode": "Tunai",
    },
}, {
    "text": "Hari ini budi order permen 30 toples dicicil 200000 dibayar langsung",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
        "pelanggan": "Budi",
        "barang": "Permen",
        "jumlah": "30",
        "satuan": "toples",
        "status": "Cicil",
        "nominal_bayar": "200000",
        "metode": "Tunai",
    },
}, {
    "text": "Hari ini naha ambil permen 50 dus sudah lunas dibayar secara transfer",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
        "pelanggan": "Naha",
        "barang": "Permen",
        "jumlah": "50",
        "satuan": "dus",
        "status": "Lunas",
        "metode": "Transfer",
    },
}, {
    "text": "Hari ini nala ambil brownis 100 bungkus dicicil 1000000 dibayar secara transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
        "pelanggan": "Nala",
        "barang": "Brownis",
        "jumlah": "100",
        "satuan": "bungkus",
        "status": "Cicil",
        "nominal_bayar": "1000000",
        "metode": "Transfer",
    },
}, {
    "text": "Hari ini nala ambil permen 70 dus dicicil 2000000 dibayar secara transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
        "pelanggan": "Nala",
        "barang": "Permen",
        "jumlah": "70",
        "satuan": "dus",
        "status": "Cicil",
        "nominal_bayar": "2000000",
        "metode": "Transfer",
    },
}, {
    "text": "Hari ini nala ambil serbuk 100 lunas dibayar secara transfer",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
        "pelanggan": "Nala",
        "barang": "Serbuk",
        "jumlah": "100",
        "status": "Lunas",
        "metode": "Transfer",
    },
}, {
    "text": "Hari ini pak agus ambil permen coklat 2 dus",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "pelanggan": "Agus",
        "barang": "Permen Coklat",
        "jumlah": "2",
        "satuan": "dus",
    },
}, {
    "text": "Hari ini pak andi order barang 50 pcs berupa permen",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "pelanggan": "Andi",
        "barang": "Permen",
        "jumlah": "50",
        "satuan": "pcs",
    },
}, {
    "text": "Hari ini rara ambil permen coklat 13 dus dibayar lunas secara cash",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "pelanggan": "Rara",
        "barang": "Permen Coklat",
        "jumlah": "13",
        "satuan": "dus",
        "status": "Lunas",
        "metode": "Tunai",
    },
}, {
    "text": "Hari ini rudi order permen 600 toples dicicil 200000 bayar langsung",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
        "pelanggan": "Rudi",
        "barang": "Permen",
        "jumlah": "600",
        "satuan": "toples",
        "status": "Cicil",
        "nominal_bayar": "200000",
        "metode": "Tunai",
    },
}, {
    "text": "Hari ini rudi order permen 600 toples dicicil 200000 cash",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
        "pelanggan": "Rudi",
        "barang": "Permen",
        "jumlah": "600",
        "satuan": "toples",
        "status": "Cicil",
        "nominal_bayar": "200000",
        "metode": "Tunai",
    },
}, {
    "text": "Hari ini rudi order permen 600 toples dicicil 200000 sudah dibayar",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
        "pelanggan": "Rudi",
        "barang": "Permen",
        "jumlah": "600",
        "satuan": "toples",
        "status": "Cicil",
        "nominal_bayar": "200000",
    },
}, {
    "text": "Hari ini rudi order permen 600 toples dicicil 200000 tf",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
        "pelanggan": "Rudi",
        "barang": "Permen",
        "jumlah": "600",
        "satuan": "toples",
        "status": "Cicil",
        "nominal_bayar": "200000",
        "metode": "Transfer",
    },
}, {
    "text": "Hari ini rudi order permen 600 toples sudah lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "pelanggan": "Rudi",
        "barang": "Permen",
        "jumlah": "600",
        "satuan": "toples",
        "status": "Lunas",
    },
}, {
    "text": "Hari ini supri ambil permen 20 toples sudah lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "pelanggan": "Supri",
        "barang": "Permen",
        "jumlah": "20",
        "satuan": "toples",
        "status": "Lunas",
    },
}, {
    "text": "Perbaharui pesanan pak naha",
    "intent": "update_transaksi",
    "entities": {
        "pelanggan": "Naha",
    },
}, {
    "text": "Perbaharui transaksi zio",
    "intent": "update_transaksi",
    "entities": {
        "pelanggan": "Zio",
    },
}, {
    "text": "Pesanan pak ardi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "Ardi",
    },
}, {
    "text": "Siapa pembeli paling banyak hari ini",
    "intent": "total_transaksi",
    "entities": {},
}, {
    "text": "Siapa pembeli terbanyak",
    "intent": "total_transaksi",
    "entities": {},
}, {
    "text": "Siapa pembeli terbanyak hari ini",
    "intent": "total_transaksi",
    "entities": {},
}, {
    "text": "Siapa transaksi terbangak hari ini",
    "intent": "total_transaksi",
    "entities": {},
}, {
    "text": "Siapa tunggakan paking banyak",
    "intent": "total_tunggakan",
    "entities": {},
}, {
    "text": "Siapa yang bayar cash",
    "intent": "filter_bayar_cash",
    "entities": {},
}, {
    "text": "Siapa yang bayar transfer",
    "intent": "filter_bayar_transfer",
    "entities": {},
}, {
    "text": "Siapa yang masih hutang",
    "intent": "total_tunggakan",
    "entities": {},
}, {
    "text": "Siapa yang masih nyicil",
    "intent": "total_tunggakan",
    "entities": {},
}, {
    "text": "Siapa yang pesan hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {},
}, {
    "text": "Tambah barang brownis harga 2500 per bungkus",
    "intent": "tambah_produk",
    "entities": {
        "barang": "Brownis",
        "harga": "2500",
        "satuan": "bungkus",
    },
}, {
    "text": "Tambah barang brownis harga 2500 per toples",
    "intent": "tambah_produk",
    "entities": {
        "barang": "Brownis",
        "harga": "2500",
        "satuan": "toples",
    },
}, {
    "text": "Tambah barang permen coklat",
    "intent": "tambah_produk",
    "entities": {
        "barang": "Permen Coklat",
    },
}, {
    "text": "Tambah barang roti pia bulus",
    "intent": "tambah_produk",
    "entities": {
        "barang": "Roti Pia Bulus",
    },
}, {
    "text": "Tampilan data penjualan hari ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {},
}, {
    "text": "Tampilkan daftar harga barang",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "Tampilkan harga brownis",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
        "barang": "Brownis",
    },
}, {
    "text": "Tampilkan jumlah pesanan dari pak andi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "Andi",
    },
}, {
    "text": "Tampilkan semua daftar penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "Tampilkan total transaksi hari ini",
    "intent": "total_transaksi",
    "entities": {},
}, {
    "text": "Tampilkan transaksi tanggal 28",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
        "tanggal": "28",
    },
}, {
    "text": "Tampilkan uang masuk kemarin",
    "intent": "total_uang_masuk",
    "entities": {},
}, {
    "text": "Total cicilan penjual hari ini",
    "intent": "total_tagihan",
    "entities": {},
}, {
    "text": "Update harga barang",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "Update pesanan naha",
    "intent": "update_transaksi",
    "entities": {
        "pelanggan": "Naha",
    },
}, {
    "text": "Zio bayar hutang 27000000 transfer",
    "intent": "bayar_hutang",
    "entities": {
        "pelanggan": "Zio",
        "nominal_bayar": "27000000",
        "metode": "Transfer",
    },
}, {
    "text": "Zio bayar tagihan 27 juta",
    "intent": "bayar_hutang",
    "entities": {
        "pelanggan": "Zio",
        "nominal_bayar": "27000000",
    },
}, {
    "text": "ada barang apa saja",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "ada berapa penjualan hari ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {},
}, {
    "text": "add barang brownis",
    "intent": "tambah_produk",
    "entities": {
        "produk": "brownis",
    },
}, {
    "text": "add produk permen",
    "intent": "tambah_produk",
    "entities": {
        "produk": "permen",
    },
}, {
    "text": "apa yang belum lunas",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "apa yg blm lunas",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "apakabar",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "assalamualaikum",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "barang apa saja yang ada",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "barang paling mahal",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
        "filter": "tertinggi",
    },
}, {
    "text": "berapa banyak transaksi hari ini",
    "intent": "total_transaksi",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "berapa harga brownis",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
        "produk": "brownis",
    },
}, {
    "text": "berapa harga permen",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
        "produk": "permen",
    },
}, {
    "text": "berapa harga permen coklat",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
        "produk": "permen coklat",
    },
}, {
    "text": "berapa harga produk tertinggi",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
        "filter": "tertinggi",
    },
}, {
    "text": "berapa harga roti pia",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
        "produk": "roti pia",
    },
}, {
    "text": "berapa harga serbuk",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
        "produk": "serbuk",
    },
}, {
    "text": "berapa pemasukan hari ini",
    "intent": "total_uang_masuk",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "berapa pendapatan hari ini",
    "intent": "total_uang_masuk",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "berapa pesanan pak andi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "pak andi",
    },
}, {
    "text": "berapa piutang hari ini",
    "intent": "total_tagihan",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "berapa tagihan hari ini",
    "intent": "total_tagihan",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "berapa total cicilan",
    "intent": "total_tunggakan",
    "entities": {},
}, {
    "text": "berapa total hutang pelanggan",
    "intent": "total_tunggakan",
    "entities": {},
}, {
    "text": "berapa total tagihan hari ini",
    "intent": "total_tagihan",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "berapa total tagihan kemarin",
    "intent": "total_tagihan",
    "entities": {
        "waktu": "kemarin",
    },
}, {
    "text": "berapa total transaksi",
    "intent": "total_transaksi",
    "entities": {},
}, {
    "text": "berapa total transaksi bulan ini",
    "intent": "total_transaksi",
    "entities": {
        "waktu": "bulan ini",
    },
}, {
    "text": "berapa total transaksi hari ini",
    "intent": "total_transaksi",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "berapa total tunggakan hari ini",
    "intent": "total_tunggakan",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "berapa total uang masuk hari ini",
    "intent": "total_uang_masuk",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "berapa total uang tagihan hari ini",
    "intent": "total_tagihan",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "berapa total uang tagihan kemarin",
    "intent": "total_tagihan",
    "entities": {
        "waktu": "kemarin",
    },
}, {
    "text": "berapa total uang tagihan tanggal 21",
    "intent": "total_tagihan",
    "entities": {
        "tanggal": "21",
    },
}, {
    "text": "berapa transaksi hari ini",
    "intent": "total_transaksi",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "berapa transaksi kemarin",
    "intent": "total_transaksi",
    "entities": {
        "waktu": "kemarin",
    },
}, {
    "text": "berapa transaksi pak ardi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "pak ardi",
    },
}, {
    "text": "berapa tunggakan hari ini",
    "intent": "total_tunggakan",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "berapa uang masuk hari ini",
    "intent": "total_uang_masuk",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "berapa uang masuk kemarin",
    "intent": "total_uang_masuk",
    "entities": {
        "waktu": "kemarin",
    },
}, {
    "text": "berapa yang masih tagihan",
    "intent": "total_tagihan",
    "entities": {},
}, {
    "text": "besok pak ardi ambil barang 100 buah brownis sudah dibayar",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {
        "pelanggan": "pak ardi",
        "produk": "brownis",
        "jumlah": "100",
        "satuan": "buah",
        "status": "lunas",
        "waktu": "besok",
    },
}, {
    "text": "brp harga brownis",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
        "produk": "brownis",
    },
}, {
    "text": "brp harga permen",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
        "produk": "permen",
    },
}, {
    "text": "brp harga prduk tertinggi",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
        "filter": "tertinggi",
    },
}, {
    "text": "buang semua data penjualan",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "catat pelunasan pak zio 27 juta tf",
    "intent": "bayar_hutang",
    "entities": {
        "pelanggan": "pak zio",
        "nominal": "27000000",
        "bayar": "transfer",
    },
}, {
    "text": "cek barang",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "cek data penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "cek harga barang",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "cek harga brg",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "cek harga brownis",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
        "produk": "brownis",
    },
}, {
    "text": "cek harga permen",
    "intent": "tampilkan_produk",
    "entities": {
        "produk": "permen",
    },
}, {
    "text": "cek harga roti pia",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
        "produk": "roti pia",
    },
}, {
    "text": "cek harga serbuk",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
        "produk": "serbuk",
    },
}, {
    "text": "cek hutang pelanggan",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "cek hutang terbesar",
    "intent": "hutang_terbanyak",
    "entities": {},
}, {
    "text": "cek pemasukan hari ini",
    "intent": "total_uang_masuk",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "cek penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "cek penjualan hari ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {},
}, {
    "text": "cek penjualan kemarin",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
        "waktu": "kemarin",
    },
}, {
    "text": "cek penjulan hri ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {},
}, {
    "text": "cek pesanan hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {},
}, {
    "text": "cek pesanan pak andi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "pak andi",
    },
}, {
    "text": "cek pesanan pak ardi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "pak ardi",
    },
}, {
    "text": "cek pesanan pak hendra",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "pak hendra",
    },
}, {
    "text": "cek pesanan tanggal 21",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
        "tanggal": "21",
    },
}, {
    "text": "cek pesanan tanggal 21 04 2026",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
        "tanggal": "21-04-2026",
    },
}, {
    "text": "cek pesanan udin",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "udin",
    },
}, {
    "text": "cek pesnan pak andi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "pak andi",
    },
}, {
    "text": "cek pesnan pak ardi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "pak ardi",
    },
}, {
    "text": "cek pesnan tanggal 21",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
        "tanggal": "21",
    },
}, {
    "text": "cek pesnan tanggal 21 04 2026",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
        "tanggal": "21-04-2026",
    },
}, {
    "text": "cek pesnan udin",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "udin",
    },
}, {
    "text": "cek piutang",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "cek pnjualan hari ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {},
}, {
    "text": "cek produk",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "cek semua penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "cek semua transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "cek smua penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "cek tagihan hari ini",
    "intent": "total_tagihan",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "cek transaksi hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {},
}, {
    "text": "cek transaksi ibu maya",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "ibu maya",
    },
}, {
    "text": "cek transaksi kemarin",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
        "waktu": "kemarin",
    },
}, {
    "text": "cek transaksi tanggal 21",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
        "tanggal": "21",
    },
}, {
    "text": "cek transaksi tunai",
    "intent": "filter_bayar_cash",
    "entities": {
        "bayar": "tunai",
    },
}, {
    "text": "cek transaksi udin",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "udin",
    },
}, {
    "text": "cek transaksi via transfer",
    "intent": "filter_bayar_transfer",
    "entities": {
        "bayar": "transfer",
    },
}, {
    "text": "cek tunggakan",
    "intent": "total_tunggakan",
    "entities": {},
}, {
    "text": "cek yang bayar tunai",
    "intent": "filter_bayar_cash",
    "entities": {
        "bayar": "tunai",
    },
}, {
    "text": "cek yang bayar via tf",
    "intent": "filter_bayar_transfer",
    "entities": {
        "bayar": "transfer",
    },
}, {
    "text": "cek yang belum lunas",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "clear semua transaksi",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "customer terbanyak",
    "intent": "pembeli_terbanyak",
    "entities": {},
}, {
    "text": "daftar barang",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "daftar hutang",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "daftar penjualan hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {},
}, {
    "text": "daftar penjualan kemarin",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
        "waktu": "kemarin",
    },
}, {
    "text": "daftar penjualan semua",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "daftar prduk",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "daftar produk",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "daftar tunggakan",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "daftar yang bayar cash",
    "intent": "filter_bayar_cash",
    "entities": {
        "bayar": "cash",
    },
}, {
    "text": "daftar yang bayar tf",
    "intent": "filter_bayar_transfer",
    "entities": {
        "bayar": "transfer",
    },
}, {
    "text": "daftarkan barang brownis",
    "intent": "tambah_produk",
    "entities": {
        "produk": "brownis",
    },
}, {
    "text": "daftarkan produk permen",
    "intent": "tambah_produk",
    "entities": {
        "produk": "permen",
    },
}, {
    "text": "data pembelian pak rudi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "pak rudi",
    },
}, {
    "text": "data penjualan hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {},
}, {
    "text": "data penjualan tanggal 5",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
        "tanggal": "5",
    },
}, {
    "text": "data pesanan mba rina",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "mba rina",
    },
}, {
    "text": "data tanggal 21 04",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
        "tanggal": "21-04",
    },
}, {
    "text": "data transaksi pak andi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "pak andi",
    },
}, {
    "text": "delete barang permen",
    "intent": "hapus_produk",
    "entities": {
        "produk": "permen",
    },
}, {
    "text": "delete produk brownis",
    "intent": "hapus_produk",
    "entities": {
        "produk": "brownis",
    },
}, {
    "text": "delete semua transaksi",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "edit barang",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "edit data transaksi ibu maya",
    "intent": "update_transaksi",
    "entities": {
        "pelanggan": "ibu maya",
    },
}, {
    "text": "edit harga brownis",
    "intent": "edit_produk",
    "entities": {
        "produk": "brownis",
    },
}, {
    "text": "edit harga produk",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "edit nama barang",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "edit order pak joko",
    "intent": "update_transaksi",
    "entities": {
        "pelanggan": "pak joko",
    },
}, {
    "text": "edit pesanan pak naha",
    "intent": "update_transaksi",
    "entities": {
        "pelanggan": "pak naha",
    },
}, {
    "text": "edit produk brownis",
    "intent": "edit_produk",
    "entities": {
        "produk": "brownis",
    },
}, {
    "text": "edit transaksi pak budi",
    "intent": "update_transaksi",
    "entities": {
        "pelanggan": "pak budi",
    },
}, {
    "text": "ganti data transaksi pak soni",
    "intent": "update_transaksi",
    "entities": {
        "pelanggan": "pak soni",
    },
}, {
    "text": "ganti harga brownis",
    "intent": "edit_produk",
    "entities": {
        "produk": "brownis",
    },
}, {
    "text": "ganti harga brownis jadi 2000",
    "intent": "edit_produk",
    "entities": {
        "produk": "brownis",
        "harga_baru": "2000",
    },
}, {
    "text": "ganti harga brownis jdi 2000",
    "intent": "edit_produk",
    "entities": {
        "produk": "brownis",
        "harga_baru": "2000",
    },
}, {
    "text": "ganti harga permen coklat",
    "intent": "edit_produk",
    "entities": {
        "produk": "permen coklat",
    },
}, {
    "text": "ganti harga permen jadi 14000",
    "intent": "edit_produk",
    "entities": {
        "produk": "permen",
        "harga_baru": "14000",
    },
}, {
    "text": "ganti hrga prmen jdi 14000",
    "intent": "edit_produk",
    "entities": {
        "produk": "permen",
        "harga_baru": "14000",
    },
}, {
    "text": "ganti nama barang",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "gimana penjualan hari ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {},
}, {
    "text": "gmn penjualan hri ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {},
}, {
    "text": "hai",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "hai bisa bantu saya",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "hai bot",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "hai kak",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "hallo",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "hallo semuanya",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "halloo",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "halo",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "halo ada yang bisa bantu",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "halo bot",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "halo bro",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "haloo",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "halooo",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "hapus barang brownis",
    "intent": "hapus_produk",
    "entities": {
        "produk": "brownis",
    },
}, {
    "text": "hapus barang permen coklat",
    "intent": "hapus_produk",
    "entities": {
        "produk": "permen coklat",
    },
}, {
    "text": "hapus barang produk",
    "intent": "hapus_produk",
    "entities": {},
}, {
    "text": "hapus data pak hendra",
    "intent": "hapus_transaksi",
    "entities": {
        "pelanggan": "pak hendra",
    },
}, {
    "text": "hapus data penjualan",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "hapus harga barang",
    "intent": "hapus_produk",
    "entities": {},
}, {
    "text": "hapus order pak rudi",
    "intent": "hapus_transaksi",
    "entities": {
        "pelanggan": "pak rudi",
    },
}, {
    "text": "hapus pesanan pak budi",
    "intent": "hapus_transaksi",
    "entities": {
        "pelanggan": "pak budi",
    },
}, {
    "text": "hapus pesanan udin",
    "intent": "hapus_transaksi",
    "entities": {
        "pelanggan": "udin",
    },
}, {
    "text": "hapus pesanan udin dengan status pembayaran belum lunas",
    "intent": "hapus_transaksi",
    "entities": {
        "pelanggan": "udin",
        "status": "belum lunas",
    },
}, {
    "text": "hapus pesnan udin",
    "intent": "hapus_transaksi",
    "entities": {
        "pelanggan": "udin",
    },
}, {
    "text": "hapus pesnan udin dg status pembayaran blm lunas",
    "intent": "hapus_transaksi",
    "entities": {
        "pelanggan": "udin",
        "status": "belum lunas",
    },
}, {
    "text": "hapus produk permen",
    "intent": "hapus_produk",
    "entities": {
        "produk": "permen",
    },
}, {
    "text": "hapus produk roti pia",
    "intent": "hapus_produk",
    "entities": {
        "produk": "roti pia",
    },
}, {
    "text": "hapus produk serbuk",
    "intent": "hapus_produk",
    "entities": {
        "produk": "serbuk",
    },
}, {
    "text": "hapus rekap penjualan",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "hapus riwayat pesanan pak ardi",
    "intent": "hapus_transaksi",
    "entities": {
        "pelanggan": "pak ardi",
    },
}, {
    "text": "hapus seluruh transaksi",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "hapus semua data penjualan",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "hapus semua data transaksi",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "hapus semua order",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "hapus semua transaksi",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "hapus smua data penjualan",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "hapus smua transaksi",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "hapus transaksi pak andi",
    "intent": "hapus_transaksi",
    "entities": {
        "pelanggan": "pak andi",
    },
}, {
    "text": "hapus transaksi pak joko",
    "intent": "hapus_transaksi",
    "entities": {
        "pelanggan": "pak joko",
    },
}, {
    "text": "hapus transaksi udin",
    "intent": "hapus_transaksi",
    "entities": {
        "pelanggan": "udin",
    },
}, {
    "text": "harga brownis",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
        "produk": "brownis",
    },
}, {
    "text": "harga brownis diganti 2000",
    "intent": "edit_produk",
    "entities": {
        "produk": "brownis",
        "harga_baru": "2000",
    },
}, {
    "text": "harga permen",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
        "produk": "permen",
    },
}, {
    "text": "harga permen coklat",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
        "produk": "permen coklat",
    },
}, {
    "text": "harga permen diubah 14000",
    "intent": "edit_produk",
    "entities": {
        "produk": "permen",
        "harga_baru": "14000",
    },
}, {
    "text": "harga roti pia",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
        "produk": "roti pia",
    },
}, {
    "text": "harga serbuk",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
        "produk": "serbuk",
    },
}, {
    "text": "harga terendah",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
        "filter": "terendah",
    },
}, {
    "text": "harga tertinggi",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
        "filter": "tertinggi",
    },
}, {
    "text": "hari ini ada order apa aja",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {},
}, {
    "text": "hari ini ada transaksi apa",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {},
}, {
    "text": "hari ini andi order permen 600 toples dicicil 200000 tunai",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
        "pelanggan": "andi",
        "produk": "permen",
        "jumlah": "600",
        "satuan": "toples",
        "dp": "200000",
        "bayar": "tunai",
    },
}, {
    "text": "hari ini budi order permen 30 toples dicicil 200000 dibayar langsung",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
        "pelanggan": "budi",
        "produk": "permen",
        "jumlah": "30",
        "satuan": "toples",
        "dp": "200000",
        "bayar": "cash",
    },
}, {
    "text": "hari ini naha ambil permen 50 dus sudah lunas dibayar secara transfer",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
        "pelanggan": "naha",
        "produk": "permen",
        "jumlah": "50",
        "satuan": "dus",
        "bayar": "transfer",
        "status": "lunas",
    },
}, {
    "text": "hari ini nala ambil brownis 100 bungkus dicicil 1000000 dibayar secara transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
        "pelanggan": "nala",
        "produk": "brownis",
        "jumlah": "100",
        "satuan": "bungkus",
        "dp": "1000000",
        "bayar": "transfer",
    },
}, {
    "text": "hari ini nala ambil permen 70 dus dicicil 2000000 dibayar secara transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
        "pelanggan": "nala",
        "produk": "permen",
        "jumlah": "70",
        "satuan": "dus",
        "dp": "2000000",
        "bayar": "transfer",
    },
}, {
    "text": "hari ini nala ambil serbuk 100 lunas dibayar secara transfer",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
        "pelanggan": "nala",
        "produk": "serbuk",
        "jumlah": "100",
        "bayar": "transfer",
        "status": "lunas",
    },
}, {
    "text": "hari ini pak agus ambil permen coklat 2 dus",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "pelanggan": "pak agus",
        "produk": "permen coklat",
        "jumlah": "2",
        "satuan": "dus",
    },
}, {
    "text": "hari ini pak andi order barang 50 pcs berupa permen",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "pelanggan": "pak andi",
        "produk": "permen",
        "jumlah": "50",
        "satuan": "pcs",
    },
}, {
    "text": "hari ini penjualan gimana",
    "intent": "cek_penjualan_hari_ini",
    "entities": {},
}, {
    "text": "hari ini rara ambil permen coklat 13 dus dibayar lunas secara cash",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "pelanggan": "rara",
        "produk": "permen coklat",
        "jumlah": "13",
        "satuan": "dus",
        "bayar": "cash",
        "status": "lunas",
    },
}, {
    "text": "hari ini rudi order permen 600 toples dicicil 200000 bayar langsung",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
        "pelanggan": "rudi",
        "produk": "permen",
        "jumlah": "600",
        "satuan": "toples",
        "dp": "200000",
        "bayar": "langsung",
    },
}, {
    "text": "hari ini rudi order permen 600 toples dicicil 200000 cash",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
        "pelanggan": "rudi",
        "produk": "permen",
        "jumlah": "600",
        "satuan": "toples",
        "dp": "200000",
        "bayar": "cash",
    },
}, {
    "text": "hari ini rudi order permen 600 toples dicicil 200000 sudah dibayar",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
        "pelanggan": "rudi",
        "produk": "permen",
        "jumlah": "600",
        "satuan": "toples",
        "dp": "200000",
        "bayar": "transfer",
    },
}, {
    "text": "hari ini rudi order permen 600 toples dicicil 200000 tf",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
        "pelanggan": "rudi",
        "produk": "permen",
        "jumlah": "600",
        "satuan": "toples",
        "dp": "200000",
        "bayar": "transfer",
    },
}, {
    "text": "hari ini rudi order permen 600 toples sudah lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "pelanggan": "rudi",
        "produk": "permen",
        "jumlah": "600",
        "satuan": "toples",
        "status": "lunas",
    },
}, {
    "text": "hari ini siapa yang beli",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {},
}, {
    "text": "hari ini supri ambil permen 20 toples sudah lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "pelanggan": "supri",
        "produk": "permen",
        "jumlah": "20",
        "satuan": "toples",
        "status": "lunas",
    },
}, {
    "text": "hari ini udin ambil permen 30 dus sudah lunas",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
        "pelanggan": "udin",
        "produk": "permen",
        "jumlah": "30",
        "satuan": "dus",
        "status": "lunas",
    },
}, {
    "text": "hari minggu pak ardi ambil barang 100 buah brownis udah dibayar tunai",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {
        "pelanggan": "pak ardi",
        "produk": "brownis",
        "jumlah": "100",
        "satuan": "buah",
        "bayar": "tunai",
        "status": "lunas",
        "waktu": "hari minggu",
    },
}, {
    "text": "hari senin pak ardi ambil barang 100 buah brownis udah dibayar tunai",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {
        "pelanggan": "pak ardi",
        "produk": "brownis",
        "jumlah": "100",
        "satuan": "buah",
        "bayar": "tunai",
        "status": "lunas",
        "waktu": "hari senin",
    },
}, {
    "text": "hei",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "hei gan",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "hello",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "helo",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "helo bos",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "hey",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "hi",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "hitung total transaksi",
    "intent": "total_transaksi",
    "entities": {},
}, {
    "text": "hlo",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "hlw",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "hrga brownis",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
        "produk": "brownis",
    },
}, {
    "text": "hrga permen",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
        "produk": "permen",
    },
}, {
    "text": "hutang pelanggan berapa",
    "intent": "total_tunggakan",
    "entities": {},
}, {
    "text": "hutang terbesar siapa",
    "intent": "hutang_terbanyak",
    "entities": {},
}, {
    "text": "ibu sari lunasi hutang 1000000 tf",
    "intent": "bayar_hutang",
    "entities": {
        "pelanggan": "ibu sari",
        "nominal": "1000000",
        "bayar": "transfer",
    },
}, {
    "text": "info penjualan hari ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {},
}, {
    "text": "input barang brownis 2500",
    "intent": "tambah_produk",
    "entities": {
        "produk": "brownis",
        "harga": "2500",
    },
}, {
    "text": "input produk permen coklat 13000",
    "intent": "tambah_produk",
    "entities": {
        "produk": "permen coklat",
        "harga": "13000",
    },
}, {
    "text": "jumlah transaksi",
    "intent": "total_transaksi",
    "entities": {},
}, {
    "text": "jumlah transaksi hari ini",
    "intent": "total_transaksi",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "keluarkan data penjualan semua",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "kemarin ada order apa",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
        "waktu": "kemarin",
    },
}, {
    "text": "kemarin pak ardi ambil barang 100 buah brownis sudah dibayar tunai",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {
        "pelanggan": "pak ardi",
        "produk": "brownis",
        "jumlah": "100",
        "satuan": "buah",
        "bayar": "tunai",
        "status": "lunas",
        "waktu": "kemarin",
    },
}, {
    "text": "kemarin siapa yang beli",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
        "waktu": "kemarin",
    },
}, {
    "text": "kemren ada order apa",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
        "waktu": "kemarin",
    },
}, {
    "text": "laporan hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {},
}, {
    "text": "laporan kemarin",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
        "waktu": "kemarin",
    },
}, {
    "text": "laporan penjualan hari ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {},
}, {
    "text": "laporan pnjualan hri ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {},
}, {
    "text": "lhat semua transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "liatin semua transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "lihat barang",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "lihat data penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "lihat order pak doni",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "pak doni",
    },
}, {
    "text": "lihat penjualan tanggal 15",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
        "tanggal": "15",
    },
}, {
    "text": "lihat pesanan pak andi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "pak andi",
    },
}, {
    "text": "lihat produk",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "lihat semua transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "lihat transaksi hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {},
}, {
    "text": "lihat transaksi kemarin",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
        "waktu": "kemarin",
    },
}, {
    "text": "lihat yang belum bayar",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "list barang",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "list produk",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "list semua penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "lusa pak ardi ambil barang 100 buah brownis sudah dibayar tunai",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {
        "pelanggan": "pak ardi",
        "produk": "brownis",
        "jumlah": "100",
        "satuan": "buah",
        "bayar": "tunai",
        "status": "lunas",
        "waktu": "lusa",
    },
}, {
    "text": "masukkan barang baru brownis",
    "intent": "tambah_produk",
    "entities": {
        "produk": "brownis",
    },
}, {
    "text": "masukkan produk baru permen coklat",
    "intent": "tambah_produk",
    "entities": {
        "produk": "permen coklat",
    },
}, {
    "text": "mba rina bayar hutang 2000000 transfer",
    "intent": "bayar_hutang",
    "entities": {
        "pelanggan": "mba rina",
        "nominal": "2000000",
        "bayar": "transfer",
    },
}, {
    "text": "met pagi",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "met siang",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "minggu depan pak ardi ambil barang 100 buah brownis udah dibayar tunai",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {
        "pelanggan": "pak ardi",
        "produk": "brownis",
        "jumlah": "100",
        "satuan": "buah",
        "bayar": "tunai",
        "status": "lunas",
        "waktu": "minggu depan",
    },
}, {
    "text": "minggu depang pak ardi ambil barang 100 buah brownis udah dibayar tunai",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {
        "pelanggan": "pak ardi",
        "produk": "brownis",
        "jumlah": "100",
        "satuan": "buah",
        "bayar": "tunai",
        "status": "lunas",
        "waktu": "minggu depan",
    },
}, {
    "text": "munculkan semua transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "order hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {},
}, {
    "text": "order kemarin ada apa aja",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
        "waktu": "kemarin",
    },
}, {
    "text": "order pak andi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "pak andi",
    },
}, {
    "text": "order tanggal 14",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
        "tanggal": "14",
    },
}, {
    "text": "p kabar",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "pak andi bayar hutang 500000 cash",
    "intent": "bayar_hutang",
    "entities": {
        "pelanggan": "pak andi",
        "nominal": "500000",
        "bayar": "cash",
    },
}, {
    "text": "pak andi bayar hutng 500000 csh",
    "intent": "bayar_hutang",
    "entities": {
        "pelanggan": "pak andi",
        "nominal": "500000",
        "bayar": "cash",
    },
}, {
    "text": "pak andi beli apa saja",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "pak andi",
    },
}, {
    "text": "pak budi bayar cicilan 200000 tunai",
    "intent": "bayar_hutang",
    "entities": {
        "pelanggan": "pak budi",
        "nominal": "200000",
        "bayar": "tunai",
    },
}, {
    "text": "pak budi bayar ciciln 200000 tuni",
    "intent": "bayar_hutang",
    "entities": {
        "pelanggan": "pak budi",
        "nominal": "200000",
        "bayar": "tunai",
    },
}, {
    "text": "pak doni bayar 100000 cash",
    "intent": "bayar_hutang",
    "entities": {
        "pelanggan": "pak doni",
        "nominal": "100000",
        "bayar": "cash",
    },
}, {
    "text": "pak hendra bayar tagihan 750000 cash",
    "intent": "bayar_hutang",
    "entities": {
        "pelanggan": "pak hendra",
        "nominal": "750000",
        "bayar": "cash",
    },
}, {
    "text": "pak joko bayar cicilan 150000 langsung",
    "intent": "bayar_hutang",
    "entities": {
        "pelanggan": "pak joko",
        "nominal": "150000",
        "bayar": "langsung",
    },
}, {
    "text": "pak rudi bayar sisa 300000 transfer",
    "intent": "bayar_hutang",
    "entities": {
        "pelanggan": "pak rudi",
        "nominal": "300000",
        "bayar": "transfer",
    },
}, {
    "text": "pak soni bayar hutang 3000000 tf",
    "intent": "bayar_hutang",
    "entities": {
        "pelanggan": "pak soni",
        "nominal": "3000000",
        "bayar": "transfer",
    },
}, {
    "text": "pak wahyu lunasi tagihan 500000 tunai",
    "intent": "bayar_hutang",
    "entities": {
        "pelanggan": "pak wahyu",
        "nominal": "500000",
        "bayar": "tunai",
    },
}, {
    "text": "pak zio udah bayar 27 juta transfer",
    "intent": "bayar_hutang",
    "entities": {
        "pelanggan": "pak zio",
        "nominal": "27000000",
        "bayar": "transfer",
    },
}, {
    "text": "pelanggan paling banyak beli",
    "intent": "pembeli_terbanyak",
    "entities": {},
}, {
    "text": "pelanggan terbanyak",
    "intent": "pembeli_terbanyak",
    "entities": {},
}, {
    "text": "pemasukan kemarin",
    "intent": "total_uang_masuk",
    "entities": {
        "waktu": "kemarin",
    },
}, {
    "text": "pembeli paling banyak hari ini",
    "intent": "pembeli_terbanyak",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "pembeli yang bayar transfer",
    "intent": "filter_bayar_transfer",
    "entities": {
        "bayar": "transfer",
    },
}, {
    "text": "pembeli yang bayar tunai",
    "intent": "filter_bayar_cash",
    "entities": {
        "bayar": "tunai",
    },
}, {
    "text": "pembelian hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {},
}, {
    "text": "pembelian kemarin",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
        "waktu": "kemarin",
    },
}, {
    "text": "pendapatan hari ini",
    "intent": "total_uang_masuk",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "penjualan 21 april 2026",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
        "tanggal": "21-04-2026",
    },
}, {
    "text": "penjualan hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {},
}, {
    "text": "penjualan hari ini ada berapa",
    "intent": "cek_penjualan_hari_ini",
    "entities": {},
}, {
    "text": "penjualan hari ini bagaimana",
    "intent": "cek_penjualan_hari_ini",
    "entities": {},
}, {
    "text": "penjualan hari ini gimana",
    "intent": "cek_penjualan_hari_ini",
    "entities": {},
}, {
    "text": "penjualan kemarin",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
        "waktu": "kemarin",
    },
}, {
    "text": "penjualan tanggal 25",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
        "tanggal": "25",
    },
}, {
    "text": "perbaharui harga barang",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "perbaharui order pak hendra",
    "intent": "update_transaksi",
    "entities": {
        "pelanggan": "pak hendra",
    },
}, {
    "text": "perbaharui pesanan pak naha",
    "intent": "update_transaksi",
    "entities": {
        "pelanggan": "pak naha",
    },
}, {
    "text": "perbaharui transaksi zio",
    "intent": "update_transaksi",
    "entities": {
        "pelanggan": "zio",
    },
}, {
    "text": "perbahrui pesnan pak naha",
    "intent": "update_transaksi",
    "entities": {
        "pelanggan": "pak naha",
    },
}, {
    "text": "perbahrui transaksi zio",
    "intent": "update_transaksi",
    "entities": {
        "pelanggan": "zio",
    },
}, {
    "text": "perbarui pesanan ibu sari",
    "intent": "update_transaksi",
    "entities": {
        "pelanggan": "ibu sari",
    },
}, {
    "text": "permisi",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "pesanan ibu sari",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "ibu sari",
    },
}, {
    "text": "pesanan pak ardi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "pak ardi",
    },
}, {
    "text": "pesanan pak budi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "pak budi",
    },
}, {
    "text": "pesnan pak ardi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "pak ardi",
    },
}, {
    "text": "piutang pelanggan",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "produk apa saja",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "produk paling mahal",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
        "filter": "tertinggi",
    },
}, {
    "text": "produk termahal",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
        "filter": "tertinggi",
    },
}, {
    "text": "produk termurah",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
        "filter": "terendah",
    },
}, {
    "text": "ranking pembeli",
    "intent": "pembeli_terbanyak",
    "entities": {},
}, {
    "text": "rekap hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {},
}, {
    "text": "rekap kemarin",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
        "waktu": "kemarin",
    },
}, {
    "text": "rekap penjualan hari ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {},
}, {
    "text": "rekap pnjualan hri ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {},
}, {
    "text": "rekap semua transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "rekap tanggal 10",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
        "tanggal": "10",
    },
}, {
    "text": "rekap uang masuk",
    "intent": "total_uang_masuk",
    "entities": {},
}, {
    "text": "remove produk roti pia",
    "intent": "hapus_produk",
    "entities": {
        "produk": "roti pia",
    },
}, {
    "text": "ringkasan penjualan hari ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {},
}, {
    "text": "riwayat penjualan semua",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "riwayat pesanan pak andi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "pak andi",
    },
}, {
    "text": "salam",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "salam kenal",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "selamat malam",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "selamat pagi",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "selamat siang",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "selamat sore",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "semua transaksi ada apa aja",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "show semua transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "siapa bayar di tempat",
    "intent": "filter_bayar_cash",
    "entities": {
        "bayar": "langsung",
    },
}, {
    "text": "siapa beli hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {},
}, {
    "text": "siapa cicilan terbesar",
    "intent": "hutang_terbanyak",
    "entities": {},
}, {
    "text": "siapa hutang terbanyak",
    "intent": "hutang_terbanyak",
    "entities": {},
}, {
    "text": "siapa hutng trbanyak",
    "intent": "hutang_terbanyak",
    "entities": {},
}, {
    "text": "siapa masih ada cicilan",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "siapa pembeli paling banyak hari ini",
    "intent": "pembeli_terbanyak",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "siapa pembeli terbanyak",
    "intent": "pembeli_terbanyak",
    "entities": {},
}, {
    "text": "siapa pembeli terbanyak hari ini",
    "intent": "pembeli_terbanyak",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "siapa pembeli terbanyak kemarin",
    "intent": "pembeli_terbanyak",
    "entities": {
        "waktu": "kemarin",
    },
}, {
    "text": "siapa pembeli terbesar",
    "intent": "pembeli_terbanyak",
    "entities": {},
}, {
    "text": "siapa pesan barang hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {},
}, {
    "text": "siapa punya hutang paling besar",
    "intent": "hutang_terbanyak",
    "entities": {},
}, {
    "text": "siapa tggakn paling banyak",
    "intent": "hutang_terbanyak",
    "entities": {},
}, {
    "text": "siapa transaksi terbanyak hari ini",
    "intent": "pembeli_terbanyak",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "siapa tunggakan paling banyak",
    "intent": "hutang_terbanyak",
    "entities": {},
}, {
    "text": "siapa yang ambil barang hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {},
}, {
    "text": "siapa yang bayar cash",
    "intent": "filter_bayar_cash",
    "entities": {
        "bayar": "cash",
    },
}, {
    "text": "siapa yang bayar langsung",
    "intent": "filter_bayar_cash",
    "entities": {
        "bayar": "langsung",
    },
}, {
    "text": "siapa yang bayar transfer",
    "intent": "filter_bayar_transfer",
    "entities": {
        "bayar": "transfer",
    },
}, {
    "text": "siapa yang bayar tunai",
    "intent": "filter_bayar_cash",
    "entities": {
        "bayar": "tunai",
    },
}, {
    "text": "siapa yang beli hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {},
}, {
    "text": "siapa yang beli kemarin",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
        "waktu": "kemarin",
    },
}, {
    "text": "siapa yang belum bayar",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "siapa yang belum lunas",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "siapa yang cicilan",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "siapa yang kontan",
    "intent": "filter_bayar_cash",
    "entities": {
        "bayar": "kontan",
    },
}, {
    "text": "siapa yang masih hutang",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "siapa yang masih nyicil",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "siapa yang masih punya hutang",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "siapa yang order hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {},
}, {
    "text": "siapa yang order kemarin",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
        "waktu": "kemarin",
    },
}, {
    "text": "siapa yang paling banyak cicilan",
    "intent": "hutang_terbanyak",
    "entities": {},
}, {
    "text": "siapa yang paling banyak hutang",
    "intent": "hutang_terbanyak",
    "entities": {},
}, {
    "text": "siapa yang paling banyak order",
    "intent": "pembeli_terbanyak",
    "entities": {},
}, {
    "text": "siapa yang paling banyak pesan",
    "intent": "pembeli_terbanyak",
    "entities": {},
}, {
    "text": "siapa yang paling banyak tunggakan",
    "intent": "hutang_terbanyak",
    "entities": {},
}, {
    "text": "siapa yang pesan hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {},
}, {
    "text": "siapa yang tf",
    "intent": "filter_bayar_transfer",
    "entities": {
        "bayar": "transfer",
    },
}, {
    "text": "siapa yg bayar cash",
    "intent": "filter_bayar_cash",
    "entities": {
        "bayar": "cash",
    },
}, {
    "text": "siapa yg bayar lgsung",
    "intent": "filter_bayar_cash",
    "entities": {
        "bayar": "langsung",
    },
}, {
    "text": "siapa yg bayar transfr",
    "intent": "filter_bayar_transfer",
    "entities": {
        "bayar": "transfer",
    },
}, {
    "text": "siapa yg bayar tuni",
    "intent": "filter_bayar_cash",
    "entities": {
        "bayar": "tunai",
    },
}, {
    "text": "siapa yg blm bayar",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "siapa yg msh hutang",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "siapa yg msh nyicil",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "siapa yg order hri ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {},
}, {
    "text": "siapa yg paling banyak order hri ini",
    "intent": "pembeli_terbanyak",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "siapa yg pesan hri ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {},
}, {
    "text": "summary penjualan hari ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {},
}, {
    "text": "tagihan hari ini berapa",
    "intent": "total_tagihan",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "tagihan pelanggan",
    "intent": "total_tagihan",
    "entities": {},
}, {
    "text": "tambah barang",
    "intent": "tambah_produk",
    "entities": {},
}, {
    "text": "tambah barang baru",
    "intent": "tambah_produk",
    "entities": {},
}, {
    "text": "tambah barang brownis harga 2500 per bungkus",
    "intent": "tambah_produk",
    "entities": {
        "produk": "brownis",
        "harga": "2500",
        "satuan": "bungkus",
    },
}, {
    "text": "tambah barang brownis harga 2500 per toples",
    "intent": "tambah_produk",
    "entities": {
        "produk": "brownis",
        "harga": "2500",
        "satuan": "toples",
    },
}, {
    "text": "tambah barang permen cokalat",
    "intent": "tambah_produk",
    "entities": {
        "barang": "Permen Coklat",
    },
}, {
    "text": "tambah barang permen coklat",
    "intent": "tambah_produk",
    "entities": {
        "produk": "permen coklat",
    },
}, {
    "text": "tambah barang prmen cklat harga 13.000",
    "intent": "tambah_produk",
    "entities": {
        "produk": "permen coklat",
        "harga": "13000",
    },
}, {
    "text": "tambah barang produk permen coklat",
    "intent": "tambah_produk",
    "entities": {
        "produk": "permen coklat",
    },
}, {
    "text": "tambah barang roti pia bulus",
    "intent": "tambah_produk",
    "entities": {
        "produk": "roti pia bulus",
    },
}, {
    "text": "tambah produk baru",
    "intent": "tambah_produk",
    "entities": {},
}, {
    "text": "tambah produk brownis harga 2.500",
    "intent": "tambah_produk",
    "entities": {
        "produk": "brownis",
        "harga": "2500",
    },
}, {
    "text": "tambah produk permen cokalat",
    "intent": "tambah_produk",
    "entities": {
        "produk": "permen coklat",
    },
}, {
    "text": "tambah produk permen coklat harga 13.000",
    "intent": "tambah_produk",
    "entities": {
        "barang": "Permen Coklat",
        "harga": "13000",
    },
}, {
    "text": "tambah produk permen coklat harga 13000",
    "intent": "tambah_produk",
    "entities": {
        "produk": "permen coklat",
        "harga": "13000",
    },
}, {
    "text": "tambahkan barang brownis harga 2500",
    "intent": "tambah_produk",
    "entities": {
        "produk": "brownis",
        "harga": "2500",
    },
}, {
    "text": "tambahkan produk permen coklat harga 13000",
    "intent": "tambah_produk",
    "entities": {
        "produk": "permen coklat",
        "harga": "13000",
    },
}, {
    "text": "tampil semua transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "tampilan data penjualan kemarin",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
        "waktu": "kemarin",
    },
}, {
    "text": "tampilan semua transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "tampilan semua transaksi pak andi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "pak andi",
    },
}, {
    "text": "tampilan smua transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "tampilin data penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "tampilin semua transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "tampilin transaksi hri ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {},
}, {
    "text": "tampilin transaksi kmarin",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
        "waktu": "kemarin",
    },
}, {
    "text": "tampilkan barang",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "tampilkan daftar harga barang",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "tampilkan daftar hutang",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "tampilkan daftar transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "tampilkan data penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "tampilkan data penjualan kemarin",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
        "waktu": "kemarin",
    },
}, {
    "text": "tampilkan harga barang",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "tampilkan harga brownis",
    "intent": "cek_harga_produk_spesifik",
    "entities": {
        "produk": "brownis",
    },
}, {
    "text": "tampilkan harga produk",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "tampilkan hutang terbesar",
    "intent": "hutang_terbanyak",
    "entities": {},
}, {
    "text": "tampilkan jumlah pesanan dari pak andi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "pak andi",
    },
}, {
    "text": "tampilkan katalog produk",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "tampilkan pemasukan hari ini",
    "intent": "total_uang_masuk",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "tampilkan penjualan tanggal 21 april",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
        "tanggal": "21 april",
    },
}, {
    "text": "tampilkan pesanan pak andi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "pak andi",
    },
}, {
    "text": "tampilkan piutang",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "tampilkan produk",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "tampilkan rekap penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "tampilkan riwayat transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "tampilkan seluruh transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "tampilkan semua barang",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "tampilkan semua daftar penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "tampilkan semua data",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "tampilkan semua penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "tampilkan semua produk",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "tampilkan semua transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "tampilkan semua transaksi pak andi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "pak andi",
    },
}, {
    "text": "tampilkan smua brg",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "tampilkan smua prduk",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "tampilkan tagihan",
    "intent": "total_tagihan",
    "entities": {},
}, {
    "text": "tampilkan total transaksi hari ini",
    "intent": "total_transaksi",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "tampilkan transaksi cash",
    "intent": "filter_bayar_cash",
    "entities": {
        "bayar": "cash",
    },
}, {
    "text": "tampilkan transaksi hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {},
}, {
    "text": "tampilkan transaksi pak joko",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "pak joko",
    },
}, {
    "text": "tampilkan transaksi tanggal 28",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
        "tanggal": "28",
    },
}, {
    "text": "tampilkan transaksi tgl 28",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
        "tanggal": "28",
    },
}, {
    "text": "tampilkan transaksi transfer",
    "intent": "filter_bayar_transfer",
    "entities": {
        "bayar": "transfer",
    },
}, {
    "text": "tampilkan tunggakan",
    "intent": "total_tunggakan",
    "entities": {},
}, {
    "text": "tampilkan uang masuk kemarin",
    "intent": "total_uang_masuk",
    "entities": {
        "waktu": "kemarin",
    },
}, {
    "text": "tampilkan yang bayar cash",
    "intent": "filter_bayar_cash",
    "entities": {
        "bayar": "cash",
    },
}, {
    "text": "tampilkan yang bayar transfer",
    "intent": "filter_bayar_transfer",
    "entities": {
        "bayar": "transfer",
    },
}, {
    "text": "tampilkan yang belum lunas",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "tamplkan semua transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "tanggal 21 ada transaksi apa",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
        "tanggal": "21",
    },
}, {
    "text": "tanggal 28 ada order apa",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
        "tanggal": "28",
    },
}, {
    "text": "tgl 21 siapa yang beli",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
        "tanggal": "21",
    },
}, {
    "text": "top pembeli",
    "intent": "pembeli_terbanyak",
    "entities": {},
}, {
    "text": "total cash masuk hari ini",
    "intent": "total_uang_masuk",
    "entities": {
        "waktu": "hari ini",
        "bayar": "cash",
    },
}, {
    "text": "total cicilan",
    "intent": "total_tunggakan",
    "entities": {},
}, {
    "text": "total cicilan penjualan hari ini",
    "intent": "total_tunggakan",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "total hutang",
    "intent": "total_tunggakan",
    "entities": {},
}, {
    "text": "total order hari ini",
    "intent": "total_transaksi",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "total pemasukan",
    "intent": "total_uang_masuk",
    "entities": {},
}, {
    "text": "total pembelian hari ini",
    "intent": "total_transaksi",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "total pendapatan hari ini",
    "intent": "total_uang_masuk",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "total pesanan pak budi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {
        "pelanggan": "pak budi",
    },
}, {
    "text": "total piutang",
    "intent": "total_tagihan",
    "entities": {},
}, {
    "text": "total tagihan",
    "intent": "total_tagihan",
    "entities": {},
}, {
    "text": "total tagihan hari ini",
    "intent": "total_tagihan",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "total transaksi",
    "intent": "total_transaksi",
    "entities": {},
}, {
    "text": "total transaksi hari ini",
    "intent": "total_transaksi",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "total transaksi kemarin",
    "intent": "total_transaksi",
    "entities": {
        "waktu": "kemarin",
    },
}, {
    "text": "total transaksi minggu ini",
    "intent": "total_transaksi",
    "entities": {
        "waktu": "minggu ini",
    },
}, {
    "text": "total transfer masuk hari ini",
    "intent": "total_uang_masuk",
    "entities": {
        "waktu": "hari ini",
        "bayar": "transfer",
    },
}, {
    "text": "total tunggakan",
    "intent": "total_tunggakan",
    "entities": {},
}, {
    "text": "total tunggakan hari ini",
    "intent": "total_tunggakan",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "total uang masuk",
    "intent": "total_uang_masuk",
    "entities": {},
}, {
    "text": "transaksi hari ini apa saja",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {},
}, {
    "text": "transaksi hri ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {},
}, {
    "text": "transaksi kemarin",
    "intent": "tampilkan_transaksi_kemarin",
    "entities": {
        "waktu": "kemarin",
    },
}, {
    "text": "transaksi tanggal 20",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
        "tanggal": "20",
    },
}, {
    "text": "transaksi tanggal 21 bulan 4",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
        "tanggal": "21 bulan 4",
    },
}, {
    "text": "transaksi tgl 20",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {
        "tanggal": "20",
    },
}, {
    "text": "tunggakan hari ini",
    "intent": "total_tunggakan",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "tunggakan terbesar siapa",
    "intent": "hutang_terbanyak",
    "entities": {},
}, {
    "text": "uang masuk hari ini berapa",
    "intent": "total_uang_masuk",
    "entities": {
        "waktu": "hari ini",
    },
}, {
    "text": "uang masuk kemarin",
    "intent": "total_uang_masuk",
    "entities": {
        "waktu": "kemarin",
    },
}, {
    "text": "ubah data pesanan pak wahyu",
    "intent": "update_transaksi",
    "entities": {
        "pelanggan": "pak wahyu",
    },
}, {
    "text": "ubah harga barang",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "ubah harga permen",
    "intent": "edit_produk",
    "entities": {
        "produk": "permen",
    },
}, {
    "text": "ubah harga produk",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "ubah nama produk",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "ubah order pak doni",
    "intent": "update_transaksi",
    "entities": {
        "pelanggan": "pak doni",
    },
}, {
    "text": "ubah pesanan pak naha",
    "intent": "update_transaksi",
    "entities": {
        "pelanggan": "pak naha",
    },
}, {
    "text": "ubah pesnan pak naha",
    "intent": "update_transaksi",
    "entities": {
        "pelanggan": "pak naha",
    },
}, {
    "text": "ubah produk permen",
    "intent": "edit_produk",
    "entities": {
        "produk": "permen",
    },
}, {
    "text": "ubah transaksi pak andi",
    "intent": "update_transaksi",
    "entities": {
        "pelanggan": "pak andi",
    },
}, {
    "text": "update data pesnan naha",
    "intent": "update_transaksi",
    "entities": {
        "pelanggan": "naha",
    },
}, {
    "text": "update harga barang",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "update harga permen",
    "intent": "edit_produk",
    "entities": {
        "produk": "permen",
    },
}, {
    "text": "update harga produk",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "update nama produk",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "update penjualan hari ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {},
}, {
    "text": "update pesanan naha",
    "intent": "update_transaksi",
    "entities": {
        "pelanggan": "naha",
    },
}, {
    "text": "update produk roti pia",
    "intent": "edit_produk",
    "entities": {
        "produk": "roti pia",
    },
}, {
    "text": "update transaksi pak rudi",
    "intent": "update_transaksi",
    "entities": {
        "pelanggan": "pak rudi",
    },
}, {
    "text": "yang bayar cash siapa",
    "intent": "filter_bayar_cash",
    "entities": {
        "bayar": "cash",
    },
}, {
    "text": "yang bayar transfer siapa",
    "intent": "filter_bayar_transfer",
    "entities": {
        "bayar": "transfer",
    },
}, {
    "text": "yang belum bayar siapa",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "yang paling sering beli siapa",
    "intent": "pembeli_terbanyak",
    "entities": {},
}, {
    "text": "yg bayar transfr siapa",
    "intent": "filter_bayar_transfer",
    "entities": {
        "bayar": "transfer",
    },
}, {
    "text": "zio bayar hutang 27000000 transfer",
    "intent": "bayar_hutang",
    "entities": {
        "pelanggan": "zio",
        "nominal": "27000000",
        "bayar": "transfer",
    },
}, {
    "text": "zio bayar hutng 27000000 transfr",
    "intent": "bayar_hutang",
    "entities": {
        "pelanggan": "zio",
        "nominal": "27000000",
        "bayar": "transfer",
    },
}, {
    "text": "zio bayar taghn 27 juta",
    "intent": "bayar_hutang",
    "entities": {
        "pelanggan": "zio",
        "nominal": "27000000",
    },
}, {
    "text": "zio bayar tagihan 27 juta",
    "intent": "bayar_hutang",
    "entities": {
        "pelanggan": "zio",
        "nominal": "27000000",
    },
}, {
    "text": "zio transfer 27 jt buat lunasin hutang",
    "intent": "bayar_hutang",
    "entities": {
        "pelanggan": "zio",
        "nominal": "27000000",
        "bayar": "transfer",
    },
}, {
    "text": "hari ini andi pesan l0lipop 10 dus",
    "intent": " tambah_transaksi_lunas_cash",
    "entities": {
        "pelanggan": "andi",
        "produk": "lolipop",
        "jumlah": "10",
        "satuan": "dus",
    },
}, {
    "text": "hari ini budi pesan loli pop 5 toples",
    "intent": " tambah_transaksi_lunas_cash",
    "entities": {
        "pelanggan": "budi",
        "produk": "lolipop",
        "jumlah": "5",
        "satuan": "toples",
    },
}, {
    "text": "hari ini nala pesan lolly pop 8 pack",
    "intent": " tambah_transaksi_lunas_cash",
    "entities": {
        "pelanggan": "nala",
        "produk": "lolipop",
        "jumlah": "8",
        "satuan": "pack",
    },
}, {
    "text": "hari ini rara pesan l0llip0p 12 pcs",
    "intent": " tambah_transaksi_lunas_cash",
    "entities": {
        "pelanggan": "rara",
        "produk": "lolipop",
        "jumlah": "12",
        "satuan": "pcs",
    },
}, {
    "text": "hari ini zio pesan lolypop 6 bungkus",
    "intent": " tambah_transaksi_lunas_cash",
    "entities": {
        "pelanggan": "zio",
        "produk": "lolipop",
        "jumlah": "6",
        "satuan": "bungkus",
    },
}, {
    "text": "berapa harga l0lipop",
    "intent": " cek_harga_produk_spesifik",
    "entities": {
        "produk": "lolipop",
    },
}, {
    "text": "berapa harga loli pop",
    "intent": " cek_harga_produk_spesifik",
    "entities": {
        "produk": "lolipop",
    },
}, {
    "text": "berapa harga lolly pop",
    "intent": " cek_harga_produk_spesifik",
    "entities": {
        "produk": "lolipop",
    },
}, {
    "text": "tambah barang l0lipop harga 15000 per pack",
    "intent": " tambah_produk",
    "entities": {
        "produk": "lolipop",
        "harga": "15000",
        "satuan": "pack",
    },
}, {
    "text": "edit harga l0lipop jadi 16000",
    "intent": " edit_produk",
    "entities": {
        "produk": "lolipop",
        "harga_baru": "16000",
    },
}, {
    "text": "hapus barang l0lipop",
    "intent": " hapus_produk",
    "entities": {
        "produk": "lolipop",
    },
}, {
    "text": "pak budi ambil willo 2 toples",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "pelanggan": "pak budi",
        "produk": "willo",
        "jumlah": "2",
        "satuan": "toples",
    },
}, {
    "text": "naha beli beem-beeng 1 karton",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "pelanggan": "naha",
        "produk": "beem-beeng",
        "jumlah": "1",
        "satuan": "karton",
    },
}, {
    "text": "adangrow 5 pouch",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "produk": "adangrow",
        "jumlah": "5",
        "satuan": "pouch",
    },
}, {
    "text": "siperquuen 10 pack",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "produk": "siperquuen",
        "jumlah": "10",
        "satuan": "pack",
    },
}, {
    "text": "chocholetus 3 toples lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "produk": "chocholetus",
        "jumlah": "3",
        "satuan": "toples",
        "status": "lunas",
    },
}, {
    "text": "miksu 1 paket",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "produk": "miksu",
        "jumlah": "1",
        "satuan": "paket",
    },
}, {
    "text": "lolipop 50 pcs",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "produk": "lolipop",
        "jumlah": "50",
        "satuan": "pcs",
    },
}, {
    "text": "coklat kubus 5 toples",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "produk": "coklat kubus",
        "jumlah": "5",
        "satuan": "toples",
    },
}, {
    "text": "piramide 2 dus",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "produk": "piramide",
        "jumlah": "2",
        "satuan": "dus",
    },
}, {
    "text": "mesis 10 bungkus",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "produk": "mesis",
        "jumlah": "10",
        "satuan": "bungkus",
    },
}, {
    "text": "salju 1 toples",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "produk": "salju",
        "jumlah": "1",
        "satuan": "toples",
    },
}, {
    "text": "serbuk jelli 5 pouch",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "produk": "serbuk jelli",
        "jumlah": "5",
        "satuan": "pouch",
    },
}, {
    "text": "pia bulus 2 toples",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "produk": "pia bulus",
        "jumlah": "2",
        "satuan": "toples",
    },
}, {
    "text": "pia roda 1 ctn",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "produk": "pia roda",
        "jumlah": "1",
        "satuan": "karton",
    },
}, {
    "text": "hari ini andi ambil permen 3 dus lunas transfer",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
        "pelanggan": "Andi",
        "barang": "Permen",
        "jumlah": "3",
        "satuan": "dus",
        "status": "Lunas",
        "metode": "Transfer",
    },
}, {
    "text": "hari ini budi beli brownis 10 bungkus lunas tf",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
        "pelanggan": "Budi",
        "barang": "Brownis",
        "jumlah": "10",
        "satuan": "bungkus",
        "status": "Lunas",
        "metode": "Transfer",
    },
}, {
    "text": "pak ardi pesan serbuk 2 karton sudah dibayar transfer",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
        "pelanggan": "Ardi",
        "barang": "Serbuk",
        "jumlah": "2",
        "satuan": "karton",
        "status": "Lunas",
        "metode": "Transfer",
    },
}, {
    "text": "rara order permen coklat 5 dus dibayar qris",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
        "pelanggan": "Rara",
        "barang": "Permen Coklat",
        "jumlah": "5",
        "satuan": "dus",
        "status": "Lunas",
        "metode": "QRIS",
    },
}, {
    "text": "udin ambil permen 1 dus lunas via qris",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
        "pelanggan": "Udin",
        "barang": "Permen",
        "jumlah": "1",
        "satuan": "dus",
        "status": "Lunas",
        "metode": "QRIS",
    },
}, {
    "text": "nala ambil roti pia 2 toples sudah lunas transfer bca",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
        "pelanggan": "Nala",
        "barang": "Roti Pia",
        "jumlah": "2",
        "satuan": "toples",
        "status": "Lunas",
        "metode": "Transfer",
    },
}, {
    "text": "mas dodi beli mesis 4 bungkus bayar trf",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
        "pelanggan": "Dodi",
        "barang": "Mesis",
        "jumlah": "4",
        "satuan": "bungkus",
        "status": "Lunas",
        "metode": "Transfer",
    },
}, {
    "text": "kak rina order salju 1 toples lunas transfer",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
        "pelanggan": "Rina",
        "barang": "Salju",
        "jumlah": "1",
        "satuan": "toples",
        "status": "Lunas",
        "metode": "Transfer",
    },
}, {
    "text": "zio ambil pia bulus 1 toples lunas qris",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
        "pelanggan": "Zio",
        "barang": "Pia Bulus",
        "jumlah": "1",
        "satuan": "toples",
        "status": "Lunas",
        "metode": "QRIS",
    },
}, {
    "text": "hari ini sinta beli lolipop 20 pcs dibayar transfer",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
        "pelanggan": "Sinta",
        "barang": "Lolipop",
        "jumlah": "20",
        "satuan": "pcs",
        "status": "Lunas",
        "metode": "Transfer",
    },
}, {
    "text": "hari ini akbar pesan coklat kubus 2 toples lunas tf",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
        "pelanggan": "Akbar",
        "barang": "Coklat Kubus",
        "jumlah": "2",
        "satuan": "toples",
        "status": "Lunas",
        "metode": "Transfer",
    },
}, {
    "text": "hari ini iwan ambil serbuk jelli 6 pouch lunas transfer bri",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
        "pelanggan": "Iwan",
        "barang": "Serbuk Jelli",
        "jumlah": "6",
        "satuan": "pouch",
        "status": "Lunas",
        "metode": "Transfer",
    },
}, {
    "text": "pak agus ambil permen 2 dus dibayar transfer mandiri",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
        "pelanggan": "Agus",
        "barang": "Permen",
        "jumlah": "2",
        "satuan": "dus",
        "status": "Lunas",
        "metode": "Transfer",
    },
}, {
    "text": "hari ini dini beli permen 10 pcs lunas trf",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
        "pelanggan": "Dini",
        "barang": "Permen",
        "jumlah": "10",
        "satuan": "pcs",
        "status": "Lunas",
        "metode": "Transfer",
    },
}, {
    "text": "hari ini rudi pesan piramide 1 dus sudah dibayar qris",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
        "pelanggan": "Rudi",
        "barang": "Piramide",
        "jumlah": "1",
        "satuan": "dus",
        "status": "Lunas",
        "metode": "QRIS",
    },
}, {
    "text": "hari ini andi order permen 30 toples dicicil 200000 transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
        "pelanggan": "Andi",
        "barang": "Permen",
        "jumlah": "30",
        "satuan": "toples",
        "status": "Cicil",
        "nominal_bayar": "200000",
        "metode": "Transfer",
    },
}, {
    "text": "hari ini budi ambil brownis 20 bungkus dp 150000 transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
        "pelanggan": "Budi",
        "barang": "Brownis",
        "jumlah": "20",
        "satuan": "bungkus",
        "status": "Cicil",
        "nominal_bayar": "150000",
        "metode": "Transfer",
    },
}, {
    "text": "nala pesan permen 10 dus dicicil 500000 dibayar transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
        "pelanggan": "Nala",
        "barang": "Permen",
        "jumlah": "10",
        "satuan": "dus",
        "status": "Cicil",
        "nominal_bayar": "500000",
        "metode": "Transfer",
    },
}, {
    "text": "rara ambil permen coklat 4 dus uang muka 100000 transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
        "pelanggan": "Rara",
        "barang": "Permen Coklat",
        "jumlah": "4",
        "satuan": "dus",
        "status": "Cicil",
        "nominal_bayar": "100000",
        "metode": "Transfer",
    },
}, {
    "text": "udin order serbuk 2 karton nyicil 250000 trf",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
        "pelanggan": "Udin",
        "barang": "Serbuk",
        "jumlah": "2",
        "satuan": "karton",
        "status": "Cicil",
        "nominal_bayar": "250000",
        "metode": "Transfer",
    },
}, {
    "text": "hari ini zio ambil roti pia 3 toples dicicil 120000 transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
        "pelanggan": "Zio",
        "barang": "Roti Pia",
        "jumlah": "3",
        "satuan": "toples",
        "status": "Cicil",
        "nominal_bayar": "120000",
        "metode": "Transfer",
    },
}, {
    "text": "pak ardi pesan mesis 8 bungkus bayar dp 50000 transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
        "pelanggan": "Ardi",
        "barang": "Mesis",
        "jumlah": "8",
        "satuan": "bungkus",
        "status": "Cicil",
        "nominal_bayar": "50000",
        "metode": "Transfer",
    },
}, {
    "text": "hari ini sinta ambil salju 2 toples bayar sebagian 70000 transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
        "pelanggan": "Sinta",
        "barang": "Salju",
        "jumlah": "2",
        "satuan": "toples",
        "status": "Cicil",
        "nominal_bayar": "70000",
        "metode": "Transfer",
    },
}, {
    "text": "hari ini iwan order permen 100 pcs dicicil 100000 transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
        "pelanggan": "Iwan",
        "barang": "Permen",
        "jumlah": "100",
        "satuan": "pcs",
        "status": "Cicil",
        "nominal_bayar": "100000",
        "metode": "Transfer",
    },
}, {
    "text": "akbar pesan pia bulus 5 toples dp 200000 transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
        "pelanggan": "Akbar",
        "barang": "Pia Bulus",
        "jumlah": "5",
        "satuan": "toples",
        "status": "Cicil",
        "nominal_bayar": "200000",
        "metode": "Transfer",
    },
}, {
    "text": "dini ambil coklat kubus 2 toples dicicil 80000 transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
        "pelanggan": "Dini",
        "barang": "Coklat Kubus",
        "jumlah": "2",
        "satuan": "toples",
        "status": "Cicil",
        "nominal_bayar": "80000",
        "metode": "Transfer",
    },
}, {
    "text": "hari ini rudi order piramide 3 dus dicicil 300000 transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
        "pelanggan": "Rudi",
        "barang": "Piramide",
        "jumlah": "3",
        "satuan": "dus",
        "status": "Cicil",
        "nominal_bayar": "300000",
        "metode": "Transfer",
    },
}, {
    "text": "hari ini agus order permen 40 pcs dicicil setengah 200000 transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
        "pelanggan": "Agus",
        "barang": "Permen",
        "jumlah": "40",
        "satuan": "pcs",
        "status": "Cicil",
        "nominal_bayar": "200000",
        "metode": "Transfer",
    },
}, {
    "text": "hari ini andi order permen 30 toples dicicil 200000 tunai",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
        "pelanggan": "Andi",
        "barang": "Permen",
        "jumlah": "30",
        "satuan": "toples",
        "status": "Cicil",
        "nominal_bayar": "200000",
        "metode": "Tunai",
    },
}, {
    "text": "hari ini budi ambil brownis 20 bungkus dp 150000 cash",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
        "pelanggan": "Budi",
        "barang": "Brownis",
        "jumlah": "20",
        "satuan": "bungkus",
        "status": "Cicil",
        "nominal_bayar": "150000",
        "metode": "Tunai",
    },
}, {
    "text": "nala pesan permen 10 dus dicicil 500000 dibayar tunai",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
        "pelanggan": "Nala",
        "barang": "Permen",
        "jumlah": "10",
        "satuan": "dus",
        "status": "Cicil",
        "nominal_bayar": "500000",
        "metode": "Tunai",
    },
}, {
    "text": "rara ambil permen coklat 4 dus uang muka 100000 tunai",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
        "pelanggan": "Rara",
        "barang": "Permen Coklat",
        "jumlah": "4",
        "satuan": "dus",
        "status": "Cicil",
        "nominal_bayar": "100000",
        "metode": "Tunai",
    },
}, {
    "text": "udin order serbuk 2 karton nyicil 250000 tunai",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
        "pelanggan": "Udin",
        "barang": "Serbuk",
        "jumlah": "2",
        "satuan": "karton",
        "status": "Cicil",
        "nominal_bayar": "250000",
        "metode": "Tunai",
    },
}, {
    "text": "hari ini zio ambil roti pia 3 toples dicicil 120000 tunai",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
        "pelanggan": "Zio",
        "barang": "Roti Pia",
        "jumlah": "3",
        "satuan": "toples",
        "status": "Cicil",
        "nominal_bayar": "120000",
        "metode": "Tunai",
    },
}, {
    "text": "pak ardi pesan mesis 8 bungkus bayar dp 50000 tunai",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
        "pelanggan": "Ardi",
        "barang": "Mesis",
        "jumlah": "8",
        "satuan": "bungkus",
        "status": "Cicil",
        "nominal_bayar": "50000",
        "metode": "Tunai",
    },
}, {
    "text": "hari ini sinta ambil salju 2 toples bayar sebagian 70000 tunai",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
        "pelanggan": "Sinta",
        "barang": "Salju",
        "jumlah": "2",
        "satuan": "toples",
        "status": "Cicil",
        "nominal_bayar": "70000",
        "metode": "Tunai",
    },
}, {
    "text": "hari ini iwan order permen 100 pcs dicicil 100000 tunai",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
        "pelanggan": "Iwan",
        "barang": "Permen",
        "jumlah": "100",
        "satuan": "pcs",
        "status": "Cicil",
        "nominal_bayar": "100000",
        "metode": "Tunai",
    },
}, {
    "text": "akbar pesan pia bulus 5 toples dp 200000 tunai",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
        "pelanggan": "Akbar",
        "barang": "Pia Bulus",
        "jumlah": "5",
        "satuan": "toples",
        "status": "Cicil",
        "nominal_bayar": "200000",
        "metode": "Tunai",
    },
}, {
    "text": "dini ambil coklat kubus 2 toples dicicil 80000 tunai",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
        "pelanggan": "Dini",
        "barang": "Coklat Kubus",
        "jumlah": "2",
        "satuan": "toples",
        "status": "Cicil",
        "nominal_bayar": "80000",
        "metode": "Tunai",
    },
}, {
    "text": "jual 2 aqua bayar qris",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
        "barang": "Aqua",
        "jumlah": "2",
        "satuan": "botol",
        "status": "Lunas",
        "metode": "QRIS",
    },
}, {
    "text": "jual 3 permen bayar transfer",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
        "barang": "Permen",
        "jumlah": "3",
        "status": "Lunas",
        "metode": "Transfer",
    },
}, {
    "text": "jual 1 brownis bayar tunai",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "barang": "Brownis",
        "jumlah": "1",
        "status": "Lunas",
        "metode": "Tunai",
    },
}, {
    "text": "jual 5 permen dicicil 20000 tunai",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
        "barang": "Permen",
        "jumlah": "5",
        "status": "Cicil",
        "nominal_bayar": "20000",
        "metode": "Tunai",
    },
}, {
    "text": "jual 5 permen dicicil 20000 transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
        "barang": "Permen",
        "jumlah": "5",
        "status": "Cicil",
        "nominal_bayar": "20000",
        "metode": "Transfer",
    },
}, {
    "text": "jual 10 roti pia bayar cash",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "barang": "Roti Pia",
        "jumlah": "10",
        "status": "Lunas",
        "metode": "Tunai",
    },
}, {
    "text": "jual 1 serbuk bayar trf",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
        "barang": "Serbuk",
        "jumlah": "1",
        "status": "Lunas",
        "metode": "Transfer",
    },
}, {
    "text": "jual permen 2 dus bayar tunai",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "barang": "Permen",
        "jumlah": "2",
        "satuan": "dus",
        "status": "Lunas",
        "metode": "Tunai",
    },
}, {
    "text": "jual permen 2 dus bayar tf",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
        "barang": "Permen",
        "jumlah": "2",
        "satuan": "dus",
        "status": "Lunas",
        "metode": "Transfer",
    },
}, {
    "text": "jual 2 permen dp 10000 tunai",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
        "barang": "Permen",
        "jumlah": "2",
        "status": "Cicil",
        "nominal_bayar": "10000",
        "metode": "Tunai",
    },
}, {
    "text": "jual 2 aqua bayar tunai",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "barang": "Aqua",
        "jumlah": "2",
        "satuan": "botol",
        "status": "Lunas",
        "metode": "Tunai",
    },
}, {
    "text": "jual 1 aqua lunas tunai",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "barang": "Aqua",
        "jumlah": "1",
        "satuan": "botol",
        "status": "Lunas",
        "metode": "Tunai",
    },
}, {
    "text": "jual 3 permen kontan",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "barang": "Permen",
        "jumlah": "3",
        "status": "Lunas",
        "metode": "Tunai",
    },
}, {
    "text": "jual 2 serbuk bayar cash",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "barang": "Serbuk",
        "jumlah": "2",
        "status": "Lunas",
        "metode": "Tunai",
    },
}, {
    "text": "jual 5 mesis bayar tunai",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "barang": "Mesis",
        "jumlah": "5",
        "status": "Lunas",
        "metode": "Tunai",
    },
}, {
    "text": "jual 1 piramide lunas cash",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "barang": "Piramide",
        "jumlah": "1",
        "satuan": "dus",
        "status": "Lunas",
        "metode": "Tunai",
    },
}, {
    "text": "jual 4 pia bulus dibayar tunai",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "barang": "Pia Bulus",
        "jumlah": "4",
        "satuan": "toples",
        "status": "Lunas",
        "metode": "Tunai",
    },
}, {
    "text": "jual 10 lolipop bayar tunai",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "barang": "Lolipop",
        "jumlah": "10",
        "satuan": "pcs",
        "status": "Lunas",
        "metode": "Tunai",
    },
}, {
    "text": "hari ini pak andi pesan permen 50 pcs",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {},
}, {
    "text": "hari ini pak agus ngambil permen coklat 2 dus",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {},
}, {
    "text": "hari ini rara ambil permen coklat 13 dus lunas cash",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {},
}, {
    "text": "hari ini udin ngambil permen 30 dus lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {},
}, {
    "text": "hari ini naha ambil permen 50 dus lunas transfer",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {},
}, {
    "text": "hari ini nala ambil permen 70 dus cicil 2000000 tf",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {},
}, {
    "text": "hari ini nala ambil brownis 100 bungkus cicil 1000000 transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {},
}, {
    "text": "hari ini nala ambil serbuk 100 lunas tf",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {},
}, {
    "text": "hari ini rudi order permen 600 toples cicil 200000 transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {},
}, {
    "text": "hari ini rudi order permen 600 toples cicil 200000 lunas",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {},
}, {
    "text": "hari ini rudi order permen 600 toples cicil 200000 tunai",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {},
}, {
    "text": "hari ini budi order permen 30 toples cicil 200000 cash langsung",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {},
}, {
    "text": "hari ini rudi order permen 600 toples lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {},
}, {
    "text": "hari ini andi order permen 600 toples cicil 200000 cash",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {},
}, {
    "text": "hari ini rudi order permen 600 toples cicil 200000 langsung",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {},
}, {
    "text": "hari ini supri ambil permen 20 toples lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {},
}, {
    "text": "kemarin pak ardi beli brownis 100 buah lunas cash",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {},
}, {
    "text": "kemarin ardi ambil brownis 100 udah bayar tunai",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {},
}, {
    "text": "besok ardi ambil brownis 100 buah lunas",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {},
}, {
    "text": "lusa ardi ambil brownis 100 buah lunas cash",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {},
}, {
    "text": "3 hari lalu ardi ambil brownis 100 lunas tunai",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {},
}, {
    "text": "2 hari yang lalu budi ambil permen 50 dus lunas",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {},
}, {
    "text": "3 hari ke depan ardi ambil brownis 100 lunas",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {},
}, {
    "text": "minggu dpan ardi ambil brownis 100 lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {},
}, {
    "text": "1 minggu ke depan ardi ambil brownis 100 lunas",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {},
}, {
    "text": "hari selasa pak ardi ambil brownis 100 lunas",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {},
}, {
    "text": "hari rabu naha ambil permen 50 dus lunas transfer",
    "intent": "tambah_transaksi_tanggal_spesifik",
    "entities": {},
}, {
    "text": "hari ini pak andi oredre permen 50 pcs",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {},
}, {
    "text": "hri ini pak andi order prmen 50 pcs",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {},
}, {
    "text": "hari ini paka andi order permen 50 pcs",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {},
}, {
    "text": "hari ni pak andi order permen 50 pcs lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {},
}, {
    "text": "hri ini rudi ordr permen 600 toples cicil 200000 tf",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {},
}, {
    "text": "hari ini budi ambl brownis 30 bungkus luans",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {},
}, {
    "text": "kemrin ardi ambil brownis 100 udah bayar tnai",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {},
}, {
    "text": "minggu dpan ardi ambl brownis 100 lunas tunai",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {},
}, {
    "text": "hari ini supri ambil permen 20 topls sudah lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {},
}, {
    "text": "hari ini nala ambl srbuk 100 lunas transfer",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {},
}, {
    "text": "tadi andi beli permen 50 pcs lunas cash",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {},
}, {
    "text": "pak andi beli permen 50 pcs hari ini lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {},
}, {
    "text": "pak agus pesan permen coklat 2 dus hari ini",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {},
}, {
    "text": "pak agus beli permen coklat 2 dus hari ini",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {},
}, {
    "text": "pak agus transaksi permen coklat 2 dus hari ini lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {},
}, {
    "text": "catat pesanan pak andi permen 50 pcs hari ini lunas cash",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {},
}, {
    "text": "input transaksi pak andi permen 50 pcs hari ini lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {},
}, {
    "text": "tambah transaksi pak andi permen 50 pcs hari ini",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {},
}, {
    "text": "simpan transaksi pak andi permen 50 pcs hari ini lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {},
}, {
    "text": "rekap pak andi beli permen 50 pcs hari ini lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {},
}, {
    "text": "tampil semua daftar penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "lihat semua daftar penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "tampilkan semua data penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "tampilkan data penjualan hari ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {},
}, {
    "text": "tampilkan data penjualan lusa",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "lihat data penjualan hari ini",
    "intent": "cek_penjualan_hari_ini",
    "entities": {},
}, {
    "text": "lihat pesanan hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {},
}, {
    "text": "tampilkan pesanan hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {},
}, {
    "text": "cek pesanan tanggal 21 april 2026",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {},
}, {
    "text": "tampilkan pesanan tanggal 21 april",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {},
}, {
    "text": "lihat transaksi tanggal 28",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {},
}, {
    "text": "data tanggal 28",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {},
}, {
    "text": "pesanan tanggal 28",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {},
}, {
    "text": "tampilkan semua transaksi/data/pembelian pak andi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "tampilkan semua data pak andi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "tampilkan semua pembelian pak andi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "tampilkan jumlah pesanan pak andi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {},
}, {
    "text": "riwayat pesanan pak ardi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {},
}, {
    "text": "Cek pesanan/transaksi udin",
    "intent": "cek_pesanan_pelanggan",
    "entities": {},
}, {
    "text": "lihat transaksi udin",
    "intent": "cek_pesanan_pelanggan",
    "entities": {},
}, {
    "text": "riwayat udin",
    "intent": "cek_pesanan_pelanggan",
    "entities": {},
}, {
    "text": "tampilkaan semua data penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "liht semua daftar penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "tampilkan semua tranksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "tampilkan dat penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "pesanan pak ardi hari ini",
    "intent": "cek_pesanan_pelanggan",
    "entities": {},
}, {
    "text": "tampiln transaksi tanggal 28",
    "intent": "tampilkan_transaksi_tanggal",
    "entities": {},
}, {
    "text": "liat semua transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "liat transaksi hari ini",
    "intent": "tampilkan_transaksi_hari_ini",
    "entities": {},
}, {
    "text": "liat pesanan udin",
    "intent": "cek_pesanan_pelanggan",
    "entities": {},
}, {
    "text": "lht riwayat pak andi",
    "intent": "cek_pesanan_pelanggan",
    "entities": {},
}, {
    "text": "print semua data penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "tampung semua transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "daftar semua penjualan",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "list semua transaksi",
    "intent": "tampilkan_semua_transaksi",
    "entities": {},
}, {
    "text": "Hapus semua data penjualan/transaksi",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "hapus semua data/daftar penjualan",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "hapus semua data",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "hapus seluruh data penjualan",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "hapus semua rekap penjualan",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "hapus pesanan udin belum lunas",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "hapus transaksi udin belum lunas",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "hapus pesanan/transaksi udin",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "hapus data udin",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "hapus pesanan pak ardi",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "hapus data pak andi",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "hapus pembelian pak andi",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "hapus semwa data penjualan",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "hapus semu transaksi",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "hapus penjualan udin",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "hapus pesenan udin",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "hpus semua data penjualan",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "hapus pesanaan pak ardi",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "hps semua transaksi",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "hapus semua dat penjualan",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "hapus transaks udin",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "remove pesanan udin",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "clear semua data penjualan",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "bersihkan semua data penjualan",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "hilangkan semua transaksi",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "hapusin semua data penjualan",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "hapusin pesanan udin",
    "intent": "hapus_transaksi",
    "entities": {},
}, {
    "text": "Update pesanan/transaksi naha",
    "intent": "update_transaksi",
    "entities": {},
}, {
    "text": "update transaksi naha",
    "intent": "update_transaksi",
    "entities": {},
}, {
    "text": "Perbaharui/ubah/edit pesanan pak naha",
    "intent": "update_transaksi",
    "entities": {},
}, {
    "text": "edit transaksi zio",
    "intent": "update_transaksi",
    "entities": {},
}, {
    "text": "ubah transaksi zio",
    "intent": "update_transaksi",
    "entities": {},
}, {
    "text": "update data pak ardi",
    "intent": "update_transaksi",
    "entities": {},
}, {
    "text": "ubah data pesanan pak ardi",
    "intent": "update_transaksi",
    "entities": {},
}, {
    "text": "edit data pesanan pak andi",
    "intent": "update_transaksi",
    "entities": {},
}, {
    "text": "perbarui pesanan pak andi",
    "intent": "update_transaksi",
    "entities": {},
}, {
    "text": "ganti status pesanan pak andi",
    "intent": "update_transaksi",
    "entities": {},
}, {
    "text": "ganti status bayar pak andi jadi lunas",
    "intent": "update_transaksi",
    "entities": {},
}, {
    "text": "ubah status bayar naha jadi lunas",
    "intent": "update_transaksi",
    "entities": {},
}, {
    "text": "edit status pembayaran udin",
    "intent": "update_transaksi",
    "entities": {},
}, {
    "text": "zio bayar hutang 27 juta transfer",
    "intent": "Pelunasan_Hutang",
    "entities": {},
}, {
    "text": "zio bayar tagihan 27000000",
    "intent": "Pelunasan_Hutang",
    "entities": {},
}, {
    "text": "zio lunasin tagihan 27 juta",
    "intent": "Pelunasan_Hutang",
    "entities": {},
}, {
    "text": "zio bayar cicilan 27 juta transfer",
    "intent": "Pelunasan_Hutang",
    "entities": {},
}, {
    "text": "zio bayar 27000000 tf",
    "intent": "update_transaksi",
    "entities": {},
}, {
    "text": "updaet pesanan naha",
    "intent": "update_transaksi",
    "entities": {},
}, {
    "text": "update pesanaan naha",
    "intent": "update_transaksi",
    "entities": {},
}, {
    "text": "perbaharui pesenan pak naha",
    "intent": "update_transaksi",
    "entities": {},
}, {
    "text": "edti transaksi zio",
    "intent": "update_transaksi",
    "entities": {},
}, {
    "text": "edit transaks zio",
    "intent": "update_transaksi",
    "entities": {},
}, {
    "text": "ubah transksi pak ardi",
    "intent": "update_transaksi",
    "entities": {},
}, {
    "text": "update dat pak ardi",
    "intent": "update_transaksi",
    "entities": {},
}, {
    "text": "zio byr hutang 27 juta tf",
    "intent": "update_transaksi",
    "entities": {},
}, {
    "text": "modify pesanan naha",
    "intent": "update_transaksi",
    "entities": {},
}, {
    "text": "revisi pesanan pak naha",
    "intent": "update_transaksi",
    "entities": {},
}, {
    "text": "koreksi transaksi zio",
    "intent": "update_transaksi",
    "entities": {},
}, {
    "text": "change data pesanan pak ardi",
    "intent": "update_transaksi",
    "entities": {},
}, {
    "text": "ganti data transaksi pak andi",
    "intent": "update_transaksi",
    "entities": {},
}, {
    "text": "Cek/tampilkan harga barang/produk",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "cek harga produk",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "tampil semua barang/produk",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "lihat daftar harga barang",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "lihat semua produk",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "harga brownis berapa",
    "intent": "cek_harga_produk_spesifik",
    "entities": {},
}, {
    "text": "lihat harga brownis",
    "intent": "cek_harga_produk_spesifik",
    "entities": {},
}, {
    "text": "harga produk tertinggi",
    "intent": "cek_harga_produk_spesifik",
    "entities": {},
}, {
    "text": "harga termahal",
    "intent": "cek_harga_produk_spesifik",
    "entities": {},
}, {
    "text": "produk apa yang paling mahal",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "cek hraga permen",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "tampilkan hrga barang",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "cek hrga produk",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "berapa hraga permen",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "berapa hrga brownis",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "tampilkan semua barng",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "liat harga permen",
    "intent": "cek_harga_produk_spesifik",
    "entities": {},
}, {
    "text": "liat semua produk",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "tampilkn daftar harga",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "cek harga prmen",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "show harga barang",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "print daftar produk",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "info harga barang",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "info produk",
    "intent": "tampilkan_produk",
    "entities": {},
}, {
    "text": "Tambah barang/produk permen coklat",
    "intent": "tambah_produk",
    "entities": {},
}, {
    "text": "tambah produk permen coklat",
    "intent": "tambah_produk",
    "entities": {},
}, {
    "text": "tambah barang/produk",
    "intent": "tambah_produk",
    "entities": {},
}, {
    "text": "tambah produk",
    "intent": "tambah_produk",
    "entities": {},
}, {
    "text": "tambah barang permen coklat harga 13000",
    "intent": "tambah_produk",
    "entities": {},
}, {
    "text": "tambah barang brownis harga 2500 toples",
    "intent": "tambah_produk",
    "entities": {},
}, {
    "text": "tambah produk brownis 2500 per toples",
    "intent": "tambah_produk",
    "entities": {},
}, {
    "text": "tambah barang brownis harga 2500 bungkus",
    "intent": "tambah_produk",
    "entities": {},
}, {
    "text": "tambah produk roti pia bulus",
    "intent": "tambah_produk",
    "entities": {},
}, {
    "text": "input produk baru permen coklat harga 13000",
    "intent": "tambah_produk",
    "entities": {},
}, {
    "text": "input barang baru brownis 2500",
    "intent": "tambah_produk",
    "entities": {},
}, {
    "text": "tambah item permen coklat harga 13000",
    "intent": "tambah_produk",
    "entities": {},
}, {
    "text": "daftarkan produk permen coklat harga 13000",
    "intent": "tambah_produk",
    "entities": {},
}, {
    "text": "masukkan barang brownis harga 2500",
    "intent": "tambah_produk",
    "entities": {},
}, {
    "text": "tambh barang permen coklat",
    "intent": "tambah_produk",
    "entities": {},
}, {
    "text": "tambah barang premen coklat",
    "intent": "tambah_produk",
    "entities": {},
}, {
    "text": "tamabah produk permen coklat",
    "intent": "tambah_produk",
    "entities": {},
}, {
    "text": "tamabah barang brownis harga 2500",
    "intent": "tambah_produk",
    "entities": {},
}, {
    "text": "tambah brg brownis harga 2500",
    "intent": "tambah_produk",
    "entities": {},
}, {
    "text": "tambah barang bornwis harga 2500",
    "intent": "tambah_produk",
    "entities": {},
}, {
    "text": "tambah produk rmeni coklat harga 13000",
    "intent": "tambah_produk",
    "entities": {},
}, {
    "text": "tamabh barang roti pia",
    "intent": "tambah_produk",
    "entities": {},
}, {
    "text": "tambah barang/produk permen cokalat",
    "intent": "tambah_produk",
    "entities": {},
}, {
    "text": "add barang permen coklat harga 13000",
    "intent": "tambah_produk",
    "entities": {},
}, {
    "text": "buat produk baru permen coklat",
    "intent": "tambah_produk",
    "entities": {},
}, {
    "text": "create produk permen coklat 13000",
    "intent": "tambah_produk",
    "entities": {},
}, {
    "text": "register barang brownis 2500 toples",
    "intent": "tambah_produk",
    "entities": {},
}, {
    "text": "edit barang/produk",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "edit produk",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "Edit/update/ubah/hapus harga barang",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "Update/ubah/edti harga barang/produk",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "edti harga barang",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "ubah harga brownis jadi 2000",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "update harga brownis 2000",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "edit harga brownis 2000",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "ubah harga permen jadi 14000",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "update harga permen 14000",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "edit harga permen 14000",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "hapus/edit/ubah/ganti/update/perbaharui/tampilkan/tambah harga barang/produk",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "edit/ubah/ganti/update/perbaharui nama barang",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "ganti nama brownis jadi brownies premium",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "ubah nama permen jadi permen original",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "edti barang permen",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "ganti hraga brownis jadi 2000",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "ubah hrga permen jadi 14000",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "updaet harga barang",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "edti harga prmen",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "ubah harga brownis jd 2000",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "update hrga barang",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "edit produk brwnis",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "modify harga brownis 2000",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "change harga permen 14000",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "revisi harga brownis 2000",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "koreksi harga barang",
    "intent": "edit_produk",
    "entities": {},
}, {
    "text": "hapus barang",
    "intent": "hapus_produk",
    "entities": {},
}, {
    "text": "hapus produk",
    "intent": "hapus_produk",
    "entities": {},
}, {
    "text": "hapus barang permen",
    "intent": "hapus_produk",
    "entities": {},
}, {
    "text": "hapus produk brownis",
    "intent": "hapus_produk",
    "entities": {},
}, {
    "text": "hapus/edit/ubah/ganti/update/perbaharui/tampilkan/tambah nama barang/produk",
    "intent": "hapus_produk",
    "entities": {},
}, {
    "text": "buang produk permen",
    "intent": "hapus_produk",
    "entities": {},
}, {
    "text": "delete produk permen",
    "intent": "hapus_produk",
    "entities": {},
}, {
    "text": "remove barang brownis",
    "intent": "hapus_produk",
    "entities": {},
}, {
    "text": "hilangkan barang roti",
    "intent": "hapus_produk",
    "entities": {},
}, {
    "text": "hapus brang permen",
    "intent": "hapus_produk",
    "entities": {},
}, {
    "text": "hpus produk permen",
    "intent": "hapus_produk",
    "entities": {},
}, {
    "text": "hapus prdk permen",
    "intent": "hapus_produk",
    "entities": {},
}, {
    "text": "hapus barang brwnis",
    "intent": "hapus_produk",
    "entities": {},
}, {
    "text": "hapus produk browni",
    "intent": "hapus_produk",
    "entities": {},
}, {
    "text": "remove produk brownis",
    "intent": "hapus_produk",
    "entities": {},
}, {
    "text": "buang produk brownis",
    "intent": "hapus_produk",
    "entities": {},
}, {
    "text": "clear barang permen",
    "intent": "hapus_produk",
    "entities": {},
}, {
    "text": "total uang masuk hari ini",
    "intent": "total_uang_masuk",
    "entities": {},
}, {
    "text": "total uang tagihan hari ini",
    "intent": "total_tagihan",
    "entities": {},
}, {
    "text": "total uang tagihan kemarin",
    "intent": "total_tagihan",
    "entities": {},
}, {
    "text": "total uang tagihan tanggal 21",
    "intent": "total_tagihan",
    "entities": {},
}, {
    "text": "Cek/tampilkan/berapa pemasukan hari ini",
    "intent": "total_uang_masuk",
    "entities": {},
}, {
    "text": "pemasukan hari ini",
    "intent": "total_uang_masuk",
    "entities": {},
}, {
    "text": "total cicilan hari ini",
    "intent": "total_tagihan",
    "entities": {},
}, {
    "text": "berapa cicilan hari ini",
    "intent": "total_tagihan",
    "entities": {},
}, {
    "text": "berapa total transaks hari ini",
    "intent": "total_transaksi",
    "entities": {},
}, {
    "text": "total transakis hari ini",
    "intent": "total_transaksi",
    "entities": {},
}, {
    "text": "brp total transaksi hari ini",
    "intent": "total_transaksi",
    "entities": {},
}, {
    "text": "total uang masuk hari ni",
    "intent": "total_uang_masuk",
    "entities": {},
}, {
    "text": "brp uang masuk hari ini",
    "intent": "total_uang_masuk",
    "entities": {},
}, {
    "text": "total uang taagihan hari ini",
    "intent": "total_transaksi",
    "entities": {},
}, {
    "text": "total tunggakaan hari ini",
    "intent": "total_transaksi",
    "entities": {},
}, {
    "text": "berapa pemassukan hari ini",
    "intent": "total_transaksi",
    "entities": {},
}, {
    "text": "rekap transaksi hari ini",
    "intent": "total_transaksi",
    "entities": {},
}, {
    "text": "summary transaksi hari ini",
    "intent": "total_transaksi",
    "entities": {},
}, {
    "text": "omzet hari ini",
    "intent": "total_uang_masuk",
    "entities": {},
}, {
    "text": "siapa yang masih cicil",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "siapa yang punya hutang",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "siapa yang bayar dengan transfer",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "siapa yang bayar cash/tunai/langsung",
    "intent": "filter_bayar_cash",
    "entities": {},
}, {
    "text": "siapa bayar cash",
    "intent": "filter_bayar_cash",
    "entities": {},
}, {
    "text": "siapa bayar transfer",
    "intent": "filter_bayar_transfer",
    "entities": {},
}, {
    "text": "siapa yang msh nyicil",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "siapa yang masih nyicill",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "siapa yang masih ntang",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "siapa yg masih hutang",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "siapa paling banyak hutng",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "siapa yg byr cash",
    "intent": "filter_bayar_cash",
    "entities": {},
}, {
    "text": "siapa yang byr transfer",
    "intent": "filter_bayar_transfer",
    "entities": {},
}, {
    "text": "siapa yang blm lunas",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "siapa yang outstanding",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "siapa yang kredit",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "siapa yang debt",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "siapa yang nunggak",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "siapa yang punya tagihan",
    "intent": "filter_belum_lunas",
    "entities": {},
}, {
    "text": "siapa saja yang pesan hari ini",
    "intent": "pembeli_terbanyak",
    "entities": {},
}, {
    "text": "siapa yang paling banyak beli hari ini",
    "intent": "pembeli_terbanyak",
    "entities": {},
}, {
    "text": "siapa yang paling banyak transaksi hari ini",
    "intent": "pembeli_terbanyak",
    "entities": {},
}, {
    "text": "siapa yang paling banyak beli",
    "intent": "pembeli_terbanyak",
    "entities": {},
}, {
    "text": "Siapa pembeli terbanyak hari ini/kemarin/tanggal sekian",
    "intent": "pembeli_terbanyak",
    "entities": {},
}, {
    "text": "siapa pembeli terbanyak tanggal 21",
    "intent": "pembeli_terbanyak",
    "entities": {},
}, {
    "text": "siapa yang pesn hari ini",
    "intent": "pembeli_terbanyak",
    "entities": {},
}, {
    "text": "siapa saja yg order hari ini",
    "intent": "pembeli_terbanyak",
    "entities": {},
}, {
    "text": "siapa pemeli paling banyak hari ini",
    "intent": "pembeli_terbanyak",
    "entities": {},
}, {
    "text": "siapa pembeli trbanyak",
    "intent": "pembeli_terbanyak",
    "entities": {},
}, {
    "text": "siapa yang paling bnyak beli",
    "intent": "pembeli_terbanyak",
    "entities": {},
}, {
    "text": "siapa pmbeli terbanyak hari ini",
    "intent": "pembeli_terbanyak",
    "entities": {},
}, {
    "text": "pelanggan terbanyak hari ini",
    "intent": "pembeli_terbanyak",
    "entities": {},
}, {
    "text": "customer terbanyak hari ini",
    "intent": "pembeli_terbanyak",
    "entities": {},
}, {
    "text": "pembeli top hari ini",
    "intent": "pembeli_terbanyak",
    "entities": {},
}, {
    "text": "siapa yang belanja terbanyak",
    "intent": "pembeli_terbanyak",
    "entities": {},
}, {
    "text": "pagi",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "siang",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "sore",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "malam",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "assalamu'alaikum",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "wassalamu'alaikum",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "ada orang",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "helloo",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "haii",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "hie",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "slmat pagi",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "selamat apgi",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "helo bot",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "hai bott",
    "intent": "greeting",
    "entities": {},
}, {
    "text": "bantuan",
    "intent": "bantuan",
    "entities": {},
}, {
    "text": "help",
    "intent": "bantuan",
    "entities": {},
}, {
    "text": "tolong",
    "intent": "bantuan",
    "entities": {},
}, {
    "text": "cara pakai",
    "intent": "bantuan",
    "entities": {},
}, {
    "text": "cara menggunakan",
    "intent": "bantuan",
    "entities": {},
}, {
    "text": "perintah apa saja",
    "intent": "bantuan",
    "entities": {},
}, {
    "text": "apa saja yang bisa dilakukan",
    "intent": "bantuan",
    "entities": {},
}, {
    "text": "fitur apa saja",
    "intent": "bantuan",
    "entities": {},
}, {
    "text": "menu",
    "intent": "bantuan",
    "entities": {},
}, {
    "text": "panduan",
    "intent": "bantuan",
    "entities": {},
}, {
    "text": "tutorial",
    "intent": "bantuan",
    "entities": {},
}, {
    "text": "info",
    "intent": "bantuan",
    "entities": {},
}, {
    "text": "informasi",
    "intent": "bantuan",
    "entities": {},
}, {
    "text": "bantuaan",
    "intent": "bantuan",
    "entities": {},
}, {
    "text": "hlp",
    "intent": "bantuan",
    "entities": {},
}, {
    "text": "helpp",
    "intent": "bantuan",
    "entities": {},
}, {
    "text": "bantu dong",
    "intent": "bantuan",
    "entities": {},
}, {
    "text": "cara pake",
    "intent": "bantuan",
    "entities": {},
}, {
    "text": "cara nggunain",
    "intent": "bantuan",
    "entities": {},
}, {
    "text": "perintah apa aj",
    "intent": "bantuan",
    "entities": {},
}, {
    "text": "menu apa aj",
    "intent": "bantuan",
    "entities": {},
}, {
    "text": "Hari ini udin ambil permen 30 dus sudah lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "pelanggan": "Udin",
        "barang": "Permen",
        "jumlah": "30",
        "satuan": "dus",
        "status": "Lunas",
    },
}, {
    "text": "Hari ini andi order permen 600 toples dicicil 200000 tunai",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
        "pelanggan": "Andi",
        "barang": "Permen",
        "jumlah": "600",
        "satuan": "toples",
        "status": "Cicil",
        "nominal_bayar": "200000",
        "metode": "Tunai",
    },
}, {
    "text": "Hari ini budi order permen 30 toples dicicil 200000 dibayar langsung",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
        "pelanggan": "Budi",
        "barang": "Permen",
        "jumlah": "30",
        "satuan": "toples",
        "status": "Cicil",
        "nominal_bayar": "200000",
        "metode": "Tunai",
    },
}, {
    "text": "Hari ini naha ambil permen 50 dus sudah lunas dibayar secara transfer",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
        "pelanggan": "Naha",
        "barang": "Permen",
        "jumlah": "50",
        "satuan": "dus",
        "status": "Lunas",
        "metode": "Transfer",
    },
}, {
    "text": "Hari ini nala ambil brownis 100 bungkus dicicil 1000000 dibayar secara transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
        "pelanggan": "Nala",
        "barang": "Brownis",
        "jumlah": "100",
        "satuan": "bungkus",
        "status": "Cicil",
        "nominal_bayar": "1000000",
        "metode": "Transfer",
    },
}, {
    "text": "Hari ini nala ambil permen 70 dus dicicil 2000000 dibayar secara transfer",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
        "pelanggan": "Nala",
        "barang": "Permen",
        "jumlah": "70",
        "satuan": "dus",
        "status": "Cicil",
        "nominal_bayar": "2000000",
        "metode": "Transfer",
    },
}, {
    "text": "Hari ini nala ambil serbuk 100 lunas dibayar secara transfer",
    "intent": "tambah_transaksi_lunas_transfer",
    "entities": {
        "pelanggan": "Nala",
        "barang": "Serbuk",
        "jumlah": "100",
        "status": "Lunas",
        "metode": "Transfer",
    },
}, {
    "text": "Hari ini pak agus ambil permen coklat 2 dus",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "pelanggan": "Agus",
        "barang": "Permen Coklat",
        "jumlah": "2",
        "satuan": "dus",
    },
}, {
    "text": "Hari ini pak andi order barang 50 pcs berupa permen",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "pelanggan": "Andi",
        "barang": "Permen",
        "jumlah": "50",
        "satuan": "pcs",
    },
}, {
    "text": "Hari ini rara ambil permen coklat 13 dus dibayar lunas secara cash",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "pelanggan": "Rara",
        "barang": "Permen Coklat",
        "jumlah": "13",
        "satuan": "dus",
        "status": "Lunas",
        "metode": "Tunai",
    },
}, {
    "text": "Hari ini rudi order permen 600 toples dicicil 200000 bayar langsung",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
        "pelanggan": "Rudi",
        "barang": "Permen",
        "jumlah": "600",
        "satuan": "toples",
        "status": "Cicil",
        "nominal_bayar": "200000",
        "metode": "Tunai",
    },
}, {
    "text": "Hari ini rudi order permen 600 toples dicicil 200000 cash",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
        "pelanggan": "Rudi",
        "barang": "Permen",
        "jumlah": "600",
        "satuan": "toples",
        "status": "Cicil",
        "nominal_bayar": "200000",
        "metode": "Tunai",
    },
}, {
    "text": "Hari ini rudi order permen 600 toples dicicil 200000 sudah dibayar",
    "intent": "tambah_transaksi_cicilan_cash",
    "entities": {
        "pelanggan": "Rudi",
        "barang": "Permen",
        "jumlah": "600",
        "satuan": "toples",
        "status": "Cicil",
        "nominal_bayar": "200000",
    },
}, {
    "text": "Hari ini rudi order permen 600 toples dicicil 200000 tf",
    "intent": "tambah_transaksi_cicilan_transfer",
    "entities": {
        "pelanggan": "Rudi",
        "barang": "Permen",
        "jumlah": "600",
        "satuan": "toples",
        "status": "Cicil",
        "nominal_bayar": "200000",
        "metode": "Transfer",
    },
}, {
    "text": "Hari ini rudi order permen 600 toples sudah lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "pelanggan": "Rudi",
        "barang": "Permen",
        "jumlah": "600",
        "satuan": "toples",
        "status": "Lunas",
    },
}, {
    "text": "Hari ini supri ambil permen 20 toples sudah lunas",
    "intent": "tambah_transaksi_lunas_cash",
    "entities": {
        "pelanggan": "Supri",
        "barang": "Permen",
        "jumlah": "20",
        "satuan": "toples",
        "status": "Lunas",
    },
}, {
    "text": "cek hutang",
    "intent": "cek_hutang",
    "entities": {},
}, {
    "text": "cek hutang pelanggan",
    "intent": "cek_hutang",
    "entities": {},
}, {
    "text": "cek piutang",
    "intent": "cek_hutang",
    "entities": {},
}, {
    "text": "cek tagihan",
    "intent": "cek_tagihan",
    "entities": {},
}, {
    "text": "cek tagihan pelanggan",
    "intent": "cek_tagihan",
    "entities": {},
}, {
    "text": "cek semua penjualan",
    "intent": "cek_semua_penjualan",
    "entities": {},
}, {
    "text": "cek semua transaksi",
    "intent": "cek_semua_penjualan",
    "entities": {},
}, {
    "text": "lihat semua transaksi",
    "intent": "lihat_semua_transaksi",
    "entities": {},
}, {
    "text": "lihat semua penjualan",
    "intent": "lihat_semua_transaksi",
    "entities": {},
}, {
    "text": "tanggal 19-06-2026 budi ambil bembeng 40 ctn dicicil 200000 tunai",
    "intent": "tambah_transaksi_cicilan_tanggal_spesifik",
    "entities": {
        "pelanggan": "Budi",
        "barang": "Bembeng",
        "jumlah": "40",
        "satuan": "ctn",
        "status": "Cicil",
        "nominal_bayar": "200000",
        "metode": "Tunai",
        "waktu": "tanggal 19-06-2026",
    },
}, {
    "text": "tgl 21/04/2026 pak andi ambil permen 10 dus dicicil 50000 transfer",
    "intent": "tambah_transaksi_cicilan_tanggal_spesifik",
    "entities": {
        "pelanggan": "Andi",
        "barang": "Permen",
        "jumlah": "10",
        "satuan": "dus",
        "status": "Cicil",
        "nominal_bayar": "50000",
        "metode": "Transfer",
        "waktu": "21/04/2026",
    },
}, {
    "text": "21 april 2026 udin ambil meses 20 ctn dicicil 150000 cash",
    "intent": "tambah_transaksi_cicilan_tanggal_spesifik",
    "entities": {
        "pelanggan": "Udin",
        "barang": "Meses",
        "jumlah": "20",
        "satuan": "ctn",
        "status": "Cicil",
        "nominal_bayar": "150000",
        "metode": "Tunai",
        "waktu": "21 april 2026",
    },
}, {
    "text": "hari ini budi pesan bembeng 40 ctn; meses 20 ctn; willo 100 ctn lunas tunai",
    "intent": "tambah_transaksi_multi_item",
    "entities": {
        "pelanggan": "Budi",
        "status": "Lunas",
        "metode": "Tunai",
    },
}, {
    "text": "hari ini pak andi order bembeng 10 ctn; meses 5 ctn; willo 12 ctn sudah lunas cash",
    "intent": "tambah_transaksi_multi_item",
    "entities": {
        "pelanggan": "Andi",
        "status": "Lunas",
        "metode": "Tunai",
    },
}]

VALID_UNITS = frozenset([
    "dus",
    "karton",
    "pcs",
    "bks",
    "bungkus",
    "bal",
    "renceng",
    "box",
    "kg",
    "toples",
    "pack",
    "buah",
    "botol",
    "sachet",
    "loyang",
    "lusin",
    "pouch",
    "ctn",
    "paket",
])
