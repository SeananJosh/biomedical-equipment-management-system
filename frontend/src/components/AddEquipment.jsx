import { useState } from "react";

function AddEquipment({ onEquipmentAdded }) {
    const [name, setName] = useState("");
    const [model, setModel] = useState("");
    const [serialNumber, setSerialNumber] = useState("");
    const [department, setDepartment] = useState("");
    const [status, setStatus] = useState("");
    function handleSubmit(e) {
    e.preventDefault();
    const equipmentData = {
        name: name,
        model: model,
        serial_number: serialNumber,
        department: department,
        status: status
    };
    fetch("http://127.0.0.1:8000/equipment", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(equipmentData)
    }).then(response => response.json()).then((data) => {
    onEquipmentAdded(data.equipment);
});
    console.log(name);
    console.log(model);
    console.log(serialNumber);
    console.log(department);
    console.log(status);
    }
  return (
    <div>
      <h2>Add New Equipment</h2>

      <form onSubmit={handleSubmit}>
        <input
          placeholder="Equipment name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          placeholder="Model"
          value={model}
          onChange={(e) => setModel(e.target.value)}
        />
        <input
          placeholder="Serial number"
          value={serialNumber}
          onChange={(e) => setSerialNumber(e.target.value)}
        />
        <input
          placeholder="Department"
          value={department}
          onChange={(e) => setDepartment(e.target.value)}
        />
        <input
          placeholder="Status"
          value={status}
          onChange={(e) => setStatus(e.target.value)}
        />

        <button type="submit">Add Equipment</button>
      </form>
    </div>
  );
}

export default AddEquipment;