import Header from './components/Header';
import EquipmentCard from './components/EquipmentCard';
import AddEquipment from './components/AddEquipment';
import AddMaintenance from './components/AddMaintenance';
import { useEffect, useState } from "react";
function App(){
  const [equipmentList, setEquipmentList] = useState([]);
  const [selectedEquipmentId, setSelectedEquipmentId] = useState(null);
  useEffect(() => {
  fetch("http://127.0.0.1:8000/equipment")
    .then(response => response.json())
    .then(data => setEquipmentList(data));
}, []);
function handleDelete(id) {
    fetch(`http://127.0.0.1:8000/equipment/${id}`, {
        method: "DELETE"
    }).then(()=>{ setEquipmentList(currentList => currentList.filter(equipment => equipment.id !== id));
  });
}
const [maintenance, setMaintenance] = useState([]);
function onViewMaintenance(id)
{
  setSelectedEquipmentId(id);
  fetch(`http://127.0.0.1:8000/equipment/${id}/maintenance`)
  .then(response => response.json())
  .then(data => setMaintenance(data));
}
  return(
    <div>
      <Header title="Biomedical Equipment Management System" />
      <p>Total equipment: {equipmentList.length}</p>
      <AddEquipment
  onEquipmentAdded={(newEquipment) =>
    setEquipmentList([...equipmentList, newEquipment])
  }
/>
      {equipmentList.map((equipment) => (
  <EquipmentCard
    key={equipment.id}
    equipment={equipment}
    onDelete={handleDelete}
    onViewMaintenance={onViewMaintenance}
  />
))}
{selectedEquipmentId !== null && (
  <AddMaintenance
    equipmentId={selectedEquipmentId}
    onMaintenanceAdded={(newRecord) =>
        setMaintenance(currentMaintenance => [
            ...currentMaintenance,
            newRecord
        ])
    }
/>
)}
  {
    maintenance.map((record) => (
      <div key={record.id}>
        <p>{record.id}</p>
        <p>{record.equipment_id}</p>
        <p>{record.description}</p>
      </div>
    ))
  }
    </div>
  );

}
export default App;