import Image from "next/image";
import Link from "next/link";

export default function Home() {
  return (
    <div className="h-screen flex flex-col items-center justify-center bg-[#e5c6e4] px-6">
      {/* Title */}
      <h1 className="text-4xl font-bold text-center text-gray-900 mb-6">
        CTG Data Management System
      </h1>

      {/* Card Container */}
      <div className="w-full max-w-3xl bg-white shadow-lg rounded-xl p-8 border border-gray-300">
        <p className="text-center text-2xl font-semibold text-gray-800 mb-6">
          Choose Input Method
        </p>

        {/* Input Method Cards */}

        <div className="flex flex-col sm:flex-row justify-center gap-10">
          {/* Upload Image Card */}
          <Link href="/upload">
            <div className="flex flex-col items-center justify-center bg-gray-100 p-6 rounded-lg w-80 h-80 cursor-pointer hover:shadow-lg hover:-translate-y-2 transition">
              <Image
                src="/upload.png"
                width={100}
                height={100}
                alt="Upload CTG waveform"
                className="mb-4"
              />
              <p className="font-semibold text-xl text-gray-900 mb-2 text-center">
                Upload Images of Waveform
              </p>
              <p className="text-center text-gray-700">
                Upload CTG waveform images for automated processing.
              </p>
            </div>
          </Link>

          {/* Manual Entry Card */}
          <Link href="/manual">
            <div className="flex flex-col items-center justify-center bg-gray-100 p-6 rounded-lg w-80 h-80 cursor-pointer hover:shadow-lg hover:-translate-y-2 transition">
              <Image
                src="/upload.png"
                width={100}
                height={100}
                alt="Manual Data Entry"
                className="mb-4"
              />
              <p className="font-semibold text-xl text-gray-900 mb-2 text-center">
                Manual Entries
              </p>
              <p className="text-center text-gray-700">
                Manually enter CTG data values.
              </p>
            </div>
          </Link>
        </div>
      </div>
    </div>
  );
}
