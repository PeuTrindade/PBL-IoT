import { TbAirConditioningDisabled } from "react-icons/tb";
import { FaPowerOff } from "react-icons/fa";
import { FaTemperatureEmpty } from "react-icons/fa6";
import Dropdown from "./Dropdown";
import { useState } from "react";
import { FiClock } from "react-icons/fi";

function List({ items, brokerIP }) {
    const [selectedDevice, setSelectedDevice] = useState()
    const [selectedDeviceIndex, setSelectedDeviceIndex] = useState()

    const onClickModeButton = async (address, mode) => {
        try {
            await fetch(`http://${brokerIP}:5976//change_mode/${address}/${mode}`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
        } catch (error) {
            console.info(error)
        }
    }

    const updateTemperature = async (address, temperature) => {
        try {
            await fetch(`http://${brokerIP}:5976//change_temperature/${address}/${temperature}`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
        } catch (error) {
            console.info(error)
        }
    }

    function formatDate(dateString) {
        let date = new Date(dateString);
    
        let day = date.getDate();
        let month = date.getMonth() + 1;
        let hour = date.getHours();
        let minutes = date.getMinutes();
    
        day = day < 10 ? '0' + day : day;
        month = month < 10 ? '0' + month : month;
        hour = hour < 10 ? '0' + hour : hour;
        minutes = minutes < 10 ? '0' + minutes : minutes;
    
        let formattedDate = `${day}/${month} - ${hour}:${minutes}`;
    
        return formattedDate;
    }

    console.log(items)

    return (
        <ul className="list-group mt-3">
            {items && items.map((item, index) => {
                return (
                    <li key={index} className="d-flex align-items-center justify-content-between list-group-item">
                        <span style={{ gap: '10px'}} className="d-flex">
                          <TbAirConditioningDisabled fontSize={25} />
                          {item.deviceName}  
                        </span>
                        <span style={{ gap: '24px'}} className="d-flex align-items-center">
                          <FaPowerOff color={item.on ? 'green': 'red'} onClick={() => onClickModeButton(item.id, item.on ? 'off': 'on')} cursor='pointer' fontSize={18} />

                          <span style={{ gap: '1px'}} className="d-flex align-items-center">
                            <FaTemperatureEmpty fontSize={18} />
                            {`${item.temperature}°C`}
                          </span>

                          <Dropdown items={[<li style={{ cursor: 'pointer'}} onClick={() => {
                            setSelectedDevice(item)
                          }} className="dropdown-item" data-bs-toggle="modal" data-bs-target="#staticBackdrop">Editar temperatura</li>,<li style={{ cursor: 'pointer'}} onClick={() => {
                            setSelectedDeviceIndex(index)
                          }} className="dropdown-item" data-bs-toggle="offcanvas" data-bs-target="#offcanvasScrolling" aria-controls="offcanvasScrolling">Exibir logs</li>]} />
                        </span>
                    </li>
                )
            })}
            <div className="modal fade" id="staticBackdrop" data-bs-backdrop="static" data-bs-keyboard="false" tabIndex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
                <div className="modal-dialog">
                    <div className="modal-content">
                    <div className="modal-header">
                        <h1 className="modal-title fs-5" id="staticBackdropLabel">{selectedDevice?.deviceName}</h1>
                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div className="modal-body">
                        <form onSubmit={(e) => e.preventDefault()}>
                            <input id="updateTemperatureInput" placeholder="Insira uma nova temperatura" className="form-control" type="number" />
                        </form>
                    </div>
                    <div className="modal-footer">
                        <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                        <button type="button" onClick={() => {
                            const temperature = document.getElementById('updateTemperatureInput').value

                            updateTemperature(selectedDevice?.id,temperature)

                            document.getElementById('updateTemperatureInput').value = undefined
                        }} data-bs-dismiss="modal" className="btn btn-primary">Salvar</button>
                    </div>
                    </div>
                </div>
            </div>

            <div className="offcanvas offcanvas-start" data-bs-scroll="true" data-bs-backdrop="false" tabindex="-1" id="offcanvasScrolling" aria-labelledby="offcanvasScrollingLabel">
                <div className="offcanvas-header">
                    <h5 className="offcanvas-title" id="offcanvasScrollingLabel">{items[selectedDeviceIndex]?.deviceName} - logs</h5>
                    <button type="button" className="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
                </div>
                <div className="offcanvas-body">
                <ul className="list-group">
                    {items[selectedDeviceIndex]?.logs && items[selectedDeviceIndex]?.logs.slice().reverse().map((log, key) => {
                        return (
                            <li style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start', gap: '6px'}} key={key} className="list-group-item">
                                <span style={{ display: 'flex',alignItems: 'center', gap: '6px'}} className="badge text-bg-primary"><FiClock /> {formatDate(log.date)}</span>
                                {log.message}
                            </li>
                        )
                    })}
                </ul>
                </div>
            </div>
        </ul>
    )
}


export default List;