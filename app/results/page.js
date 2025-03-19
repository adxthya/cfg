import { Suspense } from "react";
import ResultsClient from "@/components/ResultsClient";

export default function ResultsPage() {
  return (
    <Suspense
      fallback={<p className="text-center text-gray-600">Loading...</p>}
    >
      <ResultsClient />
    </Suspense>
  );
}
