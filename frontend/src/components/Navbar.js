function Navbar() {
    return (
        <nav className="navbar bg-primary">
            <div className="container-fluid">
                <a className="navbar-brand text-white" href="/">Air manager</a>
                <ul className="navbar-nav">
                    <li className="nav-item">
                        <a className="nav-link active text-white" aria-current="page" href="/">Meus ar condicionados</a>
                    </li>
                </ul>
            </div>
        </nav>
    )
}


export default Navbar;