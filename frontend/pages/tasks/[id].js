import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import api from '../../utils/api';
import TaskForm from '../../components/TaskForm';
import Link from 'next/link';

export default function TaskDetails() {
    const router = useRouter();
    const { id } = router.query;
    const [task, setTask] = useState(null);
    const [loading, setLoading] = useState(true);
    const [isEditing, setIsEditing] = useState(false);

    useEffect(() => {
        if (!id) return;
        const fetchTask = async () => {
            try {
                const res = await api.get(`/tasks/${id}`);
                setTask(res.data);
            } catch (error) {
                alert("Task not found");
                router.push('/');
            } finally {
                setLoading(false);
            }
        };
        fetchTask();
    }, [id, router]);

    const handleUpdate = async (data) => {
        try {
            const res = await api.patch(`/tasks/${id}`, data);
            setTask(res.data);
            setIsEditing(false);
        } catch (error) {
            alert("Failed to update task");
        }
    };

    if (loading) return <div className="p-8">Loading...</div>;
    if (!task) return null;

    return (
        <div className="min-h-screen bg-gray-100 p-8">
            <div className="max-w-2xl mx-auto">
                <div className="mb-6 flex justify-between items-center">
                    <Link href="/">
                        <span className="text-blue-600 hover:underline cursor-pointer">&larr; Back to Dashboard</span>
                    </Link>
                    {!isEditing && (
                        <button
                            onClick={() => setIsEditing(true)}
                            className="bg-indigo-600 text-white px-4 py-2 rounded"
                        >
                            Edit Task
                        </button>
                    )}
                </div>

                {isEditing ? (
                    <div className="bg-white p-6 rounded shadow">
                        <h1 className="text-2xl font-bold mb-4">Edit Task</h1>
                        <TaskForm
                            initialData={task}
                            onSubmit={handleUpdate}
                            onCancel={() => setIsEditing(false)}
                        />
                    </div>
                ) : (
                    <div className="bg-white p-6 rounded shadow space-y-4">
                        <div className="border-b pb-4">
                            <h1 className="text-3xl font-bold text-gray-900">{task.title}</h1>
                            <div className="flex space-x-2 mt-2">
                                <span className="px-2 bg-blue-100 text-blue-800 rounded text-sm">{task.status}</span>
                                <span className="px-2 bg-purple-100 text-purple-800 rounded text-sm">{task.priority}</span>
                                {task.category && <span className="px-2 bg-gray-100 text-gray-800 rounded text-sm">{task.category}</span>}
                            </div>
                        </div>

                        {task.description && (
                            <div>
                                <h3 className="text-sm font-medium text-gray-500">Description</h3>
                                <p className="mt-1 text-gray-900 whitespace-pre-wrap">{task.description}</p>
                            </div>
                        )}

                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <h3 className="text-sm font-medium text-gray-500">Due Date</h3>
                                <p>{task.due_date ? new Date(task.due_date).toLocaleDateString() : 'None'}</p>
                            </div>
                            <div>
                                <h3 className="text-sm font-medium text-gray-500">Start Date</h3>
                                <p>{task.start_date ? new Date(task.start_date).toLocaleDateString() : 'None'}</p>
                            </div>
                            <div>
                                <h3 className="text-sm font-medium text-gray-500">Created At</h3>
                                <p>{new Date(task.created_at).toLocaleString()}</p>
                            </div>
                            <div>
                                <h3 className="text-sm font-medium text-gray-500">Tags</h3>
                                <p>{task.tags && task.tags !== "[]" ? task.tags.replace(/[\[\]"]/g, '') : 'None'}</p>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
