function Navbar() {
    return (
        <nav className="navbar bg-primary">
            <div className="container-fluid">
                <a className="navbar-brand text-white" href="/">Air manager</a>
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link active text-white" aria-current="page" href="/">Meus ar condicionados</a>
                    </li>
                </ul>
            </div>
        </nav>
    )
}


export default Navbar;