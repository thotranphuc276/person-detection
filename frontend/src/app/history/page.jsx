'use client';

import Link from 'next/link';
import HistoryTable from '@/components/HistoryTable';

export default function HistoryPage() {
    return (
        <main className="max-w-6xl mx-auto p-4">
            <div className="mb-6 flex items-center justify-between">
                <h1 className="text-3xl font-bold">Detection History</h1>
                <Link
                    href="/"
                    className="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300"
                >
                    Back to Upload
                </Link>
            </div>

            <HistoryTable />
        </main>
    );
}