from database import db_client

class SupabaseWorksheet:
    def __init__(self, table_name, headers):
        self.table_name = table_name
        self.headers = headers
        self.row_mapping = {} # row_idx (1-based) -> supabase_id

    def _get_supabase(self):
        return db_client.get_supabase()

    def get_all_values(self):
        response = self._get_supabase().table(self.table_name).select("*").order("id").execute()
        data = response.data
        
        result = [self.headers]
        self.row_mapping = {}
        
        for idx, row in enumerate(data):
            row_num = idx + 2 # row 1 is header
            self.row_mapping[row_num] = row["id"]
            
            # Map based on table
            if self.table_name == "transaksi":
                # A=Tanggal | B=Nama | C=Barang | D=Jumlah | E=Harga Satuan | F=Total Harga | G=Status | H=Metode Bayar | I=Jumlah Tagihan | J=Jumlah Uang Masuk
                result.append([
                    row.get("tanggal", ""),
                    row.get("nama_pelanggan", ""),
                    row.get("barang", ""),
                    str(row.get("jumlah_satuan", "")),
                    str(row.get("harga", 0)),
                    str(row.get("total", 0)),
                    row.get("status", ""),
                    row.get("metode_pembayaran", ""),
                    str(row.get("tagihan", 0)),
                    str(row.get("uang_masuk", 0))
                ])
            elif self.table_name == "master_barang":
                result.append([
                    str(row.get("id")),
                    row.get("nama_barang", ""),
                    str(row.get("harga", 0)),
                    row.get("satuan", "")
                ])
            elif self.table_name == "master_metode":
                result.append([
                    str(row.get("id")),
                    row.get("nama_metode", ""),
                    row.get("kata_kunci", "")
                ])
            elif self.table_name == "histori_pelunasan":
                result.append([
                    row.get("tanggal_bayar", ""),
                    "", # Nama Pelanggan (not stored directly in histori table)
                    str(row.get("nominal_bayar", 0)),
                    str(row.get("sisa_tagihan", 0)),
                    row.get("metode_pembayaran", "")
                ])
                
        return result

    def append_row(self, values, value_input_option="USER_ENTERED"):
        data = {}
        if self.table_name == "transaksi":
            data = {
                "tanggal": values[0] if len(values) > 0 else "",
                "nama_pelanggan": values[1] if len(values) > 1 else "",
                "barang": values[2] if len(values) > 2 else "",
                "jumlah_satuan": values[3] if len(values) > 3 else "",
                "harga": self._clean_num(values[4]) if len(values) > 4 else 0,
                "total": self._clean_num(values[5]) if len(values) > 5 else 0,
                "status": values[6] if len(values) > 6 else "",
                "metode_pembayaran": values[7] if len(values) > 7 else "",
                "tagihan": self._clean_num(values[8]) if len(values) > 8 else 0,
                "uang_masuk": self._clean_num(values[9]) if len(values) > 9 else 0
            }
        elif self.table_name == "master_barang":
            data = {
                "nama_barang": values[1] if len(values) > 1 else "",
                "harga": self._clean_num(values[2]) if len(values) > 2 else 0,
                "satuan": values[3] if len(values) > 3 else "pcs"
            }
        elif self.table_name == "master_metode":
            data = {
                "nama_metode": values[1] if len(values) > 1 else "",
                "kata_kunci": values[2] if len(values) > 2 else ""
            }
        elif self.table_name == "histori_pelunasan":
            data = {
                "tanggal_bayar": values[0] if len(values) > 0 else "",
                "nominal_bayar": self._clean_num(values[2]) if len(values) > 2 else 0,
                "sisa_tagihan": self._clean_num(values[3]) if len(values) > 3 else 0,
                "metode_pembayaran": values[4] if len(values) > 4 else ""
            }
            
        res = self._get_supabase().table(self.table_name).insert(data).execute()
        # Return a dict to mock gspread response and avoid attribute errors in main.py
        return {"updates": {"updatedRange": None}}

    def append_rows(self, rows_to_append, value_input_option="USER_ENTERED"):
        for row in rows_to_append:
            self.append_row(row)
        return {"updates": {"updatedRows": len(rows_to_append)}}

    def update_cell(self, row, col, value):
        if row not in self.row_mapping:
            self.get_all_values() # Refresh mapping
            if row not in self.row_mapping:
                return # Row not found
                
        supabase_id = self.row_mapping[row]
        data = {}
        
        if self.table_name == "transaksi":
            cols = ["tanggal", "nama_pelanggan", "barang", "jumlah_satuan", "harga", "total", "status", "metode_pembayaran", "tagihan", "uang_masuk"]
            if 1 <= col <= len(cols):
                col_name = cols[col - 1]
                if col_name in ["harga", "total", "tagihan", "uang_masuk"]:
                    data[col_name] = self._clean_num(value)
                else:
                    data[col_name] = str(value)
        
        if data:
            self._get_supabase().table(self.table_name).update(data).eq("id", supabase_id).execute()

    def update_cells(self, cell_list, value_input_option="USER_ENTERED"):
        if not cell_list: return
        
        # Group cells by row
        row_data = {} # row -> {col: value}
        for cell in cell_list:
            if cell.row not in row_data: row_data[cell.row] = {}
            row_data[cell.row][cell.col] = cell.value
            
        for row, cols in row_data.items():
            if row not in self.row_mapping:
                self.get_all_values()
                if row not in self.row_mapping: continue
            
            supabase_id = self.row_mapping[row]
            data = {}
            if self.table_name == "transaksi":
                col_names = ["tanggal", "nama_pelanggan", "barang", "jumlah_satuan", "harga", "total", "status", "metode_pembayaran", "tagihan", "uang_masuk"]
                for col_idx, value in cols.items():
                    if 1 <= col_idx <= len(col_names):
                        col_name = col_names[col_idx - 1]
                        if col_name in ["harga", "total", "tagihan", "uang_masuk"]:
                            data[col_name] = self._clean_num(value)
                        else:
                            data[col_name] = str(value)
            
            if data:
                self._get_supabase().table(self.table_name).update(data).eq("id", supabase_id).execute()

    def delete_rows(self, row_idx):
        if row_idx not in self.row_mapping:
            self.get_all_values()
            if row_idx not in self.row_mapping:
                return
        supabase_id = self.row_mapping[row_idx]
        self._get_supabase().table(self.table_name).delete().eq("id", supabase_id).execute()

    def delete_row(self, row_idx):
        self.delete_rows(row_idx)

    def row_values(self, row_idx):
        # Fetch directly or use mapped cache
        self.get_all_values()
        if row_idx not in self.row_mapping:
            return []
        supabase_id = self.row_mapping[row_idx]
        res = self._get_supabase().table(self.table_name).select("*").eq("id", supabase_id).execute()
        if res.data:
            row = res.data[0]
            if self.table_name == "transaksi":
                return [
                    row.get("tanggal", ""), row.get("nama_pelanggan", ""), row.get("barang", ""),
                    str(row.get("jumlah_satuan", "")), str(row.get("harga", 0)), str(row.get("total", 0)),
                    row.get("status", ""), row.get("metode_pembayaran", ""), str(row.get("tagihan", 0)),
                    str(row.get("uang_masuk", 0))
                ]
        return []

    def format(self, *args, **kwargs):
        pass # Ignore formatting commands

    def range(self, range_name):
        # Dummy cell object
        class Cell:
            def __init__(self, row, col, value=""):
                self.row = row
                self.col = col
                self.value = value
        
        # very basic parser for A2:J2
        import re
        match = re.search(r'([A-Z])(\d+):([A-Z])(\d+)', range_name)
        if match:
            r = int(match.group(2))
            cells = []
            for c in range(1, 11):
                cells.append(Cell(r, c))
            return cells
        return []

    def _clean_num(self, val):
        try:
            if isinstance(val, (int, float)): return val
            bersih = str(val).replace("Rp", "").replace(".", "").replace(",", "").strip()
            return int(bersih) if bersih else 0
        except Exception:
            return 0
