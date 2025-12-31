//javascript for schedule page
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
    },{
        date: '2025-01-18T19:00:00+07:00',
        title: 'Premier Match',
        map: 'Haven',
    },{
        date: '2025-01-25T19:00:00+07:00',
        title: 'Premier Match',
        map: 'Pearl',
    },{
        date: '2025-02-01T19:00:00+07:00',
        title: 'Premier Match',
        map: 'Split',
    },{
        date: '2025-02-08T19:00:00+07:00',
        title: 'Premier Match',
        map: 'Abyss',
    },{
        date: '2025-02-15T19:00:00+07:00',
        title: 'Premier Match',
        map: 'Lotus',
    },
];

function displaySchedule() {
    const matchInfoElement = document.getElementById('match-info');

    matchSchedule.forEach((match) => {
        const matchDate = new Date(match.date);
        const formattedDate = matchDate.toLocaleString('en-US', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            hour12: true,
            timeZoneName: 'short',
        });

        const matchCard = document.createElement('div');
        matchCard.classList.add('match-card');

        matchCard.innerHTML = `
            <h2>${match.title}</h2>
            <p>Date: ${formattedDate}</p>
            <p>Map: ${match.map}</p>
        `;

        matchInfoElement.appendChild(matchCard);
    });
}

// Initialize the schedule display
displaySchedule();