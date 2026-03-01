const GITHUB_BASE = "https://raw.githubusercontent.com/Mahasewa/masin-bbfs/main/";
let store = { hk: [], sdy: [], sgp: [] };

async function loadData() {
    try {
        const files = ['data_keluaran_hk.txt', 'data_keluaran_sdy.txt', 'data_keluaran_sgp.txt'];
        const results = await Promise.all(files.map(f => fetch(GITHUB_BASE + f + '?v=' + Date.now()).then(r => r.text())));

        store.hk = bersihkan(results[0]);
        store.sdy = bersihkan(results[1]);
        store.sgp = bersihkan(results[2]);

        tampilkan();
        
        document.getElementById('loader').classList.add('hidden');
        document.getElementById('app').classList.remove('hidden');
    } catch (e) {
        console.error(e);
        document.getElementById('loader').innerText = "Gagal memuat data.";
    }
}

function bersihkan(raw) {
    if(!raw) return [];
    // Memecah berdasarkan baris, tab, atau spasi ganda
    // Lalu ambil hanya yang isinya 4 digit angka
    const data = raw.split(/[\n\r\t\s]+/)
                    .map(v => v.trim())
                    .filter(v => /^\d{4}$/.test(v));
    return [...new Set(data)]; // Pastikan unik
}

function tampilkan() {
    // Update Statistik
    document.getElementById('stat-hk').innerText = store.hk.length + " Angka";
    document.getElementById('stat-sdy').innerText = store.sdy.length + " Angka";
    document.getElementById('stat-sgp').innerText = store.sgp.length + " Angka";

    // Isi Konten
    document.getElementById('txt-hk').innerText = store.hk.join('*');
    document.getElementById('txt-sdy').innerText = store.sdy.join('*');
    document.getElementById('txt-sgp').innerText = store.sgp.join('*');

    // Cari Duplikat
    const duplikat = store.hk.filter(v => store.sdy.includes(v) && store.sgp.includes(v));
    document.getElementById('total-duplikat').innerText = "Total: " + duplikat.length + " Angka";
    document.getElementById('txt-duplikat').innerText = duplikat.length > 0 ? duplikat.join('*') : "Tidak ada duplikat.";

    // Cari Perawan
    const all = new Set([...store.hk, ...store.sdy, ...store.sgp]);
    let perawan = [];
    for(let i=0; i<=9999; i++) {
        let n = i.toString().padStart(4, '0');
        if(!all.has(n)) perawan.push(n);
    }
    document.getElementById('total-perawan').innerText = "Total: " + perawan.length + " Angka";
    document.getElementById('txt-perawan').innerText = perawan.join('*');
}

function bukaDetail(id) {
    const el = document.getElementById('box-' + id);
    el.classList.toggle('hidden');
}

function copy(id) {
    const txt = document.getElementById(id).innerText;
    navigator.clipboard.writeText(txt).then(() => alert("Berhasil Salin!"));
}

// Jalankan otomatis
loadData();
