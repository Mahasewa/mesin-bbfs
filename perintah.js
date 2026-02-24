// 1. DAFTAR TOMBOL (Tambah di sini kalau mau tombol baru)
const daftarFitur = [
    { id: "3d", nama: "PASANG 3D" },
    { id: "4d", nama: "PASANG 4D" }
    // Nanti tinggal tambah { id: "statistik", nama: "STATISTIK" } kalau mau
];

// 2. FUNGSI EKSEKUSI (Logika utama)
async function eksekusiPerintah(id, dataHijau, dataHistory) {
    let acak = [];
    let twin = [];
    
    // Penentuan Mode berdasarkan ID Tombol
    let mode = (id === "4d") ? 4 : 3;

    dataHijau.forEach(ekor => {
        let limit = (mode === 4) ? 99 : 9;
        for (let i = 0; i <= limit; i++) {
            let depan = (mode === 4) ? i.toString().padStart(2, '0') : i.toString();
            let gabung = depan + ekor;
            
            // Filter 1: Anti Quad/Triple
            let counts = {};
            for(let char of gabung) counts[char] = (counts[char] || 0) + 1;
            if (Math.max(...Object.values(counts)) >= 3) continue;

            // Filter 2: Seri Depan-Belakang
            if (ekor[0] === ekor[1] && depan.endsWith(ekor[0])) continue;

            // Filter 3: Riwayat
            if (dataHistory.some(h => h.endsWith(gabung))) continue;

            let unik = new Set(gabung).size;
            if (unik === mode) acak.push(gabung);
            else twin.push(gabung);
        }
    });

    return { acak, twin };
}

// 3. FUNGSI COPY
function salinTeks(id) {
    const teks = document.getElementById(id).innerText;
    navigator.clipboard.writeText(teks).then(() => {
        alert("Data berhasil dicopy, Koh!");
    });
}
