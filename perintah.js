// perintah.js - Otak Mesin Mahasewa
async function prosesGenerate(mode, dataHijau, dataHistory) {
    let acak = [];
    let twin = [];

    dataHijau.forEach(ekor => {
        let limit = (mode === 4) ? 99 : 9;
        for (let i = 0; i <= limit; i++) {
            let depan = (mode === 4) ? i.toString().padStart(2, '0') : i.toString();
            let gabung = depan + ekor;
            
            let counts = {};
            for(let char of gabung) counts[char] = (counts[char] || 0) + 1;
            if (Math.max(...Object.values(counts)) >= 3) continue;

            if (ekor[0] === ekor[1] && depan.endsWith(ekor[0])) continue;
            if (dataHistory.some(h => h.endsWith(gabung))) continue;

            let unik = new Set(gabung).size;
            if (unik === mode) acak.push(gabung);
            else twin.push(gabung);
        }
    });
    return { acak, twin };
}

function salinTeks(id) {
    const teks = document.getElementById(id).innerText;
    navigator.clipboard.writeText(teks).then(() => {
        alert("Teks berhasil disalin, Koh!");
    });
}
