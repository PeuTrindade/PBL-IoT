import { IoEllipsisVertical } from "react-icons/io5";

function Dropdown({ items }) {
    return (
        <div className="btn-group">
            <button className="btn btn-primary btn-sm dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                <IoEllipsisVertical />
            </button>
            <ul className="dropdown-menu">
                {items.length > 0 && items.map((item, key) => {
                    return item
                })}
            </ul>
        </div>
    ) 
}

export default Dropdown