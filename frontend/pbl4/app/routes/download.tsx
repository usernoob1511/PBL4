import { useState } from "react";

export default function DownloadPage() {
  const [fileName, setFileName] = useState("");
  const [protocol, setProtocol] = useState("ftp");
  const [message, setMessage] = useState("");

  const handleDownload = async () => {
    if (!fileName) {
      setMessage("Vui lòng nhập tên file để tải xuống.");
      return;
    }

    try {
      // Gọi API backend để download
      const response = await fetch(
        `http://localhost:8000/api/download/?filename=${encodeURIComponent(fileName)}&protocol=${protocol}`,
        {
          method: "GET", // <-- THÊM: Chỉ định rõ phương thức là GET
        }
      );

      if (response.ok) {
        // Tạo một URL tạm thời từ blob và kích hoạt download
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = fileName;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
        setMessage("Tải xuống thành công!");
      } else {
        const result = await response.json();
        setMessage(`Lỗi: ${result.msg || 'Không thể tải file.'}`);
      }
    } catch (error) {
      setMessage("Đã xảy ra lỗi khi kết nối đến server.");
      console.error("Download error:", error);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Download File</h1>
      <div className="mb-4">
        <input
          type="text"
          placeholder="Nhập tên file"
          value={fileName}
          onChange={(e) => setFileName(e.target.value)}
          className="border p-2 rounded w-full"
        />
      </div>
      <div className="mb-4">
        <label className="mr-2">Giao thức:</label>
        <select value={protocol} onChange={(e) => setProtocol(e.target.value)} className="border p-2 rounded">
          <option value="ftp">FTP</option>
          <option value="tftp">TFTP</option>
        </select>
      </div>
      <button onClick={handleDownload} className="bg-green-500 text-white px-4 py-2 rounded">
        Download
      </button>
      {message && <p className="mt-4 text-gray-700 dark:text-gray-200">{message}</p>}
    </div>
  );
}
