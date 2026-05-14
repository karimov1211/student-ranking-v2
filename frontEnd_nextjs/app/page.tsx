"use client";
import React, { useState, useEffect } from 'react';
import { UserPlus, Database, TrendingUp, Trophy } from 'lucide-react';

export default function Home() {
  const [showModal, setShowModal] = useState(false);
  const [students, setStudents] = useState([]);

  // Haqiqiy loyihada bu ma'lumotlar FastAPI'dan (fetch orqali) olinadi
  // Node.js ulanmagani sababli hozircha UI'ni ko'rsatish uchun "Mock" ma'lumot ishlatamiz
  useEffect(() => {
    setStudents([
      { full_name: "Aziz Karimov", major: "Software Engineering", gpa: 92.5 },
      { full_name: "Malika Ergasheva", major: "Data Science", gpa: 88.0 },
      { full_name: "Jasur Rahimov", major: "Cyber Security", gpa: 75.3 }
    ]);
  }, []);

  return (
    <main className="min-h-screen relative p-8">
      {/* Background Orbs */}
      <div className="fixed inset-0 z-[-1] overflow-hidden pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[50vw] h-[50vw] rounded-full bg-purple-600/20 blur-[100px]" />
        <div className="absolute bottom-[-20%] right-[-10%] w-[60vw] h-[60vw] rounded-full bg-blue-600/20 blur-[100px]" />
      </div>

      <div className="max-w-5xl mx-auto space-y-8">
        {/* Header */}
        <header className="glass-panel rounded-3xl p-6 flex justify-between items-center shadow-lg">
          <div className="flex items-center gap-3">
            <TrendingUp className="text-purple-500 w-8 h-8" />
            <h1 className="text-2xl font-extrabold tracking-tight">Ranking<span className="text-purple-500">System</span> V2</h1>
          </div>
          
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 bg-blue-500/10 text-blue-400 border border-blue-500/20 px-4 py-2 rounded-full text-sm font-semibold">
              <Database className="w-4 h-4" />
              <span>Azure SQL Ulandi</span>
            </div>
            
            <button 
              onClick={() => setShowModal(true)}
              className="flex items-center gap-2 bg-gradient-to-r from-purple-600 to-blue-600 px-5 py-2.5 rounded-xl font-bold text-white hover:scale-105 transition-transform"
            >
              <UserPlus className="w-5 h-5" />
              Yangi Talaba
            </button>
          </div>
        </header>

        {/* Main Content */}
        <div className="glass-panel rounded-3xl p-8">
          <div className="mb-8">
            <h2 className="text-3xl font-bold mb-2">Top Talabalar Reytingi</h2>
            <p className="text-gray-400">Pandas yordamida vaznli GPA hisoblangan (Next.js UI)</p>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b-2 border-white/10 text-gray-400">
                  <th className="pb-4 font-semibold px-4">O'rin</th>
                  <th className="pb-4 font-semibold px-4">F.I.SH</th>
                  <th className="pb-4 font-semibold px-4">Yo'nalish</th>
                  <th className="pb-4 font-semibold px-4">Weighted GPA</th>
                </tr>
              </thead>
              <tbody>
                {students.map((student: any, idx: number) => (
                  <tr key={idx} className="border-b border-white/5 hover:bg-white/5 transition-colors group">
                    <td className="py-4 px-4">
                      <div className={`w-10 h-10 rounded-xl flex items-center justify-center font-bold shadow-lg
                        ${idx === 0 ? 'bg-gradient-to-br from-yellow-400 to-orange-600' : 
                          idx === 1 ? 'bg-gradient-to-br from-gray-300 to-gray-500' : 
                          idx === 2 ? 'bg-gradient-to-br from-amber-700 to-amber-900' : 
                          'bg-white/10'}`}>
                        #{idx + 1}
                      </div>
                    </td>
                    <td className="py-4 px-4 font-bold">{student.full_name}</td>
                    <td className="py-4 px-4 text-gray-300">{student.major}</td>
                    <td className="py-4 px-4">
                      <span className="bg-gradient-to-r from-purple-500 to-blue-500 px-4 py-1.5 rounded-full font-bold shadow-[0_0_15px_rgba(139,92,246,0.3)]">
                        {student.gpa.toFixed(2)}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Modal Form */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
          <div className="glass-panel p-8 rounded-3xl w-[450px] relative">
            <button 
              onClick={() => setShowModal(false)}
              className="absolute top-4 right-4 text-gray-400 hover:text-white"
            >
              ✕
            </button>
            <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
              <UserPlus className="text-purple-500" /> Yangi Talaba
            </h2>
            
            <form className="space-y-4">
              <div>
                <label className="block text-sm text-gray-400 mb-1">F.I.SH</label>
                <input type="text" className="w-full bg-black/30 border border-white/10 rounded-xl px-4 py-3 outline-none focus:border-purple-500 transition-colors" />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-1">Yo'nalish</label>
                <input type="text" className="w-full bg-black/30 border border-white/10 rounded-xl px-4 py-3 outline-none focus:border-purple-500 transition-colors" />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-1">Umumiy Ball</label>
                <input type="number" className="w-full bg-black/30 border border-white/10 rounded-xl px-4 py-3 outline-none focus:border-purple-500 transition-colors" />
              </div>
              
              <button type="button" onClick={() => setShowModal(false)} className="w-full mt-4 bg-gradient-to-r from-purple-600 to-blue-600 py-3 rounded-xl font-bold hover:shadow-[0_0_20px_rgba(139,92,246,0.4)] transition-all">
                Saqlash va Hisoblash
              </button>
            </form>
          </div>
        </div>
      )}
    </main>
  );
}
