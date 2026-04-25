import type {ReactNode} from "react"

interface TableProps {
    headers: string[]
    children: ReactNode
}

export const Table = ({headers, children}: TableProps) => {
    return (
    <div className="overflow-x-auto rounded-xl border border-gray-200 shadow-sm">
        <table className="w-full border-collapse">
            <thead className="bg-gray-100">
                <tr>
                {headers.map((header, index) => (
                    <th
                        key={index}
                        className="px-4 py-3 text-left font-semibold text-sm"
                    >
                    {header}
                </th>
            ))}
                </tr>
            </thead>

        <tbody>
            {children}
        </tbody>
        </table>
    </div>
    )
}