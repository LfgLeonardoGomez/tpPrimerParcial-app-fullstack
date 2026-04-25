import {useForm} from "react-hook-form";
import {Button} from "../common/Button";
import {useCategoriaCreate, useUpdateCategoria} from "../../hooks/useCategoria";
import type {ICategoriaCreate, ICategoria} from "../../interfaces/ICategoria";
import { useEffect } from "react";

interface CategoriaFormProps {
    onClose: ()=> void;
    categoriaToEdit?: ICategoria;
}

export const CategoriaForm = ({onClose, categoriaToEdit}: CategoriaFormProps) => {
    const {register, handleSubmit, reset} = useForm<ICategoriaCreate>();
    const createCategoria = useCategoriaCreate();
    const updateCategoria = useUpdateCategoria();

    const isEditMode = !!categoriaToEdit

    useEffect(() => {
        if (categoriaToEdit) {
            reset({
                nombre: categoriaToEdit.nombre,
                descripcion: categoriaToEdit.descripcion || "",
        })
        }
    }, [categoriaToEdit, reset])

    const onSubmit = async (data: ICategoriaCreate) => {
        try {
                if (isEditMode && categoriaToEdit) {
                    await updateCategoria.mutateAsync({
                    id: categoriaToEdit.id,
                    categoria: data,
                })
                } else {
                    await createCategoria.mutateAsync(data)
                }
                reset();
                onClose();
        } catch (error) {
            console.error("Error al crear la categoría", error);
        }}
        return  (
        <form
        onSubmit={handleSubmit(onSubmit)}
        className="space-y-4"
        >
        <div>
            <label className="block mb-1 font-medium">
            Nombre
            </label>

            <input
            {...register("nombre", {
                required: true,
            })}
            className="w-full border rounded-lg px-3 py-2"
            />
        </div>

        <div>
            <label className="block mb-1 font-medium">
            Descripción
            </label>

            <textarea
            {...register("descripcion")}
            className="w-full border rounded-lg px-3 py-2"
            />
        </div>

        <div className="flex justify-end gap-2">
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
            >
            {isEditMode
                ? "Actualizar"
                : "Guardar"}
            </Button>
        </div>
        </form>
    )
}
