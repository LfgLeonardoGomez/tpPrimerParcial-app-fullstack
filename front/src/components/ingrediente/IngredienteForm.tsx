import { useForm } from "react-hook-form";
import { Button } from "../common/Button";
import { useCreateIngrediente, useUpdateIngrediente } from "../../hooks/useIngrediente";
import type { IIngrediente, IIngredienteCreate, IIngredienteUpdate } from "../../interfaces/IIngrediente";

interface IngredienteFormProps {
    onClose: () => void;
    ingredienteToEdit?: IIngrediente;
}

export const IngredienteForm = ({ onClose, ingredienteToEdit }: IngredienteFormProps) => {
    const { register, handleSubmit, formState: { errors }, reset } = useForm<IIngredienteCreate>({
        defaultValues: ingredienteToEdit
            ? {
                nombre: ingredienteToEdit.nombre,
                descripcion: ingredienteToEdit.descripcion || "",
                es_alergeno: ingredienteToEdit.es_alergeno,
            }
            : {
                nombre: "",
                descripcion: "",
                es_alergeno: false,
            },
    });

    const createIngrediente = useCreateIngrediente();
    const updateIngrediente = useUpdateIngrediente();

    const onSubmit = async (data: IIngredienteCreate) => {
        try {
            if (ingredienteToEdit) {
                const updateData: IIngredienteUpdate = {
                    nombre: data.nombre,
                    descripcion: data.descripcion,
                    es_alergeno: data.es_alergeno,
                };
                await updateIngrediente.mutateAsync({
                    id: ingredienteToEdit.id,
                    ingrediente: updateData,
                });
            } else {
                await createIngrediente.mutateAsync(data);
            }
            reset();
            onClose();
        } catch (error) {
            console.error("Error al guardar el ingrediente", error);
        }
    };

    return (
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div>
                <label className="block text-sm font-medium mb-1">
                    Nombre
                </label>
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
                    placeholder="Ej: Tomate"
                />
                {errors.nombre && (
                    <p className="text-red-500 text-sm mt-1">{errors.nombre.message}</p>
                )}
            </div>

            <div>
                <label className="block text-sm font-medium mb-1">
                    Descripción
                </label>
                <textarea
                    {...register("descripcion", {
                        minLength: {
                            value: 3,
                            message: "La descripción debe tener al menos 3 caracteres",
                        },
                    })}
                    className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Descripción del ingrediente"
                    rows={3}
                />
                {errors.descripcion && (
                    <p className="text-red-500 text-sm mt-1">{errors.descripcion.message}</p>
                )}
            </div>

            <div className="flex items-center">
                <input
                    type="checkbox"
                    {...register("es_alergeno")}
                    className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <label className="ml-2 text-sm font-medium">
                    ¿Es un alérgeno?
                </label>
            </div>

            <div className="flex justify-end gap-2 pt-4">
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
                    disabled={createIngrediente.isPending || updateIngrediente.isPending}
                >
                    {ingredienteToEdit ? "Actualizar" : "Crear"}
                </Button>
            </div>
        </form>
    );
};
