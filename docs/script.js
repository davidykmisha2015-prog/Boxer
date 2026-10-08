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
    
    // Position exactly at the mouse click
    pop.style.left = `${e.clientX}px`;
    pop.style.top = `${e.clientY}px`;
    
    document.body.appendChild(pop);
    
    // Remove element after animation
    setTimeout(() => {
        pop.remove();
    }, 1000);
});
