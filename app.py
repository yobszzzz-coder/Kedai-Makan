from flask import Flask, render_template_string, request

app = Flask(__name__)

# DAFTAR MENU DAN HARGA
menu_makanan = {
    "1. Nasi Goreng": 15000,
    "2. Tinutuan": 15000,
    "3. Gorengan": 2000
}
menu_minuman = {
    "4. Kopi": 5000,
    "5. Es Teh": 5000,
    "6. Nutrisari": 5000
}

@app.route('/')
def beranda():
    return render_template_string('''
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Kasir Kedai Makan</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; font-family:Arial, sans-serif; user-select:none; }
        body { background:#f8f9fa; padding:20px; line-height:1.6; }
        .wadah { max-width:500px; margin:0 auto; background:white; border-radius:12px; box-shadow:0 2px 10px #0000001a; padding:20px; }
        h1 { text-align:center; color:#2d3436; margin-bottom:20px; font-size:20px; }
        h2 { color:#2d3436; margin:15px 0 10px; font-size:17px; }
        .menu-item { padding:6px 0; border-bottom:1px solid #eee; }
        .total { background:#e3f2fd; padding:12px; border-radius:8px; margin:15px 0; font-weight:bold; font-size:16px; }
        .bayar { background:#e8f5e9; padding:12px; border-radius:8px; margin:10px 0; }
        .ucapan { text-align:center; margin-top:20px; padding-top:15px; border-top:1px solid #eee; color:#2e7d32; font-weight:bold; }
        label { display:block; margin:8px 0 3px; font-size:14px; }
        input, select, button { width:100%; padding:10px; border-radius:6px; border:1px solid #ddd; font-size:15px; margin-bottom:10px; }
        button { background:#2e7d32; color:white; border:none; cursor:pointer; font-weight:bold; }
        button:hover { background:#256a29; }
    </style>
</head>
<body>
    <div class="wadah">
        <h1>📝 KASIR KEDEI MAKAN</h1>

        <h2>🍜 MAKANAN</h2>
        {% for nama, harga in menu_makanan.items() %}
        <div class="menu-item">{{ nama }} - Rp {{ harga }}</div>
        {% endfor %}

        <h2>🥤 MINUMAN</h2>
        {% for nama, harga in menu_minuman.items() %}
        <div class="menu-item">{{ nama }} - Rp {{ harga }}</div>
        {% endfor %}

        <form action="/proses" method="post">
            <label>Pilih Nomor Menu (pisah koma, contoh: 1,3,5):</label>
            <input type="text" name="menu" placeholder="1, 3, 5" required>

            <label>Jumlah masing-masing:</label>
            <input type="text" name="jumlah" placeholder="2, 1, 3" required>

            <button type="submit">Hitung Total</button>
        </form>
    </div>
</body>
</html>
''', menu_makanan=menu_makanan, menu_minuman=menu_minuman)

@app.route('/proses', methods=['POST'])
def proses():
    try:
        nomor_menu = request.form['menu'].replace(' ', '').split(',')
        jumlah_list = request.form['jumlah'].replace(' ', '').split(',')

        if len(nomor_menu) != len(jumlah_list):
            return "⚠️ Jumlah menu dan jumlah barang HARUS SAMA!"

        gabungan = {**menu_makanan, **menu_minuman}
        daftar_nama = list(gabungan.keys())
        daftar_harga = list(gabungan.values())

        pesanan = []
        total = 0

        for i in range(len(nomor_menu)):
            idx = int(nomor_menu[i])-1
            jml = int(jumlah_list[i])
            nama = daftar_nama[idx]
            hrg = daftar_harga[idx]
            subtotal = hrg * jml
            pesanan.append(f"{nama} x{jml} = Rp {subtotal:,}")
            total += subtotal

        return render_template_string('''
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Struk Pembelian</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; font-family:Arial, sans-serif; user-select:none; }
        body { background:#f8f9fa; padding:20px; line-height:1.6; }
        .wadah { max-width:500px; margin:0 auto; background:white; border-radius:12px; box-shadow:0 2px 10px #0000001a; padding:20px; }
        h1 { text-align:center; color:#2d3436; margin-bottom:20px; font-size:20px; }
        .pesanan { padding:8px 0; border-bottom:1px solid #eee; }
        .total { background:#e3f2fd; padding:12px; border-radius:8px; margin:15px 0; font-weight:bold; font-size:16px; text-align:center; }
        .bayar { background:#e8f5e9; padding:12px; border-radius:8px; margin:10px 0; }
        .ucapan { text-align:center; margin-top:20px; padding-top:15px; border-top:1px solid #eee; color:#2e7d32; font-weight:bold; }
        a { display:inline-block; margin-top:15px; padding:10px 20px; background:#2e7d32; color:white; border-radius:6px; text-decoration:none; }
    </style>
</head>
<body>
    <div class="wadah">
        <h1>🧾 STRUK PEMBELIAN</h1>
        {% for p in pesanan %}
        <div class="pesanan">{{ p }}</div>
        {% endfor %}

        <div class="total">TOTAL: Rp {{ total:, }}</div>

        <div class="bayar">
            <h3>💳 CARA BAYAR</h3>
            <p>1. DANA: <b>081314347426</b></p>
            <p>2. GO-PAY: <b>081314347426</b></p>
            <p>3. Bayar Langsung di Kasir</p>
        </div>

        <div class="ucapan">
            🙏 TERIMA KASIH SUDAH BERKUNJUNG 🙏<br>
            Semoga Makanannya Enak & Puas!
        </div>

        <a href="/">🔙 Pesan Lagi</a>
    </div>
</body>
</html>
''', pesanan=pesanan, total=total)

    except Exception as e:
        return f"⚠️ Salah input: {str(e)}"

# 🔴🔴🔴 WAJIB ADA BARIS INI! TANPA INI PASTI 404 🔴🔴🔴
app=app

if __name__ == "__main__":
    app.run()
      
