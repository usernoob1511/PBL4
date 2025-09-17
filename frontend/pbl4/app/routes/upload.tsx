import React, { useState } from "react";

const UploadPage = () => {
  const [file, setFile] = useState<File | null>(null);
  const [protocol, setProtocol] = useState("ftp");
  const [message, setMessage] = useState("");

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("Vui lòng chọn một file để tải lên.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("protocol", protocol);

    try {
      // Gọi API backend để upload
      const response = await fetch("http://localhost:8000/api/upload/", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();
      if (response.ok) {
        setMessage(
          `Tải lên thành công file: ${result.filename} qua ${result.protocol.toUpperCase()}`
        );
      } else {
        setMessage(`Lỗi: ${result.msg || "Không thể tải file lên."}`);
      }
    } catch (error) {
      setMessage("Đã xảy ra lỗi khi kết nối đến server.");
      console.error("Upload error:", error);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Upload File</h1>
      <div className="mb-4">
        <input
          type="file"
          onChange={handleFileChange}
          className="border p-2 rounded w-full"
        />
      </div>
      <div className="mb-4">
        <label className="mr-2">Giao thức:</label>
        <select
          value={protocol}
          onChange={(e) => setProtocol(e.target.value)}
          className="border p-2 rounded"
        >
          <option value="ftp">FTP</option>
          <option value="tftp">TFTP</option>
        </select>
      </div>
      <button
        onClick={handleUpload}
        className="bg-blue-500 text-white px-4 py-2 rounded"
      >
        Upload
      </button>
      {message && (
        <p className="mt-4 text-gray-700 dark:text-gray-200">{message}</p>
      )}
    </div>
  );
};

export default UploadPage;
