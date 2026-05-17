import React, { useState } from 'react';

interface DXFItem {
  [key: string]: string;
}

interface ExtractionResponse {
  filename: string;
  count: number;
  items: DXFItem[];
}

const DXFUpload: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<ExtractionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setLoading(true);
    setError(null);
    setData(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      // Use standard endpoint from the integration guide
      const response = await fetch('/api/v1/dxf/extract', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to extract data');
      }

      const result: ExtractionResponse = await response.json();
      setData(result);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Compute unique keys from all items to ensure no data is hidden
  const allKeys = data
    ? Array.from(new Set(data.items.flatMap(item => Object.keys(item))))
    : [];

  return (
    <div className="p-6 max-w-6xl mx-auto bg-white rounded-xl shadow-md space-y-4">
      <div className="flex flex-col space-y-2 text-center sm:text-left">
        <h2 className="text-2xl font-bold text-gray-800 tracking-tight">AutoCAD DXF Data Extraction</h2>
        <p className="text-sm text-gray-500">
          Upload your .dxf drawings to automatically extract block attributes for Bill of Quantities (BOQ) or Bar Bending Schedules (BBS).
        </p>
      </div>

      <div className="flex flex-col sm:flex-row items-center justify-between p-4 border-2 border-dashed border-gray-200 rounded-lg bg-gray-50 gap-4">
        <label className="cursor-pointer">
          <span className="bg-blue-600 text-white px-4 py-2 rounded-md font-medium text-sm hover:bg-blue-700 transition-colors">
            Select DXF Drawing
          </span>
          <input
            type="file"
            accept=".dxf"
            onChange={handleFileUpload}
            disabled={loading}
            className="hidden"
          />
        </label>
        {loading && (
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
            <span className="text-blue-600 font-medium text-sm">Processing drawing...</span>
          </div>
        )}
      </div>

      {error && (
        <div className="p-4 bg-red-50 border-l-4 border-red-500 text-red-700 rounded-md text-sm shadow-sm">
          <strong>Extraction Error:</strong> {error}
        </div>
      )}

      {data && (
        <div className="mt-8 space-y-4 animate-in fade-in duration-500">
          <div className="flex flex-col sm:flex-row sm:justify-between sm:items-end border-b pb-3 gap-2">
            <div>
              <h3 className="text-lg font-semibold text-gray-800">Extracted Components</h3>
              <p className="text-xs text-gray-400">Successfully identified {data.count} items in "{data.filename}"</p>
            </div>
          </div>

          <div className="overflow-x-auto border rounded-xl shadow-sm">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  {allKeys.map((key) => (
                    <th
                      key={key}
                      className="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-widest whitespace-nowrap"
                    >
                      {key}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-100">
                {data.items.map((item, index) => (
                  <tr key={index} className="hover:bg-blue-50/30 transition-colors">
                    {allKeys.map((key) => (
                      <td key={key} className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                        {item[key] || <span className="text-gray-300 italic">N/A</span>}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="flex justify-end pt-4">
            <button
              onClick={() => alert('Logic to integrate with BOQ/BBS state would execute here.')}
              className="px-6 py-2.5 bg-green-600 text-white rounded-lg text-sm font-semibold hover:bg-green-700 shadow-md transform active:scale-95 transition-all"
            >
              Sync to Project Quantities
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default DXFUpload;
