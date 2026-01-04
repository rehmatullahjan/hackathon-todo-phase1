import React, { useState, useEffect, useCallback } from 'react';
import Link from 'next/link';
import api from '../utils/api';
import TaskList from '../components/TaskList';
import TaskFilters from '../components/TaskFilters';
import Layout from '../components/Layout';
import { PlusIcon } from '@heroicons/react/24/solid';

const PlusIconSimple = () => (
    <svg className="w-5 h-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
        <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
    </svg>
);

export default function Home() {
    const [tasks, setTasks] = useState([]);
    const [filters, setFilters] = useState({
        status: '',
        priority: '',
        sort_by: 'created_at',
        sort_order: 'desc'
    });
    const [searchQuery, setSearchQuery] = useState('');
    const [loading, setLoading] = useState(true);

    const fetchTasks = useCallback(async () => {
        try {
            setLoading(true);
            let params = { ...filters };

            // Remove empty filters
            Object.keys(params).forEach(key => {
                if (!params[key]) delete params[key];
            });

            let response;
            if (searchQuery) {
                // Use search endpoint if query exists
                response = await api.get('/search', { params: { query: searchQuery } });
            } else {
                // Use list endpoint
                response = await api.get('/tasks', { params });
            }

            setTasks(response.data);
        } catch (error) {
            console.error("Failed to fetch tasks", error);
        } finally {
            setLoading(false);
        }
    }, [filters, searchQuery]);

    // Debounce search/filter fetch
    useEffect(() => {
        const timer = setTimeout(() => {
            fetchTasks();
        }, 300);
        return () => clearTimeout(timer);
    }, [fetchTasks]);

    const handleDelete = async (id) => {
        console.log("Attempting to delete task:", id);
        // if (!confirm("Are you sure?")) return; // Temporarily removed to ensure click works
        try {
            await api.delete(`/tasks/${id}`);
            console.log("Delete successful, refreshing list...");
            await fetchTasks();
        } catch (error) {
            console.error("Failed to delete task:", error);
            alert(`Failed to delete task: ${error.message}`);
        }
    };

    const handleComplete = async (id) => {
        try {
            await api.post(`/tasks/${id}/complete`);
            fetchTasks();
        } catch (error) {
            alert("Failed to complete task");
        }
    };

    return (
        <Layout title="Dashboard | Hackathon Todo">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
                <div>
                    <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">Tasks</h1>
                    <p className="text-gray-500 mt-1">Manage your hackathon deliverables.</p>
                </div>
                <Link href="/create" className="no-underline">
                    <span className="inline-flex items-center px-5 py-3 border border-transparent text-base font-medium rounded-xl shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all transform hover:scale-105 cursor-pointer">
                        <PlusIconSimple />
                        New Task
                    </span>
                </Link>
            </div>

            <TaskFilters
                filters={filters}
                onChange={setFilters}
                onSearch={setSearchQuery}
            />

            {loading ? (
                <div className="flex justify-center items-center py-20">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                </div>
            ) : (
                <TaskList
                    tasks={tasks}
                    onDelete={handleDelete}
                    onComplete={handleComplete}
                />
            )}
        </Layout>
    );
}
