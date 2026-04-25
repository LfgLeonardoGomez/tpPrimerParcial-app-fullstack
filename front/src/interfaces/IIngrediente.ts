export interface IIngrediente {
    id: number;
    nombre: string;
    descripcion?: string | null;
    es_alergeno: boolean;
    disponible: boolean;
}

export interface IIngredienteCreate {
    nombre: string;
    descripcion?: string;
    es_alergeno: boolean;
}

export interface IIngredienteUpdate {
    nombre?: string;
    descripcion?: string;
    es_alergeno?: boolean;
}

export interface IIngredienteResponse extends IIngrediente {
    productos?: any[];
}

export interface IIngredienteList {
    data: IIngredienteResponse[];
    count: number;
}
