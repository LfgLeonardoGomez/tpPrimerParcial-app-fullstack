import { useQuery, useMutation, useQueryClient} from '@tanstack/react-query';
import type { ICategoria, ICategoriaCreate, ICategoriaUpdate, ICategoriaList } from '../interfaces/ICategoria';
import { getCategorias, getCategoriaById, createCategoria, updateCategoria, deleteCategoria } from '../services/categoriaService';

const QUERY_KEY = 'categorias';

export const useCategorias = (
    offset: number = 0, limit: number = 100) => {
        return useQuery<ICategoriaList, Error>({
            queryKey: [QUERY_KEY, offset, limit], 
            queryFn: () => getCategorias(offset, limit),
        });
    }

export const useCategoriaById = (id: number) => {
    return useQuery< ICategoria>({
        queryKey: [QUERY_KEY, id],
        queryFn: () => getCategoriaById(id),
    });
}

export const useCategoriaCreate = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: (categoria: ICategoriaCreate) => createCategoria(categoria),
        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: [QUERY_KEY]
            });
        }
    });
}

export const useUpdateCategoria = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: ({id, categoria}: {id: number, categoria: ICategoriaUpdate}) => updateCategoria(id, categoria),
        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: [QUERY_KEY]
            });
        }
    });
}

export const useDeleteCategoria = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: (id: number) => deleteCategoria(id),
        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: [QUERY_KEY]
            });
        }
    });
}