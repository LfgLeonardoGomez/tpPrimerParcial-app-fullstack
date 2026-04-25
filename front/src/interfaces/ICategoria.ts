export type ICategoria = {
    id: number;
    nombre: string;
    descripcion: string;
    productos: IProductoSimple[];
}

export type IProductoSimple = {
    id: number;
    nombre: string;
}

export type ICategoriaCreate = {
    nombre: string;
    descripcion: string;
}

export type ICategoriaUpdate = {
    nombre?: string;
    descripcion: string;
}

export type ICategoriaList = {
    data: ICategoria[];
    count: number;
}