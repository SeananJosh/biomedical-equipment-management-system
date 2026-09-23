import { useState } from "react";

function AddMaintenance({ equipmentId, onMaintenanceAdded }) {
    const [description, setDescription] = useState("");

    function handleSubmit(e) {
        e.preventDefault();

        const maintenanceData = {
            description: description
        };

        fetch(`http://127.0.0.1:8000/equipment/${equipmentId}/maintenance`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(maintenanceData)
        })
        .then(response => response.json())
        .then(data => {
            onMaintenanceAdded(data);
            setDescription("");
        });
    }

    return (
        <form onSubmit={handleSubmit}>
            <input
                placeholder="Maintenance description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
            />

            <button type="submit">
                Add Maintenance
            </button>
        </form>
    );
}

export default AddMaintenance;