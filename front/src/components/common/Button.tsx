import type {ReactNode} from 'react';

type ButtonVariants = 'primary' | 'danger' | 'secondary';

const variants = {
    primary: "bg-blue-500 text-white",
    danger: "bg-red-500 text-white",
    secondary: "bg-gray-200 text-black",
}
interface ButtonProps {
    children: ReactNode;
    onClick?: () => void;
    type?: 'button' | 'submit' | 'reset';
    disabled?: boolean;
    variant?: ButtonVariants;
    className?: string;
}

export const Button = ({children, onClick, type = 'button', disabled = false, variant = 'primary', className = ''}: ButtonProps) => {
    return (
        <button
            type={type}
            onClick={onClick}
            disabled={disabled}
            className={`
                    px-4 py-2
                    rounded-lg
                    font-medium
                    transition
                    ${variants[variant]}
                    ${className}
                `}
        >
            {children}
        </button>
    );
}

