import { useState } from "react";
import api from "../services/api";

export default function UploadReceipt() {

  const [file, setFile] =
    useState();

  const [result, setResult] =
    useState();

  async function upload() {

    const formData =
      new FormData();

    formData.append(
      "file",
      file
    );

    const response =
      await api.post(
        "/receipts/process",
        formData
      );

    setResult(
      response.data
    );
  }

  return (
    <div>

      <input
        type="file"
        onChange={e =>
          setFile(
            e.target.files[0]
          )
        }
      />

      <button
        onClick={upload}
      >
        Upload
      </button>

      {
        result &&
        <pre>
          {
            JSON.stringify(
              result,
              null,
              2
            )
          }
        </pre>
      }

    </div>
  );
}