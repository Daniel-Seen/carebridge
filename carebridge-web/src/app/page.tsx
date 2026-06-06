"use client";

import { useState, useEffect } from "react";
import { apiGet } from "@/lib/api";

interface Elder {
  id: number;
  name: string;
  room: string;
  avatar: string;
  birth_date: string;
  notes: string;
  status: string;
}

interface Update {
  id: number;
  elder_id: number;
  elder_name: string;
  avatar: string;
  content: string;
  mood: string;
  activity: string;
  meal_summary: string;
  created_at: string;
}

const moodMap: Record<string, string> = {
  happy: "😊",
  calm: "😌",
  tired: "😴",
  unwell: "🤒",
  other: "😐",
};

export default function Dashboard() {
  const [elders, setElders] = useState<Elder[]>([]);
  const [updates, setUpdates] = useState<Update[]>([]);
  const [selectedElder, setSelectedElder] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [elderData, updateData] = await Promise.all([
          apiGet<Elder[]>("/api/elders"),
          apiGet<Update[]>("/api/updates/institution/1"),
        ]);
        setElders(elderData);
        setUpdates(updateData);
      } catch (e) {
        console.error("Failed to load data:", e);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const selectedElderUpdates = selectedElder
    ? updates.filter((u) => u.elder_id === selectedElder)
    : updates;

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto p-6 text-center text-gray-400 mt-20">
        <span className="text-4xl animate-pulse">🏥</span>
        <p className="mt-4">正在连接阳光养老院...</p>
      </div>
    );
  }

  return (
    <main className="max-w-4xl mx-auto p-4 md:p-6">
      {/* Elder Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
        {elders.map((elder) => (
          <button
            key={elder.id}
            onClick={() => setSelectedElder(selectedElder === elder.id ? null : elder.id)}
            className={`p-4 rounded-xl text-left transition-all ${
              selectedElder === elder.id
                ? "bg-sky-100 border-2 border-sky-400 shadow-md"
                : "bg-white border border-gray-100 shadow-sm hover:shadow-md"
            }`}
          >
            <div className="text-3xl mb-2">{elder.avatar || "👴"}</div>
            <h3 className="font-semibold text-gray-800 text-sm">{elder.name}</h3>
            <p className="text-xs text-gray-400">{elder.room}室</p>
            {elder.notes && (
              <p className="text-xs text-gray-400 mt-1 truncate">{elder.notes}</p>
            )}
          </button>
        ))}
      </div>

      {/* Daily Updates Feed */}
      <div className="space-y-3">
        <h2 className="text-lg font-bold text-gray-700 flex items-center gap-2">
          📋 {selectedElder ? `${elders.find((e) => e.id === selectedElder)?.name}的动态` : "今日动态"}
        </h2>

        {selectedElderUpdates.length === 0 && (
          <div className="text-center py-12 text-gray-400">
            <span className="text-4xl">📝</span>
            <p className="mt-2">暂无动态记录</p>
          </div>
        )}

        {selectedElderUpdates.map((update) => (
          <div
            key={update.id}
            className="bg-white rounded-xl p-4 shadow-sm border border-gray-100 hover:shadow-md transition-shadow"
          >
            <div className="flex items-start gap-3">
              <span className="text-2xl">{moodMap[update.mood] || "😐"}</span>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-semibold text-gray-800 text-sm">
                    {update.elder_name}
                  </span>
                  <span className="text-xs text-gray-400">
                    {update.created_at?.slice(0, 16)?.replace("T", " ")}
                  </span>
                </div>
                <p className="text-gray-600 text-sm leading-relaxed">{update.content}</p>

                {(update.activity || update.meal_summary) && (
                  <div className="mt-2 flex flex-wrap gap-2">
                    {update.activity && (
                      <span className="inline-flex items-center gap-1 text-xs px-2 py-1 rounded-full bg-purple-50 text-purple-600">
                        🎯 {update.activity}
                      </span>
                    )}
                    {update.meal_summary && (
                      <span className="inline-flex items-center gap-1 text-xs px-2 py-1 rounded-full bg-orange-50 text-orange-600">
                        🍽️ {update.meal_summary}
                      </span>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}
