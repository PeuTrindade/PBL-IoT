import { useEffect, useState } from "react";
import List from "./components/List";
import Navbar from "./components/Navbar";

function App() {
  const [devices, setDevices] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000//devices');

        if (response.ok) {
          const result = await response.json();
          const resultValues = Object.values(result)

          const formattedResults = resultValues.map((d) => ({
            id: d.addressInfo[1],
            deviceName: d.sentMessages.deviceName,
            temperature: d.sentMessages.temperature,
            on: d.sentMessages.on,
            logs: d.sentMessages.logs
          }))

          setDevices(formattedResults)
        }
      } catch (error) {
        console.info(error);
      }
    };

    fetchData();

    const intervalId = setInterval(fetchData, 100);

    return () => clearInterval(intervalId);
  }, []);

  return (
    <>
      <Navbar />
      <div style={{ marginTop: '60px'}} className='container col-6'>
        <div style={{ display: 'flex', gap: '10px', alignItems: 'center'}}>
          <h3>Meus ar condicionados</h3>
          <span class="badge text-bg-primary">{devices.length}</span>
        </div>
        {devices.length > 0 ? <List items={devices} /> : <p>Não há dispositivos conectados no momento!😓</p>}
      </div>
    </>
  );
}

export default App;
