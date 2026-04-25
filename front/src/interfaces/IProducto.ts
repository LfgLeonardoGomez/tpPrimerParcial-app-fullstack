export interface ICategoriaSimple {
    id: number;
    nombre: string;
}

export interface IIngredienteSimple {
    id: number;
    nombre: string;
}

export interface IProducto {
    id: number;
    nombre: string;
    descripcion?: string;
    precio_base: string;
    imagen_url?: string;
    stock_cantidad: number;
    disponible: boolean;
}

export interface IProductoCreate {
    nombre: string;
    descripcion?: string;
    precio_base: string;
    imagen_url?: string;
    stock_cantidad?: number;
    disponible?: boolean;
}

export interface IProductoUpdate {
    nombre?: string;
    descripcion?: string;
    precio_base?: string;
    imagen_url?: string;
    stock_cantidad?: number;
    disponible?: boolean;
}

export interface IProductoResponse extends IProducto {
    categorias: ICategoriaSimple[];
    ingredientes: IIngredienteSimple[];
}

export interface IProductoList {
    data: IProductoResponse[];
    count: number;
}

export interface IProductoCategoriasUpdate {
    categorias: number[];
}

export interface IProductoIngredientesUpdate {
    ingredientes: number[];
}