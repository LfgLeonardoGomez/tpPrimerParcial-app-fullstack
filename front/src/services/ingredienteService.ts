import type { IIngrediente, IIngredienteCreate, IIngredienteUpdate, IIngredienteList } from '../interfaces/IIngrediente';

const base_url = 'http://localhost:8000/ingredientes'

export const getIngredientes = async (offset: number = 0, limit: number = 100): Promise<IIngredienteList> => {
    const response = await fetch(`${base_url}/?offset=${offset}&limit=${limit}`)
    if (!response.ok) {
        throw new Error('Error al obtener los ingredientes');
    }
    const data = await response.json();
    return data;
}

export const getIngredienteById = async (id: number): Promise<IIngrediente> => {
    const response = await fetch(`${base_url}/${id}`)
    if (!response.ok) {
        throw new Error('Error al obtener el ingrediente');
    }   
    const data = await response.json();
    return data;
}

export const createIngrediente = async (ingrediente: IIngredienteCreate): Promise<IIngrediente> => {
    const response = await fetch(`${base_url}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(ingrediente)
    });
    if (!response.ok) {
        throw new Error('Error al crear el ingrediente');
    }
    const data = await response.json();
    return data;
}

export const updateIngrediente = async (id: number, ingrediente: IIngredienteUpdate): Promise<IIngrediente> => {
    const response = await fetch(`${base_url}/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(ingrediente)
    });
    if (!response.ok) {
        throw new Error('Error al actualizar el ingrediente');
    }
    const data = await response.json();
    return data;
}

export const deleteIngrediente = async (id: number): Promise<boolean> => {
    const response = await fetch(`${base_url}/${id}`, {
        method: 'DELETE'
    });
    if (!response.ok) {
        throw new Error('Error al eliminar el ingrediente');
    }
    return true;
}
