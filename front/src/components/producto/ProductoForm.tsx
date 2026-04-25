import { useForm } from "react-hook-form";
import { useEffect, useState } from "react";
import { Button } from "../common/Button";
import { useCreateProducto, useUpdateProducto, useUpdateProductoCategorias, useUpdateProductoIngredientes } from "../../hooks/useProducto";
import { useCategorias } from "../../hooks/useCategoria";
import { useIngredientes } from "../../hooks/useIngrediente";
import type { IProductoCreate, IProductoUpdate, IProductoResponse } from "../../interfaces/IProducto";

interface ProductoFormProps {
    onClose: () => void;
    productoToEdit?: IProductoResponse;
}

export const ProductoForm = ({ onClose, productoToEdit }: ProductoFormProps) => {
    const { register, handleSubmit, formState: { errors }, reset, watch } = useForm<IProductoCreate>({
        defaultValues: productoToEdit
            ? {
                nombre: productoToEdit.nombre,
                descripcion: productoToEdit.descripcion || "",
                precio_base: productoToEdit.precio_base,
                imagen_url: productoToEdit.imagen_url || "",
                stock_cantidad: productoToEdit.stock_cantidad,
                disponible: productoToEdit.disponible,
            }
            : {
                nombre: "",
                descripcion: "",
                precio_base: "",
                imagen_url: "",
                stock_cantidad: 0,
                disponible: true,
            },
    });

    const [selectedCategorias, setSelectedCategorias] = useState<number[]>(
        productoToEdit?.categorias.map(c => c.id) || []
    );
    const [selectedIngredientes, setSelectedIngredientes] = useState<number[]>(
        productoToEdit?.ingredientes.map(i => i.id) || []
    );

    const { data: categoriasData } = useCategorias();
    const { data: ingredientesData } = useIngredientes();

    const createProducto = useCreateProducto();
    const updateProducto = useUpdateProducto();
    const updateProductoCategorias = useUpdateProductoCategorias();
    const updateProductoIngredientes = useUpdateProductoIngredientes();

    const onSubmit = async (data: IProductoCreate) => {
        try {
            if (productoToEdit) {
                const updateData: IProductoUpdate = {
                    nombre: data.nombre,
                    descripcion: data.descripcion,
                    precio_base: data.precio_base,
                    imagen_url: data.imagen_url,
                    stock_cantidad: data.stock_cantidad,
                    disponible: data.disponible,
                };
                await updateProducto.mutateAsync({
                    id: productoToEdit.id,
                    producto: updateData,
                });

                if (selectedCategorias.length > 0) {
                    await updateProductoCategorias.mutateAsync({
                        id: productoToEdit.id,
                        categorias: selectedCategorias,
                    });
                }

                if (selectedIngredientes.length > 0) {
                    await updateProductoIngredientes.mutateAsync({
                        id: productoToEdit.id,
                        ingredientes: selectedIngredientes,
                    });
                }
            } else {
                const nuevo_producto =await createProducto.mutateAsync(data);
                
                if (selectedCategorias.length > 0) {
                    await updateProductoCategorias.mutateAsync({
                        id: nuevo_producto.id,
                        categorias: selectedCategorias,
                    });
                }

                if (selectedIngredientes.length > 0) {
                    await updateProductoIngredientes.mutateAsync({
                        id: nuevo_producto.id,
                        ingredientes: selectedIngredientes,
                    });
                }
            }
            reset();
            onClose();
        } catch (error) {
            console.error("Error al guardar el producto", error);
        }
    };

    const handleCategoriaChange = (categoriaId: number) => {
        setSelectedCategorias(prev =>
            prev.includes(categoriaId)
                ? prev.filter(id => id !== categoriaId)
                : [...prev, categoriaId]
        );
    };

    const handleIngredienteChange = (ingredienteId: number) => {
        setSelectedIngredientes(prev =>
            prev.includes(ingredienteId)
                ? prev.filter(id => id !== ingredienteId)
                : [...prev, ingredienteId]
        );
    };

    return (
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 max-h-96 overflow-y-auto pr-2">
            <div>
                <label className="block text-sm font-medium mb-1">Nombre</label>
                <input
                    type="text"
                    {...register("nombre", {
                        required: "El nombre es requerido",
                        minLength: {
                            value: 3,
                            message: "El nombre debe tener al menos 3 caracteres",
                        },
                    })}
                    className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Ej: Pizza Margarita"
                />
                {errors.nombre && (
                    <p className="text-red-500 text-sm mt-1">{errors.nombre.message}</p>
                )}
            </div>

            <div>
                <label className="block text-sm font-medium mb-1">Descripción</label>
                <textarea
                    {...register("descripcion", {
                        minLength: {
                            value: 3,
                            message: "La descripción debe tener al menos 3 caracteres",
                        },
                    })}
                    className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Descripción del producto"
                    rows={2}
                />
                {errors.descripcion && (
                    <p className="text-red-500 text-sm mt-1">{errors.descripcion.message}</p>
                )}
            </div>

            <div className="grid grid-cols-2 gap-4">
                <div>
                    <label className="block text-sm font-medium mb-1">Precio Base</label>
                    <input
                        type="text"
                        {...register("precio_base", {
                            required: "El precio es requerido",
                        })}
                        className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="12000"
                    />
                    {errors.precio_base && (
                        <p className="text-red-500 text-sm mt-1">{errors.precio_base.message}</p>
                    )}
                </div>

                <div>
                    <label className="block text-sm font-medium mb-1">Stock</label>
                    <input
                        type="number"
                        {...register("stock_cantidad", {
                            min: {
                                value: 0,
                                message: "El stock no puede ser negativo",
                            },
                        })}
                        className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="0"
                    />
                    {errors.stock_cantidad && (
                        <p className="text-red-500 text-sm mt-1">{errors.stock_cantidad.message}</p>
                    )}
                </div>
            </div>

            <div>
                <label className="block text-sm font-medium mb-1">URL Imagen</label>
                <input
                    type="text"
                    {...register("imagen_url")}
                    className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="https://ejemplo.com/imagen.jpg"
                />
            </div>

            {/* Categorías Multi-select */}
            <div>
                <label className="block text-sm font-medium mb-2">Categorías</label>
                <div className="border rounded-md p-3 max-h-32 overflow-y-auto bg-gray-50">
                    {categoriasData?.data && categoriasData.data.length > 0 ? (
                        categoriasData.data.map((categoria) => (
                            <div key={categoria.id} className="flex items-center mb-2">
                                <input
                                    type="checkbox"
                                    id={`cat-${categoria.id}`}
                                    checked={selectedCategorias.includes(categoria.id)}
                                    onChange={() => handleCategoriaChange(categoria.id)}
                                    className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                                />
                                <label htmlFor={`cat-${categoria.id}`} className="ml-2 text-sm cursor-pointer">
                                    {categoria.nombre}
                                </label>
                            </div>
                        ))
                    ) : (
                        <p className="text-gray-500 text-sm">No hay categorías disponibles</p>
                    )}
                </div>
            </div>

            {/* Ingredientes Multi-select */}
            <div>
                <label className="block text-sm font-medium mb-2">Ingredientes</label>
                <div className="border rounded-md p-3 max-h-32 overflow-y-auto bg-gray-50">
                    {ingredientesData?.data && ingredientesData.data.length > 0 ? (
                        ingredientesData.data.map((ingrediente) => (
                            <div key={ingrediente.id} className="flex items-center mb-2">
                                <input
                                    type="checkbox"
                                    id={`ing-${ingrediente.id}`}
                                    checked={selectedIngredientes.includes(ingrediente.id)}
                                    onChange={() => handleIngredienteChange(ingrediente.id)}
                                    className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                                />
                                <label htmlFor={`ing-${ingrediente.id}`} className="ml-2 text-sm cursor-pointer">
                                    {ingrediente.nombre}
                                </label>
                            </div>
                        ))
                    ) : (
                        <p className="text-gray-500 text-sm">No hay ingredientes disponibles</p>
                    )}
                </div>
            </div>

            <div className="flex items-center">
                <input
                    type="checkbox"
                    {...register("disponible")}
                    className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <label className="ml-2 text-sm font-medium">Disponible</label>
            </div>

            <div className="flex justify-end gap-2 pt-4 border-t sticky bottom-0 bg-white">
                <Button
                    type="button"
                    variant="secondary"
                    onClick={onClose}
                >
                    Cancelar
                </Button>
                <Button
                    type="submit"
                    variant="primary"
                    disabled={createProducto.isPending || updateProducto.isPending || updateProductoCategorias.isPending || updateProductoIngredientes.isPending}
                >
                    {productoToEdit ? "Actualizar" : "Crear"}
                </Button>
            </div>
        </form>
    );
};
