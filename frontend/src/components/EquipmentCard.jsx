function EquipmentCard({equipment,onDelete,onViewMaintenance}) {
  return (
    <div>
      <h3>{equipment.name}</h3>
      <p><strong>Model:</strong> {equipment.model || "N/A"}</p>
      <p><strong>Serial Number:</strong> {equipment.serial_number || "N/A"}</p>
      <p><strong>Department:</strong> {equipment.department || "N/A"}</p>
      <p><strong>Status:</strong> {equipment.status || "N/A"}</p>
      <button onClick={() => onViewMaintenance(equipment.id)}>View Maintenenace</button>
      <button onClick={() => onDelete(equipment.id)}>Delete</button>
    </div>
  );
}

export default EquipmentCard;