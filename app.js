// app.js
document.getElementById("userForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const userInput = document.getElementById("userInput").value;
    const responseContainer = document.getElementById("responseContainer");

    try {
        const response = await fetch("/process", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ input: userInput }),
        });

        const data = await response.json();
        responseContainer.textContent = data.response || "Something went wrong.";
    } catch (error) {
        console.error("Error:", error);
        responseContainer.textContent = "Error connecting to the AI. Please try again.";
    }
});

// Additional quotes display (in app.js)
const quotes = [
    "Believe you can and you're halfway there.",
    "You are stronger than you think.",
    "This too shall pass."
];

document.addEventListener("DOMContentLoaded", () => {
    const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
    document.getElementById("responseContainer").textContent = randomQuote;
});

