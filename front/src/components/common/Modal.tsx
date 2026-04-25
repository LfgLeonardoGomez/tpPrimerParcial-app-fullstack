    import type { ReactNode } from "react"

    interface ModalProps {
    isOpen: boolean
    onClose: () => void
    title: string
    children: ReactNode
    }

    export const Modal = ({
    isOpen,
    onClose,
    title,
    children,
    }: ModalProps) => {
    if (!isOpen) return null

    return (
        <div className="fixed inset-0 flex items-center justify-center bg-black/50 z-50">
        <div className="bg-white rounded-xl shadow-lg w-full max-w-lg p-6 relative">
            <button
            onClick={onClose}
            className="absolute top-4 right-4 text-gray-500 hover:text-black"
            >
            ✕
            </button>

            <h2 className="text-xl font-semibold mb-4">
            {title}
            </h2>

            <div>
            {children}
            </div>
        </div>
        </div>
    )
    }