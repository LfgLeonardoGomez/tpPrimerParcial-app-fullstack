import { useCategorias } from "../../hooks/useCategoria";
import { Button } from "../common/Button";
import { Table } from "../common/table";
import type {ICategoria} from "../../interfaces/ICategoria";

interface CategoriaTableProps {
    onEdit: (categoria: ICategoria) => void;
    onDelete?: (categoria: ICategoria) => void;
    onView?: (categoria: ICategoria) => void;
}

export const CategoriaTable = ({ onEdit, onDelete, onView }: CategoriaTableProps) => {
    const { data, isLoading, error } = useCategorias();

    if (isLoading) return <p>Cargando...</p>;
    if (error) return <p>Error al cargar las categorías</p>;

    return (
    <Table headers={["ID", "Nombre", "Descripción", "Acciones"]}>
        {data?.data.map((category) => (
            <tr key={category.id} className="border-t">
            <td className="px-4 py-3">{category.id}</td>

            <td className="px-4 py-3">{category.nombre}</td>

            <td className="px-4 py-3">{category.descripcion || "-"}</td>

            <td className="px-4 py-3 flex gap-2">
                <Button variant="secondary" onClick={() => onView?.(category)}>
                    Ver
                </Button>

                <Button variant="primary" onClick={() => onEdit(category)}>
                    Editar
                </Button>

                <Button variant="danger" onClick={() => onDelete?.(category)}>
                    Eliminar
                </Button>
            </td>
            </tr>
        ))}
    </Table>
    );
};
