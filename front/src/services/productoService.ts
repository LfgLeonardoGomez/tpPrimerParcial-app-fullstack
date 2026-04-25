import type { 
    IProducto, 
    IProductoCreate, 
    IProductoUpdate, 
    IProductoList, 
    IProductoCategoriasUpdate,
    IProductoIngredientesUpdate 
} from '../interfaces/IProducto';

const base_url = 'http://localhost:8000/productos'

export const getProductos = async (offset: number = 0, limit: number = 100): Promise<IProductoList> => {
    const response = await fetch(`${base_url}/?offset=${offset}&limit=${limit}`)
    if (!response.ok) {
        throw new Error('Error al obtener los productos');
    }
    const data = await response.json();
    return data;
}

export const getProductoById = async (id: number): Promise<IProducto> => {
    const response = await fetch(`${base_url}/${id}`)
    if (!response.ok) {
        throw new Error('Error al obtener el producto');
    }   
    const data = await response.json();
    return data;
}

export const createProducto = async (producto: IProductoCreate): Promise<IProducto> => {
    const response = await fetch(`${base_url}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(producto)
    });
    if (!response.ok) {
        throw new Error('Error al crear el producto');
    }
    const data = await response.json();
    return data;
}

export const updateProducto = async (id: number, producto: IProductoUpdate): Promise<IProducto> => {
    const response = await fetch(`${base_url}/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(producto)
    });
    if (!response.ok) {
        throw new Error('Error al actualizar el producto');
    }
    const data = await response.json();
    return data;
}

export const deleteProducto = async (id: number): Promise<boolean> => {
    const response = await fetch(`${base_url}/${id}`, {
        method: 'DELETE'
    });
    if (!response.ok) {
        throw new Error('Error al eliminar el producto');
    }
    return true;
}

export const updateProductoCategorias = async (id: number, categorias: number[]): Promise<IProducto> => {
    const response = await fetch(`${base_url}/${id}/categorias`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ categorias } as IProductoCategoriasUpdate)
    });
    if (!response.ok) {
        throw new Error('Error al actualizar las categorías del producto');
    }
    const data = await response.json();
    return data;
}

export const updateProductoIngredientes = async (id: number, ingredientes: number[]): Promise<IProducto> => {
    const response = await fetch(`${base_url}/${id}/ingredientes`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ingredientes } as IProductoIngredientesUpdate)
    });
    if (!response.ok) {
        throw new Error('Error al actualizar los ingredientes del producto');
    }
    const data = await response.json();
    return data;
}
