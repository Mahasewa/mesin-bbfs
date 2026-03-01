// CONFIG: Pastikan nama file di GitHub sama persis (Besar/Kecil Huruf)
const USER = "Mahasewa";
const REPO = "masin-bbfs";
const BRANCH = "main";
const BASE_URL = `https://raw.githubusercontent.com/${USER}/${REPO}/${BRANCH}/`;

let store = { hk: [], sdy: [], sgp: [] };

async function loadData() {
    const files = {
        hk: 'data_keluaran_hk.txt',
        sdy: 'data_keluaran_sdy.txt',
        sgp: 'data_keluaran_sgp.txt'
    };

    // Proses pengambilan data satu per satu agar tidak macet total jika ada 1 file error
    for (let key in files) {
        try {
            // Gunakan AllOrigins Proxy untuk menembus blokir browser (CORS)
            const proxyUrl = `https://api.allorigins.win/get?url=${encodeURIComponent(BASE_URL + files[key] + '?t=' + Date.now())}`;
            const res = await fetch(proxyUrl);
            const json = await res.json();
            
            if (json.contents) {
                store[key] = bersihkan(json.contents);
                console.log(`Berhasil muat ${key}: ${store[key].length} Angka`);
            }
        } catch (e) {
            console.warn(`Gagal otomatis menarik ${key}, silakan gunakan upload manual.`);
        }
    }

    tampilkan();
    document.getElementById('loader').classList.add('hidden');
    document.getElementById('app').classList.remove('hidden');
}

// FUNGSI PEMBERSIH: Mendukung format TAB (7 deret) atau 1 baris 1 data
function bersihkan(raw) {
    if(!raw) return [];
    const data = raw.split(/[\s\t\n\r]+/)
                    .map(v => v.trim().replace(/[^\d]/g, '')) // Hanya ambil digit
                    .filter(v => v.length === 4); // Harus tepat 4 digit
    return [...new Set(data)]; // Hapus angka ganda dalam satu pasaran
}

function tampilkan() {
    // Update Label Statistik
    document.getElementById('stat-hk').innerText = store.hk.length + " Angka Terdeteksi";
    document.getElementById('stat-sdy').innerText = store.sdy.length + " Angka Terdeteksi";
    document.getElementById('stat-sgp').innerText = store.sgp.length + " Angka Terdeteksi";

    // Update Isi Kotak Detail
    document.getElementById('txt-hk').innerText = store.hk.join('*') || 'Data Kosong / Belum Diupload';
    document.getElementById('txt-sdy').innerText = store.sdy.join('*') || 'Data Kosong / Belum Diupload';
    document.getElementById('txt-sgp').innerText = store.sgp.join('*') || 'Data Kosong / Belum Diupload';

    // ANALISA 1: Angka Duplikat (Irisan 3 Pasaran)
    const duplikat = store.hk.filter(v => store.sdy.includes(v) && store.sgp.includes(v));
    document.getElementById('total-duplikat').innerText = "Total: " + duplikat.length + " Angka Sama di 3 Data";
    document.getElementById('txt-duplikat').innerText = duplikat.length > 0 ? duplikat.join('*') : "Belum ada angka yang sama persis di ketiga data.";

    // ANALISA 2: Angka Perawan (0000-9999 yang belum pernah keluar sama sekali)
    const gabunganSemua = new Set([...store.hk, ...store.sdy, ...store.sgp]);
    let perawan = [];
    for(let i=0; i<=9999; i++) {
        let format4D = i.toString().padStart(4, '0');
        if(!gabunganSemua.has(format4D)) {
            perawan.push(format4D);
        }
    }
    document.getElementById('total-perawan').innerText = "Total: " + perawan.length + " Angka Belum Pernah Result";
    document.getElementById('txt-perawan').innerText = perawan.join('*');
}

// Fungsi Upload Manual (Ban Serep jika GitHub Down)
function handleFileUpload(event, pasaran) {
    const file = event.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = function(e) {
        store[pasaran] = bersihkan(e.target.result);
        tampilkan();
        alert(`Berhasil Memproses Data ${pasaran.toUpperCase()}!`);
    };
    reader.readAsText(file);
}

function bukaDetail(id) {
    const el = document.getElementById('box-' + id);
    if(el) el.classList.toggle('hidden');
}

function copy(id) {
    const txt = document.getElementById(id).innerText;
    if(!txt || txt.includes('Belum ada') || txt.includes('Kosong')) return;
    navigator.clipboard.writeText(txt).then(() => alert("Berhasil Salin, Koh!"));
}

loadData();
