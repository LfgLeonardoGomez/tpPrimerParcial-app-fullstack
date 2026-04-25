import { Button } from "../common/Button";
import type { IProductoResponse } from "../../interfaces/IProducto";

interface ProductoDetailProps {
    producto: IProductoResponse;
    onClose: () => void;
}

export const ProductoDetail = ({ producto, onClose }: ProductoDetailProps) => {
    return (
        <div className="space-y-4">
            <div className="flex gap-4">
                {producto.imagen_url && (
                    <div className="w-32 h-32 flex-shrink-0">
                        <img
                            src={producto.imagen_url}
                            alt={producto.nombre}
                            className="w-full h-full object-cover rounded-lg"
                            onError={(e) => {
                                (e.target as HTMLImageElement).src = 'https://via.placeholder.com/128?text=Sin+imagen';
                            }}
                        />
                    </div>
                )}
                <div className="flex-1">
                    <h2 className="text-2xl font-bold mb-2">{producto.nombre}</h2>
                    <p className="text-gray-600 mb-4">{producto.descripcion || "Sin descripción"}</p>
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <p className="text-sm text-gray-500">Precio Base</p>
                            <p className="text-xl font-bold text-blue-600">${producto.precio_base}</p>
                        </div>
                        <div>
                            <p className="text-sm text-gray-500">Stock</p>
                            <p className={`text-xl font-bold ${producto.stock_cantidad > 0 ? 'text-green-600' : 'text-red-600'}`}>
                                {producto.stock_cantidad}
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            <hr />

            {/* Categorías */}
            <div>
                <h3 className="text-lg font-semibold mb-2">Categorías</h3>
                {producto.categorias.length > 0 ? (
                    <div className="flex flex-wrap gap-2">
                        {producto.categorias.map((categoria) => (
                            <span
                                key={categoria.id}
                                className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm"
                            >
                                {categoria.nombre}
                            </span>
                        ))}
                    </div>
                ) : (
                    <p className="text-gray-500 italic">Sin categorías asignadas</p>
                )}
            </div>

            {/* Ingredientes */}
            <div>
                <h3 className="text-lg font-semibold mb-2">Ingredientes ({producto.ingredientes.length})</h3>
                {producto.ingredientes.length > 0 ? (
                    <div className="flex flex-wrap gap-2">
                        {producto.ingredientes.map((ingrediente) => (
                            <span
                                key={ingrediente.id}
                                className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm"
                            >
                                {ingrediente.nombre}
                            </span>
                        ))}
                    </div>
                ) : (
                    <p className="text-gray-500 italic">Sin ingredientes asignados</p>
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
