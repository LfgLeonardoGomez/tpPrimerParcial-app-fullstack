import { Button } from "../common/Button";
import type { ICategoria } from "../../interfaces/ICategoria";

interface CategoriaDetailProps {
    categoria: ICategoria;
    onClose: () => void;
}

export const CategoriaDetail = ({ categoria, onClose }: CategoriaDetailProps) => {
    return (
        <div className="space-y-4">
            <div>
                <h2 className="text-xl font-bold mb-2">{categoria.nombre}</h2>
                <p className="text-gray-600">{categoria.descripcion}</p>
            </div>

            <div>
                <h3 className="text-lg font-semibold mb-3">
                    Productos ({categoria.productos.length})
                </h3>

                {categoria.productos.length > 0 ? (
                    <div className="space-y-2">
                        {categoria.productos.map((producto) => (
                            <div
                                key={producto.id}
                                className="flex items-center justify-between p-3 bg-gray-50 rounded-md border border-gray-200 hover:bg-gray-100 transition"
                            >
                                <div>
                                    <p className="font-medium">{producto.nombre}</p>
                                    <p className="text-sm text-gray-500">ID: {producto.id}</p>
                                </div>
                                <Button
                                    variant="secondary"
                                    className="text-sm"
                                >
                                    Ver
                                </Button>
                            </div>
                        ))}
                    </div>
                ) : (
                    <p className="text-gray-500 italic">No hay productos en esta categoría</p>
                )}
            </div>

            <div className="flex justify-end pt-4 border-t">
                <Button
                    variant="secondary"
                    onClick={onClose}
                >
                    Cerrar
                </Button>
            </div>
        </div>
    );
};
