"use client";

import { useState, useEffect } from "react";
import { getOrgSettings, updateOrgSettings } from "@/lib/api";

export default function SettingsPage() {
  const [settings, setSettings] = useState({
    llm_provider: "none",
    ocr_enabled: false,
    retention_days: 30,
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchSettings() {
      try {
        const data = await getOrgSettings();
        setSettings(data);
      } catch (err) {
        setError("Failed to load settings");
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    fetchSettings();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    const checked = (e.target as HTMLInputElement).checked;
    setSettings(prev => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError(null);
    try {
      await updateOrgSettings(settings);
      alert("Settings updated successfully");
    } catch (err) {
      setError("Failed to update settings");
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Organization Settings</h1>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-medium mb-2">
            LLM Provider
          </label>
          <select
            name="llm_provider"
            value={settings.llm_provider}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          >
            <option value="none">None</option>
            <option value="default">Default</option>
          </select>
          <p className="text-xs text-gray-500 mt-1">
            Controls LLM usage for advanced analysis features.
          </p>
        </div>

        <div>
          <label className="flex items-center">
            <input
              type="checkbox"
              name="ocr_enabled"
              checked={settings.ocr_enabled}
              onChange={handleChange}
              className="mr-2"
            />
            <span className="text-sm font-medium">Enable OCR</span>
          </label>
          <p className="text-xs text-gray-500 mt-1">
            Enable optical character recognition for image-based documents.
          </p>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">
            Data Retention (Days)
          </label>
          <input
            type="number"
            name="retention_days"
            value={settings.retention_days}
            onChange={handleChange}
            min="1"
            className="w-full p-2 border rounded"
          />
          <p className="text-xs text-gray-500 mt-1">
            Number of days to retain analysis data.
          </p>
        </div>

        <div>
          <button
            type="submit"
            disabled={saving}
            className="bg-black text-white px-4 py-2 rounded disabled:opacity-50"
          >
            {saving ? "Saving..." : "Save Settings"}
          </button>
        </div>
      </form>
    </div>
  );
}