import { useEffect, useState } from "react";
import List from "./components/List";
import Navbar from "./components/Navbar";
import { IoMdSettings } from "react-icons/io";

function App() {
  const [devices, setDevices] = useState([]);
  const [brokerIP, setBrokerIP] = useState('')

  useEffect(() => {
    if (brokerIP) {
      const fetchData = async () => {
        try {
          const response = await fetch(`http://${brokerIP}:5976//devices`);
  
          if (response.ok) {
            const result = await response.json();
            const resultValuesFormatted = Object.entries(result).map(([key, value]) => ({
              id: key,
              ...value
            }))
  
            setDevices(resultValuesFormatted)
          }
        } catch (error) {
          console.info(error);
        }
      };
  
      fetchData();
  
      const intervalId = setInterval(fetchData, 1000);
  
      return () => clearInterval(intervalId);
    }
  }, [brokerIP]);

  return (
    <>
      <Navbar />
      <div style={{ marginTop: '60px'}} className='container col-6'>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
          <div style={{ display: 'flex', gap: '10px', alignItems: 'center'}}>
            <h3>Meus ar condicionados</h3>
            <span className="badge text-bg-primary">{devices.length}</span>
          </div>
          <button data-bs-toggle="modal" data-bs-target="#connectionModal" className="d-flex align-items-center p-2 justify-content-center btn btn-primary btn-sm cursor-pointer"><IoMdSettings /></button>
        </div>
        {brokerIP ? (devices.length > 0 ? <List brokerIP={brokerIP} items={devices} /> : <p>Não há dispositivos conectados no momento!😓</p>) : <p className="text-danger">Nenhum broker conectado!</p>}
      </div>

      <div className="modal fade" id="connectionModal" data-bs-backdrop="static" data-bs-keyboard="false" tabIndex="-1" aria-labelledby="connectionModalLabel" aria-hidden="true">
          <div className="modal-dialog">
              <div className="modal-content">
              <div className="modal-header">
                  <h1 className="modal-title fs-5" id="connectionModalLabel">Configurações</h1>
                  <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div className="modal-body">
                  <form onSubmit={(e) => e.preventDefault()}>
                      <input id="brokerIP" placeholder="Insira o IP da máquina da API" defaultValue={brokerIP} className="form-control" />
                  </form>
              </div>
              <div className="modal-footer">
                  <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                  <button type="button" onClick={() => {
                      const ip = document.getElementById('brokerIP').value

                      setBrokerIP(ip)
                  }} data-bs-dismiss="modal" className="btn btn-primary">Salvar</button>
              </div>
              </div>
          </div>
        </div>
    </>
  );
}

export default App;
