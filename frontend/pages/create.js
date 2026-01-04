import React, { useState } from 'react';
import { useRouter } from 'next/router';
import api from '../utils/api';
import TaskForm from '../components/TaskForm';
import Layout from '../components/Layout';

export default function CreateTask() {
    const router = useRouter();
    const [error, setError] = useState('');

    const handleCreate = async (data) => {
        setError('');
        try {
            await api.post('/tasks', data);
            router.push('/');
        } catch (error) {
            console.error("Failed to create task", error);
            const msg = error.response?.data?.detail
                ? JSON.stringify(error.response.data.detail)
                : error.message || "Unknown error";
            setError(`Failed to save task: ${msg}`);
        }
    };

    return (
        <Layout title="Create Task | Hackathon Todo">
            <div className="max-w-2xl mx-auto">
                <div className="mb-8">
                    <h1 className="text-3xl font-extrabold text-gray-900">Create New Task</h1>
                    <p className="text-gray-500 mt-2">Add a new item to your hackathon checklist.</p>
                </div>
                {error && (
                    <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg">
                        {error}
                    </div>
                )}
                <TaskForm
                    onSubmit={handleCreate}
                    onCancel={() => router.push('/')}
                />
            </div>
        </Layout>
    );
}
