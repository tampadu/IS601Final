// app/static/js/calculations.js

async function fetchCalculations() {
    try {
        const res = await fetch("/calculations/"); // public endpoint now
        if (!res.ok) throw new Error("Failed to fetch calculations");
        const data = await res.json();

        const tableBody = document.querySelector("#calc-table-body");
        tableBody.innerHTML = "";

        data.forEach(calc => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${calc.id}</td>
                <td>${calc.a}</td>
                <td>${calc.b}</td>
                <td>${calc.type}</td>
                <td>${calc.result}</td>
                <td>
                    <button onclick="editCalculation(${calc.id})">Edit</button>
                    <button onclick="deleteCalculation(${calc.id})">Delete</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    } catch (err) {
        console.error(err);
        alert("Error loading calculations");
    }
}

// Call this on page load
window.addEventListener("DOMContentLoaded", fetchCalculations);

// Add calculation
async function addCalculation() {
    const a = parseFloat(document.querySelector("#a").value);
    const b = parseFloat(document.querySelector("#b").value);
    const type = document.querySelector("#type").value;

    try {
        const res = await fetch("/calculations/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ a, b, type })
        });
        if (!res.ok) throw new Error("Failed to add calculation");
        document.querySelector("#a").value = "";
        document.querySelector("#b").value = "";
        fetchCalculations(); // Refresh table
    } catch (err) {
        console.error(err);
        alert("Error adding calculation");
    }
}

// Edit calculation
async function editCalculation(id) {
    const newType = prompt("Enter new type (Add, Sub, Multiply, Divide):");
    if (!newType) return;

    try {
        const res = await fetch(`/calculations/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ a: 0, b: 0, type: newType }) // a & b could be updated too
        });
        if (!res.ok) throw new Error("Failed to edit calculation");
        fetchCalculations();
    } catch (err) {
        console.error(err);
        alert("Error editing calculation");
    }
}

// Delete calculation
async function deleteCalculation(id) {
    if (!confirm("Are you sure you want to delete this calculation?")) return;
    try {
        const res = await fetch(`/calculations/${id}`, { method: "DELETE" });
        if (!res.ok) throw new Error("Failed to delete calculation");
        fetchCalculations();
    } catch (err) {
        console.error(err);
        alert("Error deleting calculation");
    }
}
