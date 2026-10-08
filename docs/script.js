// Global mouse tracking for background glow
document.addEventListener("mousemove", (e) => {
    // Set global custom properties on root
    document.documentElement.style.setProperty('--mouse-x', `${e.clientX}px`);
    document.documentElement.style.setProperty('--mouse-y', `${e.clientY}px`);
});

// Card hover glow effect (Antigravity-like)
const cards = document.querySelectorAll(".card");

cards.forEach(card => {
    card.addEventListener("mousemove", (e) => {
        const rect = card.getBoundingClientRect();
        // Calculate mouse position relative to the card
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        // Update the custom properties for this specific card
        card.style.setProperty('--card-mouse-x', `${x}px`);
        card.style.setProperty('--card-mouse-y', `${y}px`);
    });
});
