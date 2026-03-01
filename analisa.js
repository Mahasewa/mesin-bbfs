const USER = "Mahasewa";
const REPO = "masin-bbfs";
const BRANCH = "main";
const BASE_URL = `https://cdn.jsdelivr.net/gh/${USER}/${REPO}@${BRANCH}/`;

let store = { hk: [], sdy: [], sgp: [] };

async function loadData() {
    const files = {
        hk: 'data_keluaran_hk.txt',
        sdy: 'data_keluaran_sdy.txt',
        sgp: 'data_keluaran_sgp.txt'
    };

    // Kita coba satu-satu, kalau satu gagal, yang lain tetap jalan
    for (let key in files) {
        try {
            const res = await fetch(BASE_URL + files[key] + '?t=' + Date.now());
            if (res.ok) {
                const text = await res.text();
                store[key] = bersihkan(text);
                console.log(`Berhasil muat ${key}: ${store[key].length}`);
            } else {
                console.warn(`File ${files[key]} tidak ditemukan di GitHub.`);
            }
        } catch (e) {
            console.error(`Error fetch ${key}:`, e);
        }
    }

    tampilkan();
    document.getElementById('loader').classList.add('hidden');
    document.getElementById('app').classList.remove('hidden');
}

// FUNGSI BARU: Untuk Upload Manual jika GitHub Error
function handleFileUpload(event, pasaran) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        const text = e.target.result;
        store[pasaran] = bersihkan(text);
        tampilkan();
        alert(`Berhasil upload data ${pasaran.toUpperCase()}!`);
    };
    reader.readAsText(file);
}

function bersihkan(raw) {
    if(!raw) return [];
    // Logika sakti: ambil semua angka 4 digit dari baris/tab manapun
    const data = raw.split(/[\s\t\n\r]+/)
                    .map(v => v.trim().replace(/[^\d]/g, '')) // Hanya ambil angka
                    .filter(v => v.length === 4);
    return [...new Set(data)]; 
}

function tampilkan() {
    document.getElementById('stat-hk').innerText = store.hk.length + " Angka";
    document.getElementById('stat-sdy').innerText = store.sdy.length + " Angka";
    document.getElementById('stat-sgp').innerText = store.sgp.length + " Angka";

    document.getElementById('txt-hk').innerText = store.hk.join('*') || 'Belum ada data (Klik upload di bawah)';
    document.getElementById('txt-sdy').innerText = store.sdy.join('*') || 'Belum ada data (Klik upload di bawah)';
    document.getElementById('txt-sgp').innerText = store.sgp.join('*') || 'Belum ada data (Klik upload di bawah)';

    const duplikat = store.hk.filter(v => store.sdy.includes(v) && store.sgp.includes(v));
    document.getElementById('total-duplikat').innerText = "Total: " + duplikat.length + " Angka";
    document.getElementById('txt-duplikat').innerText = duplikat.length > 0 ? duplikat.join('*') : "Tidak ada duplikat.";

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
    if(!txt || txt.includes('Belum ada')) return;
    navigator.clipboard.writeText(txt).then(() => alert("Berhasil Salin!"));
}

loadData();
