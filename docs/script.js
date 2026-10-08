// Global mouse tracking for background glow
document.addEventListener("mousemove", (e) => {
    // Set global custom properties on root
    document.documentElement.style.setProperty('--mouse-x', `${e.clientX}px`);
    document.documentElement.style.setProperty('--mouse-y', `${e.clientY}px`);
});

// Card hover glow effect
const cards = document.querySelectorAll(".card");

cards.forEach(card => {
    card.addEventListener("mousemove", (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        card.style.setProperty('--card-mouse-x', `${x}px`);
        card.style.setProperty('--card-mouse-y', `${y}px`);
    });
});

// Click Animation (Boxer / 📦)
document.addEventListener("mousedown", (e) => {
    const emojis = ["📦", "🥊", "🚀"];
    const emoji = emojis[Math.floor(Math.random() * emojis.length)];
    
    const pop = document.createElement("div");
    pop.className = "click-pop";
    pop.innerText = emoji;
    
    pop.style.left = `${e.clientX}px`;
    pop.style.top = `${e.clientY}px`;
    
    document.body.appendChild(pop);
    
    setTimeout(() => {
        pop.remove();
    }, 1000);
});

// OS Detection
window.addEventListener("DOMContentLoaded", () => {
    let osName = "Unknown";
    const userAgent = window.navigator.userAgent;
    
    if (userAgent.indexOf("Win") !== -1) osName = "Windows";
    else if (userAgent.indexOf("Mac") !== -1) osName = "macOS";
    else if (userAgent.indexOf("Linux") !== -1) osName = "Linux";
    
    const downloadBtn = document.getElementById("download-btn");
    if (downloadBtn && osName !== "Unknown") {
        downloadBtn.innerText = `Завантажити для ${osName}`;
    }
});
