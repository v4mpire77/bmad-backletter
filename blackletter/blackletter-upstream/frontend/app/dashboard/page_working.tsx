"use client";

import React, { useState, useEffect } from "react";
import { Sun, Moon, Filter } from "lucide-react";

export default function Dashboard() {
  const [darkMode, setDarkMode] = useState(false);
  const [apiHealth, setApiHealth] = useState<'loading' | 'ok' | 'error'>('loading');

  // Check API health
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await fetch('http://localhost:8000/health');
        if (response.ok) {
          setApiHealth('ok');
        } else {
          setApiHealth('error');
        }
      } catch (error) {
        setApiHealth('error');
      }
    };

    checkHealth();
  }, []);

  return (
    <div className={darkMode ? 'min-h-screen bg-gray-900 text-white' : 'min-h-screen bg-gray-50 text-gray-900'}>
      <div className="p-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold">
              Contract Review Dashboard
            </h1>
            <p className="text-gray-600 dark:text-gray-400">
              UK Law Compliance Analysis
            </p>
          </div>
          
          <div className="flex items-center gap-4">
            {/* API Status */}
            <div className={`px-3 py-1 rounded-full text-sm flex items-center gap-2 ${
              apiHealth === 'ok' ? 'bg-green-100 text-green-800' :
              apiHealth === 'error' ? 'bg-red-100 text-red-800' :
              'bg-gray-100 text-gray-800'
            }`}>
              <div className={`w-2 h-2 rounded-full ${
                apiHealth === 'ok' ? 'bg-green-500' :
                apiHealth === 'error' ? 'bg-red-500' :
                'bg-gray-500'
              }`} />
              API: {apiHealth.toUpperCase()}
            </div>

            {/* Dark Mode Toggle */}
            <button
              onClick={() => setDarkMode(!darkMode)}
              className="p-2 rounded-lg border hover:bg-gray-100 dark:hover:bg-gray-800"
            >
              {darkMode ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
            </button>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <div className="flex items-center gap-2 mb-4">
                <Filter className="h-5 w-5" />
                <h2 className="text-lg font-semibold">Filters</h2>
              </div>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Issue Type</label>
                  <select className="w-full p-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600">
                    <option>All</option>
                    <option>GDPR</option>
                    <option>Statute</option>
                    <option>Case Law</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-2">Severity</label>
                  <select className="w-full p-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600">
                    <option>All</option>
                    <option>High</option>
                    <option>Medium</option>
                    <option>Low</option>
                  </select>
                </div>
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3 space-y-6">
            {/* KPIs */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">Documents</h3>
                <p className="text-2xl font-bold">3</p>
              </div>
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">High Risk</h3>
                <p className="text-2xl font-bold text-red-600">1</p>
              </div>
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">Medium Risk</h3>
                <p className="text-2xl font-bold text-yellow-600">1</p>
              </div>
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">Confidence</h3>
                <p className="text-2xl font-bold">85%</p>
              </div>
            </div>

            {/* Issues Table */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
              <div className="p-6 border-b dark:border-gray-700">
                <h2 className="text-lg font-semibold">Issues Found</h2>
                <p className="text-sm text-gray-600 dark:text-gray-400">3 issues detected</p>
              </div>
              
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50 dark:bg-gray-700">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        Document
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        Type
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        Severity
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        Issue
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        Confidence
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                    <tr>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">Service Agreement v2.1.pdf</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded">GDPR</span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="px-2 py-1 text-xs font-medium bg-red-100 text-red-800 rounded">High</span>
                      </td>
                      <td className="px-6 py-4 text-sm">Personal data may be transferred to third countries...</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">92%</td>
                    </tr>
                    <tr>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">Service Agreement v2.1.pdf</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="px-2 py-1 text-xs font-medium bg-purple-100 text-purple-800 rounded">Statute</span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="px-2 py-1 text-xs font-medium bg-yellow-100 text-yellow-800 rounded">Medium</span>
                      </td>
                      <td className="px-6 py-4 text-sm">Limitation of liability clause may not comply...</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">87%</td>
                    </tr>
                    <tr>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">Privacy Policy v1.3.pdf</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded">Case Law</span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="px-2 py-1 text-xs font-medium bg-gray-100 text-gray-800 rounded">Low</span>
                      </td>
                      <td className="px-6 py-4 text-sm">Cookie consent mechanism could be strengthened...</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">76%</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
