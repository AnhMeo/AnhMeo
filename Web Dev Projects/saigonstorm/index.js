const matchSchedule = [
    {
        date: '2024-12-15T19:00:00+07:00',
        title: 'Premier Playoffs',
        map: 'To be determined',
    },
    {
        date: '2025-01-11T19:00:00+07:00',
        title: 'Premier Match',
        map: 'Fracture',
    },
    {
        date: '2025-01-18T19:00:00+07:00',
        title: 'Premier Match',
        map: 'Haven',
    },
    {
        date: '2025-01-25T19:00:00+07:00',
        title: 'Premier Match',
        map: 'Pearl',
    },
    {
        date: '2025-02-01T19:00:00+07:00',
        title: 'Premier Match',
        map: 'Split',
    },
    {
        date: '2025-02-08T19:00:00+07:00',
        title: 'Premier Match',
        map: 'Abyss',
    },
    {
        date: '2025-02-15T19:00:00+07:00',
        title: 'Premier Match',
        map: 'Lotus',
    },
];

// **Countdown Timer Logic**
document.addEventListener('DOMContentLoaded', function () {
    const countdownTimer = document.getElementById('countdown-timer');
    if (countdownTimer) {
        setInterval(() => {
            const nextMatch = matchSchedule.find(match => new Date(match.date) > new Date());
            if (!nextMatch) {
                countdownTimer.innerText = 'No upcoming matches.';
                return;
            }

            const timeRemaining = getTimeRemaining(nextMatch.date);
            if (!timeRemaining) {
                countdownTimer.innerText = 'Live now!';
                return;
            }

            const { days, hours, minutes, seconds } = timeRemaining;
            countdownTimer.innerHTML = `
                <p>Next Match: ${nextMatch.title} on ${nextMatch.map}</p>
                <p>${days}:${hours}:${minutes}:${seconds}</p>
            `;
        }, 1000);
    }

    // **Tab Button Logic**
    document.querySelectorAll('.tab-button').forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons and tab content
            document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));

            // Add active class to the clicked button and corresponding tab content
            button.classList.add('active');
            const tabContent = document.getElementById(button.dataset.tab);
            tabContent.classList.add('active');
        });
    });

    // Set default active tab on page load
    const activeTabButton = document.querySelector('.tab-button.active');
    if (activeTabButton) {
        activeTabButton.click();
    }

    // **Match Archive Filtering Logic**
    const matchFilter = document.getElementById("match-filter");
    const matches = document.querySelectorAll(".match");
    const matchesList = document.getElementById("matches-list");

    if (matchFilter && matchesList) {
        const noMatchesMessage = document.createElement("p");
        noMatchesMessage.id = "no-matches-message";
        noMatchesMessage.style.display = "none";
        noMatchesMessage.textContent = "No matches found for this filter.";
        matchesList.appendChild(noMatchesMessage);

        matchFilter.addEventListener("change", () => {
            const selectedResult = matchFilter.value;
            let visibleMatches = 0;

            matches.forEach(match => {
                if (selectedResult === "all" || match.dataset.result === selectedResult) {
                    match.style.display = "block";
                    visibleMatches++;
                } else {
                    match.style.display = "none";
                }
            });

            noMatchesMessage.style.display = (visibleMatches === 0) ? "block" : "none";
        });
    }

    // **Highlight Archive Filtering Logic**
    const filter = document.getElementById("player-filter");
    const highlights = document.querySelectorAll(".highlight");
    const highlightsList = document.getElementById("highlights-list");

    if (filter && highlightsList) {
        const noClipsMessage = document.createElement("p");
        noClipsMessage.id = "no-clips-message";
        noClipsMessage.style.display = "none";
        noClipsMessage.textContent = ""; // This will be updated dynamically.
        highlightsList.appendChild(noClipsMessage);

        filter.addEventListener("change", () => {
            const selectedPlayer = filter.value;
            let visibleHighlights = 0;

            highlights.forEach(highlight => {
                if (selectedPlayer === "all" || highlight.dataset.player === selectedPlayer) {
                    highlight.style.display = "block";
                    visibleHighlights++;
                } else {
                    highlight.style.display = "none";
                }
            });

            noClipsMessage.textContent = visibleHighlights === 0 
                ? `No clips have been uploaded for ${selectedPlayer === "all" ? "any player" : selectedPlayer} yet. Check back again soon!`
                : '';
            noClipsMessage.style.display = visibleHighlights === 0 ? "block" : "none";
        });
    }

 // **Contact Form Handling**
const contactForm = document.getElementById('contactForm');
const confirmation = document.getElementById('confirmation');

if (contactForm && confirmation) {
    contactForm.addEventListener('submit', function (e) {
        e.preventDefault();
        
        const message = document.getElementById('message').value.trim();
        
        if (message === "") {
            alert("Please enter a message.");
            return;
        }

        // Show confirmation message
        confirmation.style.display = "block";
        contactForm.reset();
        setTimeout(() => {
            confirmation.style.display = "none";
        }, 3000);

        // Prepare the message to send to Discord
        const discordMessage = {
            content: `New contact form submission:\nMessage: ${message}`
        };

        // Discord webhook URL
        const webhookURL = 'https://discord.com/api/webhooks/1317187802131071116/MgNnYDFLz7YpXp1iTfMLQgMtkBf_B79skRpvekl1IwH_-NIUD5DcnluGxnM0UmUGtXBL';

        // Send form data to Discord using webhook
        fetch(webhookURL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(discordMessage),
        })
        .then(response => {
            if (response.ok) {
                console.log('Message sent to Discord');
            } else {
                console.error('Error sending message to Discord');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
}


// Helper function to calculate the time remaining until the match
function getTimeRemaining(matchDate) {
    const now = new Date(); // Current local time
    const matchTime = new Date(matchDate); // Parse match date correctly
    const timeDiff = matchTime - now; // Time difference in milliseconds

    if (timeDiff <= 0) {
        return null; // Match already happening or passed
    }

    // Convert milliseconds to days, hours, minutes, seconds
    const days = Math.floor(timeDiff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((timeDiff / (1000 * 60 * 60)) % 24);
    const minutes = Math.floor((timeDiff / (1000 * 60)) % 60);
    const seconds = Math.floor((timeDiff / 1000) % 60);

    // Pad with leading zeroes for consistent formatting
    return {
        days: String(days).padStart(2, '0'),
        hours: String(hours).padStart(2, '0'),
        minutes: String(minutes).padStart(2, '0'),
        seconds: String(seconds).padStart(2, '0')
    };
}})
