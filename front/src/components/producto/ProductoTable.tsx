import { useProductos } from "../../hooks/useProducto";
import { Button } from "../common/Button";
import { Table } from "../common/table";
import type { IProductoResponse } from "../../interfaces/IProducto";

interface ProductoTableProps {
    onEdit: (producto: IProductoResponse) => void;
    onDelete?: (producto: IProductoResponse) => void;
    onView?: (producto: IProductoResponse) => void;
}

export const ProductoTable = ({ onEdit, onDelete, onView }: ProductoTableProps) => {
    const { data, isLoading, error } = useProductos();

    if (isLoading) return <p>Cargando...</p>;
    if (error) return <p>Error al cargar los productos</p>;

    return (
        <Table headers={["ID", "Nombre", "Precio", "Stock", "Categorías", "Acciones"]}>
            {data?.data.map((producto) => (
                <tr key={producto.id} className="border-t">
                    <td className="px-4 py-3">{producto.id}</td>
                    <td className="px-4 py-3">{producto.nombre}</td>
                    <td className="px-4 py-3">${producto.precio_base}</td>
                    <td className="px-4 py-3">
                        <span className={`px-2 py-1 rounded text-sm ${
                            producto.stock_cantidad > 0 
                                ? 'bg-green-100 text-green-800' 
                                : 'bg-red-100 text-red-800'
                        }`}>
                            {producto.stock_cantidad}
                        </span>
                    </td>
                    <td className="px-4 py-3">
                        {producto.categorias.length > 0 ? (
                            <div className="flex flex-wrap gap-1">
                                {producto.categorias.map((cat) => (
                                    <span key={cat.id} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">
                                        {cat.nombre}
                                    </span>
                                ))}
                            </div>
                        ) : (
                            <span className="text-gray-500 text-sm">Sin categoría</span>
                        )}
                    </td>
                    <td className="px-4 py-3 flex gap-2">
                        <Button 
                            variant="secondary"
                            className="text-sm"
                            onClick={() => onView?.(producto)}
                        >
                            Ver
                        </Button>
                        <Button 
                            variant="primary" 
                            className="text-sm"
                            onClick={() => onEdit(producto)}
                        >
                            Editar
                        </Button>
                        <Button 
                            variant="danger" 
                            className="text-sm"
                            onClick={() => onDelete?.(producto)}
                        >
                            Eliminar
                        </Button>
                    </td>
                </tr>
            ))}
        </Table>
    );
};
