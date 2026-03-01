// JURUS PAMUNGKAS: Menggunakan CDN agar data tidak diblokir browser
const USER = "Mahasewa";
const REPO = "masin-bbfs";
const BRANCH = "main";

// Jalur alternatif jika jalur utama macet
const BASE_URL = `https://cdn.jsdelivr.net/gh/${USER}/${REPO}@${BRANCH}/`;

let store = { hk: [], sdy: [], sgp: [] };

async function loadData() {
    try {
        console.log("Memulai penarikan data...");
        
        const files = ['data_keluaran_hk.txt', 'data_keluaran_sdy.txt', 'data_keluaran_sgp.txt'];
        
        // Ambil data satu per satu agar lebih stabil
        const results = await Promise.all(files.map(async (f) => {
            // Kita tambah timestamp agar data selalu yang terbaru (bukan cache lama)
            const response = await fetch(BASE_URL + f + '?t=' + Date.now());
            if (!response.ok) throw new Error("Gagal ambil file: " + f);
            return await response.text();
        }));

        store.hk = bersihkan(results[0]);
        store.sdy = bersihkan(results[1]);
        store.sgp = bersihkan(results[2]);

        console.log("Data Berhasil: ", {hk: store.hk.length, sdy: store.sdy.length, sgp: store.sgp.length});

        tampilkan();
        
        document.getElementById('loader').classList.add('hidden');
        document.getElementById('app').classList.remove('hidden');
    } catch (e) {
        console.error("Detail Error: ", e);
        document.getElementById('loader').innerHTML = `<p class="text-red-500 font-bold">ERROR: ${e.message}</p>`;
    }
}

function bersihkan(raw) {
    if(!raw) return [];
    // Logika pembersih: memecah tab, spasi, enter dan hanya ambil 4 digit angka
    const data = raw.replace(/[^\d\s\t\n\r]/g, ' ') 
                    .split(/[\s\t\n\r]+/)
                    .map(v => v.trim())
                    .filter(v => v.length === 4 && /^\d+$/.test(v));
    return [...new Set(data)]; 
}

function tampilkan() {
    // Update Statistik di Layar
    document.getElementById('stat-hk').innerText = store.hk.length + " Angka";
    document.getElementById('stat-sdy').innerText = store.sdy.length + " Angka";
    document.getElementById('stat-sgp').innerText = store.sgp.length + " Angka";

    // Isi Data ke dalam Box Detail (format rapat pakai bintang)
    document.getElementById('txt-hk').innerText = store.hk.join('*') || 'Kosong';
    document.getElementById('txt-sdy').innerText = store.sdy.join('*') || 'Kosong';
    document.getElementById('txt-sgp').innerText = store.sgp.join('*') || 'Kosong';

    // Logika Duplikat (Irisan 3 pasaran)
    const duplikat = store.hk.filter(v => store.sdy.includes(v) && store.sgp.includes(v));
    document.getElementById('total-duplikat').innerText = "Total: " + duplikat.length + " Angka";
    document.getElementById('txt-duplikat').innerText = duplikat.length > 0 ? duplikat.join('*') : "Tidak ada duplikat.";

    // Logika Perawan (Cari yang belum ada di sejarah manapun)
    const allHistory = new Set([...store.hk, ...store.sdy, ...store.sgp]);
    let perawan = [];
    for(let i=0; i<=9999; i++) {
        let n = i.toString().padStart(4, '0');
        if(!allHistory.has(n)) perawan.push(n);
    }
    document.getElementById('total-perawan').innerText = "Total: " + perawan.length + " Angka";
    document.getElementById('txt-perawan').innerText = perawan.join('*');
}

function bukaDetail(id) {
    const el = document.getElementById('box-' + id);
    if(el) el.classList.toggle('hidden');
}

function copy(id) {
    const txt = document.getElementById(id).innerText;
    if(!txt || txt === 'Kosong') return;
    navigator.clipboard.writeText(txt).then(() => alert("Berhasil Salin!"));
}

// Jalankan aplikasi
loadData();
