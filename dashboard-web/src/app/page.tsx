"use client";

import { useEffect, useState } from "react";

interface SummaryData {
  ok: boolean;
  total_transaksi: number;
  omzet: number;
  uang_masuk: number;
  piutang: number;
  status_count: {
    lunas: number;
    dicicil: number;
    hutang: number;
    lain: number;
  };
}

interface TimeseriesData {
  ok: boolean;
  days: number;
  labels: string[];
  omzet: number[];
  uang_masuk: number[];
  piutang: number[];
  count: number[];
}

interface TransactionItem {
  id: number;
  tanggal: string;
  nama_pelanggan: string;
  barang: string;
  jumlah_satuan: number;
  harga: number;
  total: number;
  status: string;
  metode_pembayaran: string;
  tagihan: number;
  uang_masuk: number;
}

interface TopCustomer {
  nama: string;
  omzet: number;
  piutang: number;
  count: number;
}

// --- Konfigurasi URL API Backend ---
// URL backend di Render (production)
const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "https://aw-bot-backend.onrender.com";

export default function DashboardPage() {
  const [days, setDays] = useState<number>(30);
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const [summary, setSummary] = useState<SummaryData | null>(null);
  const [timeseries, setTimeseries] = useState<TimeseriesData | null>(null);
  const [recentTrx, setRecentTrx] = useState<TransactionItem[]>([]);
  const [topCustomers, setTopCustomers] = useState<TopCustomer[]>([]);

  const formatCurrency = (val: number) => {
    return new Intl.NumberFormat("id-ID", {
      style: "currency",
      currency: "IDR",
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(val);
  };

  // --- Fetch Data dari API ---
  const fetchData = async () => {
    setLoading(true);
    setError(null);

    try {
      // 1. Fetch Summary
      const summaryRes = await fetch(
        `${API_BASE_URL}/api/dashboard/summary?days=${days}`
      );
      const summaryJson = await summaryRes.json();
      if (summaryJson.ok) setSummary(summaryJson);

      // 2. Fetch Timeseries
      const timeseriesRes = await fetch(
        `${API_BASE_URL}/api/dashboard/timeseries?days=${days}`
      );
      const timeseriesJson = await timeseriesRes.json();
      if (timeseriesJson.ok) setTimeseries(timeseriesJson);

      // 3. Fetch Recent Transactions
      const recentRes = await fetch(
        `${API_BASE_URL}/api/dashboard/recent?days=${days}&q=${searchQuery}`
      );
      const recentJson = await recentRes.json();
      if (recentJson.ok) setRecentTrx(recentJson.items || []);

      // 4. Fetch Top Customers
      const topCustRes = await fetch(
        `${API_BASE_URL}/api/dashboard/top-customers?days=${days}`
      );
      const topCustJson = await topCustRes.json();
      if (topCustJson.ok) setTopCustomers(topCustJson.items || []);

    } catch (err: any) {
      console.error("Fetch error:", err);
      setError(
        "Gagal terhubung ke backend. Pastikan backend berjalan dan URL API benar!"
      );
      
      // --- Fallback ke data dummy jika gagal fetch ---
      const dummySummary: SummaryData = {
        ok: true,
        total_transaksi: 128,
        omzet: 15750000,
        uang_masuk: 12500000,
        piutang: 3250000,
        status_count: {
          lunas: 95,
          dicicil: 20,
          hutang: 10,
          lain: 3
        }
      };
      const dummyTimeseries: TimeseriesData = {
        ok: true,
        days: 30,
        labels: ["1 Jan", "5 Jan", "10 Jan", "15 Jan", "20 Jan", "25 Jan", "30 Jan"],
        omzet: [500000, 750000, 600000, 900000, 800000, 1200000, 1000000],
        uang_masuk: [400000, 600000, 500000, 750000, 650000, 1000000, 850000],
        piutang: [100000, 150000, 100000, 150000, 150000, 200000, 150000],
        count: [5, 8, 6, 10, 9, 12, 10]
      };
      const dummyRecentTrx: TransactionItem[] = [
        { id: 1, tanggal: "2024-01-30", nama_pelanggan: "Andi", barang: "Kemeja", jumlah_satuan: 2, harga: 150000, total: 300000, status: "Lunas", metode_pembayaran: "Transfer", tagihan: 0, uang_masuk: 300000 },
        { id: 2, tanggal: "2024-01-29", nama_pelanggan: "Budi", barang: "Celana", jumlah_satuan: 1, harga: 200000, total: 200000, status: "Dicicil", metode_pembayaran: "Cash", tagihan: 100000, uang_masuk: 100000 },
        { id: 3, tanggal: "2024-01-28", nama_pelanggan: "Citra", barang: "Sepatu", jumlah_satuan: 1, harga: 350000, total: 350000, status: "Lunas", metode_pembayaran: "QRIS", tagihan: 0, uang_masuk: 350000 },
      ];
      const dummyTopCustomers: TopCustomer[] = [
        { nama: "Andi", omzet: 2500000, piutang: 0, count: 12 },
        { nama: "Budi", omzet: 1800000, piutang: 500000, count: 8 },
        { nama: "Citra", omzet: 1500000, piutang: 0, count: 10 },
      ];
      setSummary(dummySummary);
      setTimeseries(dummyTimeseries);
      setRecentTrx(dummyRecentTrx);
      setTopCustomers(dummyTopCustomers);
      
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [days, searchQuery]);

  const renderChart = () => {
    if (!timeseries || !timeseries.labels.length) return null;

    const width = 800;
    const height = 250;
    const padding = 45;
    const chartWidth = width - padding * 2;
    const chartHeight = height - padding * 2;

    const maxVal = Math.max(
      ...timeseries.omzet,
      ...timeseries.uang_masuk,
      ...timeseries.piutang,
      100000
    );

    const getX = (index: number) => {
      if (timeseries.labels.length <= 1) return padding + chartWidth / 2;
      return padding + (index / (timeseries.labels.length - 1)) * chartWidth;
    };

    const getY = (val: number) => {
      return height - padding - (val / maxVal) * chartHeight;
    };

    const pointsOmzet = timeseries.omzet.map((v, i) => `${getX(i)},${getY(v)}`).join(" ");
    const pointsUangMasuk = timeseries.uang_masuk.map((v, i) => `${getX(i)},${getY(v)}`).join(" ");

    return (
      <svg viewBox={`0 0 ${width} ${height}`} className="w-full h-auto text-zinc-600">
        {/* Grid lines */}
        {[0, 0.25, 0.5, 0.75, 1].map((ratio, i) => {
          const y = height - padding - ratio * chartHeight;
          const val = ratio * maxVal;
          return (
            <g key={i}>
              <line
                x1={padding}
                y1={y}
                x2={width - padding}
                y2={y}
                stroke="#e4e4e7"
                strokeDasharray="4 4"
              />
              <text x={padding - 10} y={y + 4} textAnchor="end" className="text-[10px] fill-zinc-400 font-medium">
                {val >= 1000000 ? `${(val / 1000000).toFixed(1)}M` : val >= 1000 ? `${(val / 1000).toFixed(0)}k` : val}
              </text>
            </g>
          );
        })}

        {/* X Axis Labels */}
        {timeseries.labels.map((label, i) => {
          if (timeseries.labels.length > 15 && i % 2 !== 0) return null;
          return (
            <text
              key={i}
              x={getX(i)}
              y={height - padding + 18}
              textAnchor="middle"
              className="text-[10px] fill-zinc-400 font-medium"
            >
              {label}
            </text>
          );
        })}

        {/* Omzet Area & Line */}
        <path
          d={`M ${getX(0)} ${height - padding} L ${pointsOmzet} L ${getX(timeseries.omzet.length - 1)} ${height - padding} Z`}
          fill="url(#gradOmzet)"
          opacity="0.1"
        />
        <polyline
          fill="none"
          stroke="#6366f1"
          strokeWidth="3"
          strokeLinecap="round"
          strokeLinejoin="round"
          points={pointsOmzet}
        />

        {/* Uang Masuk Area & Line */}
        <path
          d={`M ${getX(0)} ${height - padding} L ${pointsUangMasuk} L ${getX(timeseries.uang_masuk.length - 1)} ${height - padding} Z`}
          fill="url(#gradUang)"
          opacity="0.1"
        />
        <polyline
          fill="none"
          stroke="#10b981"
          strokeWidth="3"
          strokeLinecap="round"
          strokeLinejoin="round"
          points={pointsUangMasuk}
        />

        {/* Gradients */}
        <defs>
          <linearGradient id="gradOmzet" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#6366f1" />
            <stop offset="100%" stopColor="#6366f1" stopOpacity="0" />
          </linearGradient>
          <linearGradient id="gradUang" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#10b981" />
            <stop offset="100%" stopColor="#10b981" stopOpacity="0" />
          </linearGradient>
        </defs>
      </svg>
    );
  };

  return (
    <div className="min-h-screen bg-slate-50 text-zinc-800 font-sans selection:bg-violet-100 overflow-x-hidden">
      {/* Header */}
      <header className="border-b border-zinc-200 bg-white/95 backdrop-blur sticky top-0 z-50 shadow-sm w-full">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 sm:py-0 sm:h-16 flex flex-col sm:flex-row items-center justify-between gap-3 sm:gap-4 w-full">
          <div className="flex items-center gap-3 self-start sm:self-auto">
            <div className="relative w-10 h-10 rounded-xl shadow-md shadow-indigo-500/20 border border-indigo-200/50 bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center text-white font-bold text-lg">
              AW
            </div>
            <div>
              <span className="font-extrabold text-lg tracking-tight bg-gradient-to-r from-indigo-600 to-violet-600 bg-clip-text text-transparent">
                AW Production
              </span>
              <span className="text-zinc-400 text-xs block font-mono font-semibold tracking-widest">DASHBOARD SYSTEM</span>
            </div>
          </div>

          <div className="flex items-center gap-2 w-full sm:w-auto justify-between sm:justify-end">
            <div className="flex bg-zinc-100 rounded-lg p-0.5 border border-zinc-200 flex-1 sm:flex-none">
              {[7, 14, 30, 90].map((d) => (
                <button
                  key={d}
                  onClick={() => setDays(d)}
                  className={`flex-1 sm:flex-none text-center px-2.5 py-1 text-xs font-semibold rounded-md transition-all cursor-pointer ${
                    days === d 
                      ? "bg-white text-indigo-600 shadow-sm" 
                      : "text-zinc-500 hover:text-zinc-800"
                  }`}
                >
                  {d}D
                </button>
              ))}
            </div>

            <button
              onClick={() => fetchData()}
              disabled={loading}
              className="bg-indigo-50 hover:bg-indigo-100 border border-indigo-200/60 rounded-lg px-3 py-1.5 text-indigo-600 font-bold text-xs transition-all shadow-sm flex items-center gap-1 active:scale-95 disabled:opacity-50"
              title="Refresh Data"
            >
              <svg 
                className={`w-3.5 h-3.5 transition-transform duration-700 ${loading ? 'animate-spin' : 'hover:rotate-180'}`} 
                fill="none" 
                viewBox="0 0 24 24" 
                stroke="currentColor"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M4 4v5h.582m15.356 2A8.001 8.001 0 1121.21 8H17" />
              </svg>
              <span>Refresh</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 w-full overflow-hidden">
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-xl p-4 flex gap-3 items-start w-full">
            <svg className="w-5 h-5 text-red-500 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <div>
              <h3 className="text-red-700 font-semibold text-sm">Gagal memuat data</h3>
              <p className="text-red-600/80 text-xs mt-1 font-mono">{error}</p>
            </div>
          </div>
        )}

        {loading && !summary && (
          <div className="flex flex-col items-center justify-center py-32 gap-3">
            <div className="w-10 h-10 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
            <span className="text-zinc-400 text-sm font-medium">Memuat data dari server...</span>
          </div>
        )}

        {summary && (
          <div className="space-y-8 animate-in fade-in duration-300">
            {/* Summary Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {/* Card Omzet */}
              <div className="bg-white border border-zinc-200 rounded-2xl p-5 relative overflow-hidden group shadow-sm hover:shadow-md transition-shadow">
                <div className="absolute top-0 right-0 w-24 h-24 bg-indigo-50 rounded-full blur-2xl group-hover:bg-indigo-100 transition-all duration-300"></div>
                <span className="text-zinc-400 text-xs font-semibold uppercase tracking-wider">Total Omzet</span>
                <h2 className="text-2xl sm:text-3xl font-extrabold text-zinc-900 mt-2 tracking-tight">
                  {formatCurrency(summary.omzet)}
                </h2>
                <div className="flex items-center gap-1.5 mt-3 text-indigo-600 text-xs font-semibold">
                  <span className="w-2 h-2 rounded-full bg-indigo-500"></span>
                  Pendapatan kotor
                </div>
              </div>

              {/* Card Uang Masuk */}
              <div className="bg-white border border-zinc-200 rounded-2xl p-5 relative overflow-hidden group shadow-sm hover:shadow-md transition-shadow">
                <div className="absolute top-0 right-0 w-24 h-24 bg-emerald-50 rounded-full blur-2xl group-hover:bg-emerald-100 transition-all duration-300"></div>
                <span className="text-zinc-400 text-xs font-semibold uppercase tracking-wider">Uang Masuk</span>
                <h2 className="text-2xl sm:text-3xl font-extrabold text-emerald-600 mt-2 tracking-tight">
                  {formatCurrency(summary.uang_masuk)}
                </h2>
                <div className="flex items-center gap-1.5 mt-3 text-emerald-600 text-xs font-semibold">
                  <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                  Kas masuk / Lunas & Cicilan
                </div>
              </div>

              {/* Card Piutang */}
              <div className="bg-white border border-zinc-200 rounded-2xl p-5 relative overflow-hidden group shadow-sm hover:shadow-md transition-shadow">
                <div className="absolute top-0 right-0 w-24 h-24 bg-amber-50 rounded-full blur-2xl group-hover:bg-amber-100 transition-all duration-300"></div>
                <span className="text-zinc-400 text-xs font-semibold uppercase tracking-wider">Tagihan / Piutang</span>
                <h2 className="text-2xl sm:text-3xl font-extrabold text-amber-600 mt-2 tracking-tight">
                  {formatCurrency(summary.piutang)}
                </h2>
                <div className="flex items-center gap-1.5 mt-3 text-amber-600 text-xs font-semibold">
                  <span className="w-2 h-2 rounded-full bg-amber-500"></span>
                  Total sisa piutang
                </div>
              </div>

              {/* Card Transaksi */}
              <div className="bg-white border border-zinc-200 rounded-2xl p-5 relative overflow-hidden group shadow-sm hover:shadow-md transition-shadow">
                <div className="absolute top-0 right-0 w-24 h-24 bg-violet-50 rounded-full blur-2xl group-hover:bg-violet-100 transition-all duration-300"></div>
                <span className="text-zinc-400 text-xs font-semibold uppercase tracking-wider">Volume Transaksi</span>
                <h2 className="text-2xl sm:text-3xl font-extrabold text-zinc-900 mt-2 tracking-tight">
                  {summary.total_transaksi}
                </h2>
                <div className="flex items-center gap-1.5 mt-3 text-violet-600 text-xs font-semibold">
                  <span className="w-2 h-2 rounded-full bg-violet-500"></span>
                  Transaksi tercatat
                </div>
              </div>
            </div>

            {/* Middle Section: Chart and Statuses */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Timeseries Chart Card */}
              <div className="bg-white border border-zinc-200 rounded-2xl p-5 lg:col-span-2 space-y-4 shadow-sm">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-bold text-base text-zinc-800">Tren Penjualan & Kas</h3>
                    <p className="text-zinc-400 text-xs mt-0.5">Grafik omzet vs uang masuk riil</p>
                  </div>
                  <div className="flex items-center gap-4 text-xs font-medium">
                    <div className="flex items-center gap-1.5">
                      <span className="w-3 h-1.5 rounded bg-indigo-500 block"></span>
                      <span className="text-zinc-600">Omzet</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <span className="w-3 h-1.5 rounded bg-emerald-500 block"></span>
                      <span className="text-zinc-600">Uang Masuk</span>
                    </div>
                  </div>
                </div>

                <div className="pt-2">
                  {timeseries ? renderChart() : (
                    <div className="h-48 flex items-center justify-center text-zinc-400 text-sm">
                      Menyiapkan grafik...
                    </div>
                  )}
                </div>
              </div>

              {/* Status & Top Customers Column */}
              <div className="space-y-6">
                {/* Status breakdown */}
                <div className="bg-white border border-zinc-200 rounded-2xl p-5 shadow-sm">
                  <h3 className="font-bold text-base text-zinc-800 mb-4">Status Transaksi</h3>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between text-sm">
                      <div className="flex items-center gap-2">
                        <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
                        <span className="text-zinc-500 font-medium">Lunas</span>
                      </div>
                      <span className="font-bold text-zinc-800">{summary.status_count.lunas} trx</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <div className="flex items-center gap-2">
                        <span className="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
                        <span className="text-zinc-500 font-medium">Dicicil / DP</span>
                      </div>
                      <span className="font-bold text-zinc-800">{summary.status_count.dicicil} trx</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <div className="flex items-center gap-2">
                        <span className="w-2.5 h-2.5 rounded-full bg-red-500"></span>
                        <span className="text-zinc-500 font-medium">Hutang / Belum Bayar</span>
                      </div>
                      <span className="font-bold text-zinc-800">{summary.status_count.hutang} trx</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <div className="flex items-center gap-2">
                        <span className="w-2.5 h-2.5 rounded-full bg-zinc-400"></span>
                        <span className="text-zinc-500 font-medium">Lainnya</span>
                      </div>
                      <span className="font-bold text-zinc-800">{summary.status_count.lain} trx</span>
                    </div>
                  </div>
                </div>

                {/* Top Customers Card */}
                <div className="bg-white border border-zinc-200 rounded-2xl p-5 shadow-sm">
                  <h3 className="font-bold text-base text-zinc-800 mb-4">Pelanggan Terbesar</h3>
                  <div className="space-y-3">
                    {topCustomers.length === 0 ? (
                      <div className="text-zinc-400 text-xs text-center py-4">Belum ada data pelanggan</div>
                    ) : (
                      topCustomers.map((cust, i) => (
                        <div key={i} className="flex items-center justify-between text-sm border-b border-zinc-100 pb-2 last:border-none last:pb-0">
                          <div>
                            <span className="text-zinc-800 font-semibold block truncate max-w-[120px]">{cust.nama}</span>
                            <span className="text-zinc-400 text-[10px]">{cust.count} transaksi</span>
                          </div>
                          <div className="text-right">
                            <span className="text-zinc-700 font-bold block">{formatCurrency(cust.omzet)}</span>
                            {cust.piutang > 0 && (
                              <span className="text-amber-600 text-[10px] font-semibold">Piutang: {formatCurrency(cust.piutang)}</span>
                            )}
                          </div>
                        </div>
                      ))
                    )}
                  </div>
                </div>
              </div>
            </div>

            {/* Bottom Section: Transactions Table */}
            <div className="bg-white border border-zinc-200 rounded-2xl overflow-hidden shadow-sm">
              <div className="p-5 border-b border-zinc-100 sm:flex sm:items-center sm:justify-between gap-4">
                <div>
                  <h3 className="font-bold text-base text-zinc-800">Daftar Transaksi Terbaru</h3>
                  <p className="text-zinc-400 text-xs mt-0.5">Daftar lengkap transaksi dalam range filter</p>
                </div>
                
                <div className="mt-4 sm:mt-0 relative w-full sm:max-w-xs">
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Cari pelanggan, barang, status..."
                    className="w-full bg-white border border-zinc-200 rounded-xl pl-9 pr-4 py-2 text-sm text-zinc-700 placeholder-zinc-400 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all shadow-sm"
                  />
                  <div className="absolute left-3 top-2.5 text-zinc-400">
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                  </div>
                </div>
              </div>

              {/* Desktop Table View (hidden on mobile) */}
              <div className="hidden md:block overflow-x-auto">
                <table className="w-full text-left border-collapse text-sm">
                  <thead>
                    <tr className="border-b border-zinc-200 bg-zinc-50/50 text-zinc-500 font-semibold">
                      <th className="p-4">Tanggal</th>
                      <th className="p-4">Pelanggan</th>
                      <th className="p-4">Detail Barang</th>
                      <th className="p-4 text-right">Total</th>
                      <th className="p-4 text-right">Uang Masuk</th>
                      <th className="p-4 text-right">Sisa Tagihan</th>
                      <th className="p-4 text-center">Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-zinc-100">
                    {recentTrx.length === 0 ? (
                      <tr>
                        <td colSpan={7} className="p-8 text-center text-zinc-400 text-sm">
                          Tidak ditemukan data transaksi.
                        </td>
                      </tr>
                    ) : (
                      recentTrx.map((trx) => {
                        const statusLower = trx.status?.toLowerCase() || "";
                        const statusBadge = () => {
                          if (statusLower.includes("lunas")) {
                            return <span className="bg-emerald-50 text-emerald-700 border border-emerald-200/60 text-[11px] font-semibold px-2.5 py-0.5 rounded-full shadow-sm">Lunas</span>;
                          } else if (statusLower.includes("cicil") || statusLower.includes("dp")) {
                            return <span className="bg-amber-50 text-amber-700 border border-amber-200/60 text-[11px] font-semibold px-2.5 py-0.5 rounded-full shadow-sm">Dicicil</span>;
                          } else {
                            return <span className="bg-red-50 text-red-700 border border-red-200/60 text-[11px] font-semibold px-2.5 py-0.5 rounded-full shadow-sm">Hutang</span>;
                          }
                        };

                        return (
                          <tr key={trx.id} className="hover:bg-zinc-50/30 transition-colors">
                            <td className="p-4 font-mono text-xs text-zinc-400">{trx.tanggal}</td>
                            <td className="p-4 font-semibold text-zinc-850">{trx.nama_pelanggan}</td>
                            <td className="p-4 text-zinc-600">
                              <span className="font-semibold text-zinc-800">{trx.jumlah_satuan}x</span> {trx.barang}
                              <span className="text-zinc-400 text-xs block font-mono">@{formatCurrency(trx.harga)}</span>
                            </td>
                            <td className="p-4 text-right font-bold text-zinc-900">{formatCurrency(trx.total)}</td>
                            <td className="p-4 text-right text-emerald-600 font-semibold">{formatCurrency(trx.uang_masuk)}</td>
                            <td className="p-4 text-right text-amber-600 font-semibold">{formatCurrency(trx.tagihan)}</td>
                            <td className="p-4 text-center">{statusBadge()}</td>
                          </tr>
                        );
                      })
                    )}
                  </tbody>
                </table>
              </div>

              {/* Mobile Card List View (hidden on desktop) */}
              <div className="block md:hidden divide-y divide-zinc-100">
                {recentTrx.length === 0 ? (
                  <div className="p-8 text-center text-zinc-400 text-sm">
                    Tidak ditemukan data transaksi.
                  </div>
                ) : (
                  recentTrx.map((trx) => {
                    const statusLower = trx.status?.toLowerCase() || "";
                    const statusBadge = () => {
                      if (statusLower.includes("lunas")) {
                        return <span className="bg-emerald-50 text-emerald-700 border border-emerald-200/60 text-[10px] font-semibold px-2 py-0.5 rounded-full">Lunas</span>;
                      } else if (statusLower.includes("cicil") || statusLower.includes("dp")) {
                        return <span className="bg-amber-50 text-amber-700 border border-amber-200/60 text-[10px] font-semibold px-2 py-0.5 rounded-full">Dicicil</span>;
                      } else {
                        return <span className="bg-red-50 text-red-700 border border-red-200/60 text-[10px] font-semibold px-2 py-0.5 rounded-full">Hutang</span>;
                      }
                    };

                    return (
                      <div key={trx.id} className="p-4 space-y-3 active:bg-zinc-50/50 transition-colors">
                        <div className="flex items-center justify-between">
                          <span className="font-mono text-xs text-zinc-400">{trx.tanggal}</span>
                          {statusBadge()}
                        </div>
                        
                        <div>
                          <h4 className="font-bold text-zinc-900 text-sm">{trx.nama_pelanggan}</h4>
                          <p className="text-xs text-zinc-500 mt-0.5">
                            <span className="font-semibold text-zinc-700">{trx.jumlah_satuan}x</span> {trx.barang}
                            <span className="font-mono text-[10px] text-zinc-400 ml-1.5">(@{formatCurrency(trx.harga)})</span>
                          </p>
                        </div>

                        <div className="grid grid-cols-3 gap-2 pt-1.5 border-t border-zinc-50 text-xs">
                          <div>
                            <span className="text-[10px] text-zinc-450 uppercase font-semibold block">Total</span>
                            <span className="font-bold text-zinc-800">{formatCurrency(trx.total)}</span>
                          </div>
                          <div>
                            <span className="text-[10px] text-zinc-450 uppercase font-semibold block">Bayar</span>
                            <span className="font-bold text-emerald-600">{formatCurrency(trx.uang_masuk)}</span>
                          </div>
                          <div className="text-right">
                            <span className="text-[10px] text-zinc-450 uppercase font-semibold block">Tagihan</span>
                            <span className="font-bold text-amber-600">{formatCurrency(trx.tagihan)}</span>
                          </div>
                        </div>
                      </div>
                    );
                  })
                )}
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
