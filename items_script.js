import { initializeApp } from "https://www.gstatic.com/firebasejs/9.22.1/firebase-app.js";
import { getFirestore, collection, getDocs } from "https://www.gstatic.com/firebasejs/9.22.1/firebase-firestore.js";

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

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

async function fetchItems() {
    const itemsList = document.getElementById('items');
    const querySnapshot = await getDocs(collection(db, "items"));
    
    itemsList.innerHTML = ""; // Clear any existing items

    querySnapshot.forEach((doc) => {
        const data = doc.data();
        const itemName = doc.id; // Use document ID as the item name
        const itemQuantity = data.quantity || 0;
        const itemPrice = data.price || 0;

        const itemElement = document.createElement('li');
        itemElement.innerHTML = `<strong>${itemName}</strong><br>Quantity: ${itemQuantity}<br>Price: ₹${itemPrice}`;
        itemsList.appendChild(itemElement);
    });
}

// Fetch and display items when the page loads
window.onload = fetchItems;
