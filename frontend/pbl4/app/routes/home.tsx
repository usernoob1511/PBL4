import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Linux File Transfer System</h1>
      <div className="space-y-4">
        <Link
          to="/upload"
          className="block bg-blue-500 text-white px-4 py-2 rounded text-center"
        >
          Upload File
        </Link>
        <Link
          to="/download"
          className="block bg-green-500 text-white px-4 py-2 rounded text-center"
        >
          Download File
        </Link>
      </div>
    </div>
  );
}