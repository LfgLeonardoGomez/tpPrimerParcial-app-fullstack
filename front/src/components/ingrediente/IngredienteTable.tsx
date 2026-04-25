import { useIngredientes } from "../../hooks/useIngrediente";
import { Button } from "../common/Button";
import { Table } from "../common/table";
import type { IIngrediente } from "../../interfaces/IIngrediente";

interface IngredienteTableProps {
    onEdit: (ingrediente: IIngrediente) => void;
    onDelete?: (ingrediente: IIngrediente) => void;
}

export const IngredienteTable = ({ onEdit, onDelete }: IngredienteTableProps) => {
    const { data, isLoading, error } = useIngredientes();

    if (isLoading) return <p>Cargando...</p>;
    if (error) return <p>Error al cargar los ingredientes</p>;

    return (
        <Table headers={["ID", "Nombre", "Descripción", "¿Alérgeno?", "Acciones"]}>
            {data?.data.map((ingrediente) => (
                <tr key={ingrediente.id} className="border-t">
                    <td className="px-4 py-3">{ingrediente.id}</td>
                    <td className="px-4 py-3">{ingrediente.nombre}</td>
                    <td className="px-4 py-3">{ingrediente.descripcion || "-"}</td>
                    <td className="px-4 py-3">
                        {ingrediente.es_alergeno ? (
                            <span className="bg-red-100 text-red-800 px-2 py-1 rounded text-sm">
                                Sí
                            </span>
                        ) : (
                            <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-sm">
                                No
                            </span>
                        )}
                    </td>
                    <td className="px-4 py-3 flex gap-2">
                        <Button variant="secondary">Ver</Button>
                        <Button variant="primary" onClick={() => onEdit(ingrediente)}>
                            Editar
                        </Button>
                        <Button variant="danger" onClick={() => onDelete?.(ingrediente)}>
                            Eliminar
                        </Button>
                    </td>
                </tr>
            ))}
        </Table>
    );
};
