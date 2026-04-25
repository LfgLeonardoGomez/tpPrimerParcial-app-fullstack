import type { ICategoria,ICategoriaCreate,ICategoriaUpdate,ICategoriaList} from '../interfaces/ICategoria';


const base_url = 'http://localhost:8000/categorias'

export const getCategorias = async (offset: number = 0, limit: number = 100): Promise<ICategoriaList> => {
    const response = await fetch(`${base_url}/?offset=${offset}&limit=${limit}`)
    if (!response.ok) {
        throw new Error('Error al obtener las categorias');
    }
    const data = await response.json();
    return data;
}

export const getCategoriaById = async (id:number): Promise<ICategoria> => {
    const response = await fetch (`${base_url}/${id}`)
    if (!response.ok) {
        throw new Error('Error al obtener la categoria');
    }   
    const data = await response.json();
    return data;
}

export const createCategoria = async(categoria: ICategoriaCreate): Promise<ICategoria> => {
    const response = await fetch (`${base_url}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(categoria)
    });
    if (!response.ok) {
        throw new Error('Error al crear la categoria');
    }
    const data = await response.json();
    return data;
}

export const updateCategoria = async (id:number, categoria: ICategoriaUpdate): Promise<ICategoria> => {
    const response = await fetch (`${base_url}/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(categoria)
    });
    if (!response.ok) {
        throw new Error('Error al actualizar la categoria');
    }
    const data = await response.json();
    return data;
}


export const deleteCategoria = async (id:number): Promise<boolean> => {
    const response = await fetch (`${base_url}/${id}`, {
        method: 'DELETE'
    });
    if (!response.ok) {
        throw new Error('Error al eliminar la categoria');
    }
    return true;
}