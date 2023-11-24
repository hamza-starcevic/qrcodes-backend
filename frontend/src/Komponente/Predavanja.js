import React, { useState } from "react";
import { Link } from "react-router-dom";
import Modal from "react-modal";
import QRCodeModal from "./QRCodeModal";
import QRCode from "qrcode.react";

const Predavanja = () => {
  const [inputData, setInputData] = useState({
    predmet: "",
    title: "",
    description: "",
  });

  const [tableData, setTableData] = useState([]);
  const [qrcodeData, setQRCodeData] = useState(null);
  const [isQRCodeModalOpen, setQRCodeModalOpen] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setInputData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleCreatePredavanje = () => {
    try {
      setTableData((prevTableData) => [
        ...prevTableData,
        {
          naziv: inputData.title,
          opis: inputData.description,
          predmet: inputData.predmet,
        },
      ]);
      setInputData({
        predmet: "",
        title: "",
        description: "",
      });
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleCreateQRCode = (rowData) => {
    setQRCodeData(rowData.naziv);
    setQRCodeModalOpen(true);
  };

  const closeQRCodeModal = () => {
    setQRCodeModalOpen(false);
    setQRCodeData(null);
  };

  return (
    <div className="container">
      <div className="Predmet wrapper-4">
        <input type="text" name="predmet" value={inputData.predmet} onChange={handleInputChange} placeholder="Predmet" />
        <input type="text" name="title" value={inputData.title} onChange={handleInputChange} placeholder="Title" />
        <textarea name="description" value={inputData.description} onChange={handleInputChange} placeholder="Description" />
        <button onClick={handleCreatePredavanje}>Kreiraj Predavanje</button>
      </div>
      <h1 className="H1-title">Predavanja</h1>
      <div className="predmet-card">
        <table>
          <thead>
            <tr>
              <th>Naziv</th>
              <th>Opis</th>
              <th>Predmet</th>
              
            </tr>
          </thead>
          <tbody>
            {tableData.map((row, index) => (
              <tr key={index}>
                <td>{row.naziv}</td>
                <td>{row.opis}</td>
                <td>{row.predmet}</td>
                
                  <button onClick={() => handleCreateQRCode(row)}>Kreiraj QR kod</button>
                  <Link to="/prisustvo">
                    <button>Prisustvo</button>
                  </Link>
              
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <QRCodeModal isOpen={isQRCodeModalOpen} onRequestClose={closeQRCodeModal} qrcodeData={qrcodeData} />
    </div>
  );
};

export default Predavanja;
