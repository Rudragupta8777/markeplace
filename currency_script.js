// Initialize Firebase
const firebaseConfig = {
    apiKey: "AIzaSyDB53CAuNzeJ4LgQhiNPijUbBhkfojDfHo",
    authDomain: "marketplace-bd8d7.firebaseapp.com",
    databaseURL: "https://marketplace-bd8d7-default-rtdb.firebaseio.com",
    projectId: "marketplace-bd8d7",
    storageBucket: "marketplace-bd8d7.appspot.com",
    messagingSenderId: "912974729910",
    appId: "1:912974729910:web:27103231de7900886e4c17",
    measurementId: "G-0NVEVL3CB5"
};

firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();

// Array to store team data
let teamData = {};

// Function to update the table
function updateTable() {
    // Sort teams by currency in descending order
    const sortedTeams = Object.keys(teamData).sort((a, b) => teamData[b] - teamData[a]);

    // Clear existing rows
    const tbody = document.getElementById('teamTableBody');
    tbody.innerHTML = '';

    // Append sorted rows
    sortedTeams.forEach(teamName => {
        const balance = teamData[teamName];
        const row = document.createElement('tr');
        row.id = teamName;
        row.innerHTML = `
            <td>${teamName}</td>
            <td>₹${balance}</td>
        `;
        tbody.appendChild(row);
    });
}

// Listen for real-time updates
db.collection('approved_buyers').onSnapshot((snapshot) => {
    snapshot.docChanges().forEach((change) => {
        const teamName = change.doc.id;
        const balance = change.doc.data().balance;

        if (change.type === "added" || change.type === "modified") {
            // Update team data
            teamData[teamName] = balance;
            updateTable();
        } else if (change.type === "removed") {
            // Remove team data
            delete teamData[teamName];
            updateTable();
        }
    });
}, (error) => {
    console.error("Error listening to changes: ", error);
});