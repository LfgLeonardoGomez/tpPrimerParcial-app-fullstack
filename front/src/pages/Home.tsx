import {useState} from "react"
import {Button} from "../components/common/Button";
import {CategoriaTable} from "../components/categoria/CategoriaTable";
import {Modal} from "../components/common/Modal";
import {CategoriaForm} from "../components/categoria/CategoriaForm";
import { CategoriaDetail } from "../components/categoria/CategoriaDetail";
import type { ICategoria } from "../interfaces/ICategoria";
import { useDeleteCategoria } from "../hooks/useCategoria";
import { useDeleteIngrediente } from "../hooks/useIngrediente";
import { IngredienteTable } from "../components/ingrediente/IngredienteTable";
import { IngredienteForm } from "../components/ingrediente/IngredienteForm";
import type { IIngrediente } from "../interfaces/IIngrediente";
import { ProductoTable } from "../components/producto/ProductoTable";
import { ProductoForm } from "../components/producto/ProductoForm";
import { ProductoDetail } from "../components/producto/ProductoDetail";
import { useDeleteProducto } from "../hooks/useProducto";
import type { IProductoResponse } from "../interfaces/IProducto";


type Section = "categorias" | "productos" | "ingredientes";

export const Home = () => {
    const [section, setSection] = useState<Section>("categorias")

    const [isModalOpen, setIsModalOpen] = useState(false);

    const [categoriaToEdit, setCategoriaToEdit] = useState<ICategoria | undefined>(undefined);
    const [categoriaToDelete, setCategoriaToDelete] = useState<ICategoria | undefined>(undefined);
    const [categoriaToView, setCategoriaToView] = useState<ICategoria | undefined>(undefined)
    const deleteCategoria = useDeleteCategoria();

    const [ingredienteToEdit, setIngredienteToEdit] = useState<IIngrediente | undefined>(undefined);
    const [ingredienteToDelete, setIngredienteToDelete] = useState<IIngrediente | undefined>(undefined);
    const deleteIngrediente = useDeleteIngrediente();

    const [productoToEdit, setProductoToEdit] = useState<IProductoResponse | undefined>(undefined);
    const [productoToDelete, setProductoToDelete] = useState<IProductoResponse | undefined>(undefined);
    const [productoToView, setProductoToView] = useState<IProductoResponse | undefined>(undefined);
    const deleteProducto = useDeleteProducto();

    const openModal = () => setIsModalOpen(true);
    const closeModal = () => {
        setIsModalOpen(false)
        setCategoriaToEdit(undefined);
    };

    const handleEditCategoria = (categoria: ICategoria) => {
        setCategoriaToEdit(categoria);
        setIsModalOpen(true);
    };
    const handleDeleteCategoria = (categoria: ICategoria) => {
        setCategoriaToDelete(categoria);
            }

    const confirmDelete = async () => {
        if (!categoriaToDelete) return
            await deleteCategoria.mutateAsync(categoriaToDelete.id);
            setCategoriaToDelete(undefined);
    }
    const handleViewCategoria = (categoria: ICategoria) => {
            setCategoriaToView(categoria);
            setIsModalOpen(true);
};

    const handleEditProducto = (producto: IProductoResponse) => {
        setProductoToEdit(producto);
        setIsModalOpen(true);
};

    const handleDeleteProducto = (producto: IProductoResponse) => {
        setProductoToDelete(producto);
};

    const handleViewProducto = (producto: IProductoResponse) => {
        setProductoToView(producto);
        setIsModalOpen(true);
};

    const confirmDeleteProducto = async () => {
        if (!productoToDelete) return;
        await deleteProducto.mutateAsync(productoToDelete.id);
        setProductoToDelete(undefined);
};


    const handleEditIngrediente = (ingrediente: IIngrediente) => {
        setIngredienteToEdit(ingrediente);
        setIsModalOpen(true);
        };

const handleDeleteIngrediente = (ingrediente: IIngrediente) => {
    setIngredienteToDelete(ingrediente);
};

const confirmDeleteIngrediente = async () => {
    if (!ingredienteToDelete) return;
    await deleteIngrediente.mutateAsync(ingredienteToDelete.id);
    setIngredienteToDelete(undefined);
};
    return (
            <div className="p-6 space-y-6">
        <h1 className="text-3xl font-bold">
            Panel de Administración
        </h1>

        <div className="flex gap-4">
            <Button
            variant="secondary"
            onClick={() => setSection("categorias")}
            >
            Categorías
            </Button>

            <Button
            variant="secondary"
            onClick={() => setSection("productos")}
            >
            Productos
            </Button>

            <Button
            variant="secondary"
            onClick={() => setSection("ingredientes")}
            >
            Ingredientes
            </Button>
        </div>

        <div>
            {section === "categorias" && (
            
                <>
                <div className="flex justify-end">
                    <Button
                    variant="primary"
                    onClick={openModal}
                    >
                    Nueva Categoría
                    </Button>
                </div>

                <CategoriaTable onEdit={handleEditCategoria} onDelete={handleDeleteCategoria}  onView={handleViewCategoria}/>
                
                {/* modal para crear/editar categoria */}
                    
                <Modal
                    isOpen={isModalOpen}
                    onClose={closeModal}
                    title={
                        categoriaToEdit
                            ? "Editar categoría"
                            : "Crear nueva categoría"
                        }
                >
                    <CategoriaForm
                        onClose={closeModal}
                        categoriaToEdit={categoriaToEdit}
                    />
                </Modal>
                    
                    {/* modal para ver detalles de la categoría */}

                <Modal
                    isOpen={isModalOpen && !!categoriaToView}
                    onClose={() => {
                        setIsModalOpen(false);
                        setCategoriaToView(undefined);
                    }}
                    title="Detalle de Categoría"
                >
                    {categoriaToView && (
                        <CategoriaDetail
                            categoria={categoriaToView}
                            onClose={() => {
                                setIsModalOpen(false);
                                setCategoriaToView(undefined);
                            }}
                        />
                    )}
                </Modal>
                    
                {/* modal para eliminar categoría */}
                <Modal
                    isOpen={!!categoriaToDelete}
                    onClose={() => setCategoriaToDelete(undefined)}
                    title="Eliminar categoría"
                    >
                    <p className="mb-4">
                        ¿Seguro que querés eliminar{" "}
                        <strong>{categoriaToDelete?.nombre}</strong>?
                    </p>

                    <div className="flex justify-end gap-2">
                        <Button
                        variant="secondary"
                        onClick={() => setCategoriaToDelete(undefined)}>
                        Cancelar
                        </Button>

                        <Button
                        variant="danger"
                        onClick={confirmDelete}
                        >
                        Eliminar
                        </Button>
                    </div>
                </Modal>
                </>
            

            )}

            {section === "productos" && (
    <>
        <div className="flex justify-end">
            <Button
                variant="primary"
                onClick={() => {
                    setProductoToEdit(undefined);
                    setProductoToView(undefined);
                    setIsModalOpen(true);
                }}
            >
                Nuevo Producto
            </Button>
        </div>

        <ProductoTable 
            onEdit={handleEditProducto}
            onDelete={handleDeleteProducto}
            onView={handleViewProducto}
        />

        {/* Modal para crear/editar producto */}
        <Modal
            isOpen={isModalOpen && section === "productos" && !productoToView}
            onClose={() => {
                setIsModalOpen(false);
                setProductoToEdit(undefined);
            }}
            title={
                productoToEdit
                    ? "Editar producto"
                    : "Crear nuevo producto"
            }
        >
            <ProductoForm
                onClose={() => {
                    setIsModalOpen(false);
                    setProductoToEdit(undefined);
                }}
                productoToEdit={productoToEdit}
            />
        </Modal>

        {/* Modal para ver detalle del producto */}
        <Modal
            isOpen={isModalOpen && !!productoToView}
            onClose={() => {
                setIsModalOpen(false);
                setProductoToView(undefined);
            }}
            title="Detalle del Producto"
        >
            {productoToView && (
                <ProductoDetail
                    producto={productoToView}
                    onClose={() => {
                        setIsModalOpen(false);
                        setProductoToView(undefined);
                    }}
                />
            )}
        </Modal>

        {/* Modal para eliminar producto */}
        <Modal
            isOpen={!!productoToDelete}
            onClose={() => setProductoToDelete(undefined)}
            title="Eliminar producto"
        >
            <p className="mb-4">
                ¿Seguro que querés eliminar{" "}
                <strong>{productoToDelete?.nombre}</strong>?
            </p>

            <div className="flex justify-end gap-2">
                <Button
                    variant="secondary"
                    onClick={() => setProductoToDelete(undefined)}
                >
                    Cancelar
                </Button>

                <Button
                    variant="danger"
                    onClick={confirmDeleteProducto}
                >
                    Eliminar
                </Button>
            </div>
        </Modal>
    </>
)}

            {section === "ingredientes" && (
    <>
        <div className="flex justify-end">
            <Button
                variant="primary"
                onClick={() => {
                    setIngredienteToEdit(undefined);
                    setIsModalOpen(true);
                }}
            >
                Nuevo Ingrediente
            </Button>
        </div>

        <IngredienteTable onEdit={handleEditIngrediente} onDelete={handleDeleteIngrediente} />

        <Modal
            isOpen={isModalOpen && section === "ingredientes"}
            onClose={() => {
                setIsModalOpen(false);
                setIngredienteToEdit(undefined);
            }}
            title={
                ingredienteToEdit
                    ? "Editar ingrediente"
                    : "Crear nuevo ingrediente"
            }
        >
            <IngredienteForm
                onClose={() => {
                    setIsModalOpen(false);
                    setIngredienteToEdit(undefined);
                }}
                ingredienteToEdit={ingredienteToEdit}
            />
        </Modal>

        <Modal
            isOpen={!!ingredienteToDelete}
            onClose={() => setIngredienteToDelete(undefined)}
            title="Eliminar ingrediente"
        >
            <p className="mb-4">
                ¿Seguro que querés eliminar{" "}
                <strong>{ingredienteToDelete?.nombre}</strong>?
            </p>

            <div className="flex justify-end gap-2">
                <Button
                    variant="secondary"
                    onClick={() => setIngredienteToDelete(undefined)}
                >
                    Cancelar
                </Button>

                <Button
                    variant="danger"
                    onClick={confirmDeleteIngrediente}
                >
                    Eliminar
                </Button>
            </div>
        </Modal>
    </>
)}
        </div>
        </div>
    )
}
