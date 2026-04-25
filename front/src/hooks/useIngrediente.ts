import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import * as ingredienteService from "../services/ingredienteService";
import type { IIngrediente, IIngredienteCreate, IIngredienteUpdate } from "../interfaces/IIngrediente";

export const useIngredientes = () => {
    return useQuery({
        queryKey: ["ingredientes"],
        queryFn: () => ingredienteService.getIngredientes(),
    });
};

export const useIngredienteById = (id: number) => {
    return useQuery({
        queryKey: ["ingrediente", id],
        queryFn: () => ingredienteService.getIngredienteById(id),
        enabled: !!id,
    });
};

export const useCreateIngrediente = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (ingrediente: IIngredienteCreate) =>
            ingredienteService.createIngrediente(ingrediente),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["ingredientes"] });
        },
    });
};

export const useUpdateIngrediente = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, ingrediente }: { id: number; ingrediente: IIngredienteUpdate }) =>
            ingredienteService.updateIngrediente(id, ingrediente),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["ingredientes"] });
        },
    });
};

export const useDeleteIngrediente = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (id: number) =>
            ingredienteService.deleteIngrediente(id),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["ingredientes"] });
        },
    });
};
