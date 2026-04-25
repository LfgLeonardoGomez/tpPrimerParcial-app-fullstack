import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import * as productoService from "../services/productoService";
import type { IProducto, IProductoCreate, IProductoUpdate } from "../interfaces/IProducto";

export const useProductos = () => {
    return useQuery({
        queryKey: ["productos"],
        queryFn: () => productoService.getProductos(),
    });
};

export const useProductoById = (id: number) => {
    return useQuery({
        queryKey: ["producto", id],
        queryFn: () => productoService.getProductoById(id),
        enabled: !!id,
    });
};

export const useCreateProducto = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (producto: IProductoCreate) =>
            productoService.createProducto(producto),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["productos"] });
            queryClient.invalidateQueries({ queryKey: ["categorias"] });
            queryClient.invalidateQueries({ queryKey: ["ingredientes"] });
        },
    });
};

export const useUpdateProducto = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, producto }: { id: number; producto: IProductoUpdate }) =>
            productoService.updateProducto(id, producto),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["productos"] });
            queryClient.invalidateQueries({ queryKey: ["categorias"] });
                    },
    });
};

export const useDeleteProducto = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (id: number) =>
            productoService.deleteProducto(id),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["productos"] });
            queryClient.invalidateQueries({ queryKey: ["categorias"] });
            queryClient.invalidateQueries({ queryKey: ["ingredientes"] });
        },
    });
};

export const useUpdateProductoCategorias = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, categorias }: { id: number; categorias: number[] }) =>
            productoService.updateProductoCategorias(id, categorias),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["productos"] });
            queryClient.invalidateQueries({ queryKey: ["categorias"] });
        },
    });
};

export const useUpdateProductoIngredientes = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, ingredientes }: { id: number; ingredientes: number[] }) =>
            productoService.updateProductoIngredientes(id, ingredientes),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["productos"] });
            queryClient.invalidateQueries({ queryKey: ["ingredientes"] });
        },
    });
};