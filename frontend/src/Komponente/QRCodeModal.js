import React from "react";
import Modal from "react-modal";
import QRCode from "qrcode.react";

const QRCodeModal = ({ isOpen, onRequestClose, qrcodeData }) => {
  return (
    <Modal
      isOpen={isOpen}
      onRequestClose={onRequestClose}
      contentLabel="QR Code Modal"
      style={{
        overlay: {
          backgroundColor: "rgba(0, 0, 0, 0.5)",
        },
        content: {
          width: "50%",
          height: "50%",
          margin: "auto",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
        },
      }}
    >
      <QRCode value={qrcodeData} size={256} /> {/* Adjust the size as needed */}
    </Modal>
  );
};

export default QRCodeModal;
