import React from 'react';
import Link from 'next/link';

const PriorityBadge = ({ priority }) => {
    const colors = {
        low: 'bg-green-100 text-green-800',
        medium: 'bg-blue-100 text-blue-800',
        high: 'bg-orange-100 text-orange-800',
        urgent: 'bg-red-100 text-red-800',
    };
    return (
        <span className={`px-2.5 py-0.5 rounded-full text-xs font-medium uppercase tracking-wide ${colors[priority] || 'bg-gray-100 text-gray-800'}`}>
            {priority}
        </span>
    );
};

const StatusBadge = ({ status }) => {
    const colors = {
        pending: 'bg-gray-100 text-gray-800',
        in_progress: 'bg-yellow-100 text-yellow-800',
        completed: 'bg-green-100 text-green-800',
        cancelled: 'bg-red-100 text-red-800',
        paused: 'bg-purple-100 text-purple-800',
    };
    return (
        <span className={`px-2.5 py-0.5 rounded-full text-xs font-medium uppercase tracking-wide ${colors[status] || 'bg-gray-100 text-gray-800'}`}>
            {status ? status.replace('_', ' ') : 'unknown'}
        </span>
    );
};

const TaskList = ({ tasks, onDelete, onComplete }) => {
    if (!tasks || !tasks.length) {
        return (
            <div className="text-center py-20 bg-white rounded-xl border border-dashed border-gray-300">
                <p className="text-gray-500 text-lg">No tasks found matching your criteria.</p>
                <p className="text-gray-400 text-sm mt-2">Try adjusting filters or create a new task.</p>
            </div>
        );
    }

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {tasks.map((task) => (
                <div key={task.id} className="group bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-all duration-200 flex flex-col overflow-hidden relative">
                    {/* Top Border for Priority */}
                    <div className={`h-1 w-full ${task.priority === 'urgent' ? 'bg-red-500' :
                            task.priority === 'high' ? 'bg-orange-400' :
                                task.priority === 'medium' ? 'bg-blue-400' : 'bg-green-400'
                        }`}></div>

                    <div className="p-5 flex-grow">
                        <div className="flex justify-between items-start mb-3">
                            <PriorityBadge priority={task.priority} />
                            {task.due_date && (
                                <span className="text-xs text-gray-500 font-medium bg-gray-50 px-2 py-1 rounded">
                                    Due {new Date(task.due_date).toLocaleDateString()}
                                </span>
                            )}
                        </div>

                        <h3 className={`text-lg font-bold text-gray-900 mb-2 truncate ${task.status === 'completed' ? 'line-through text-gray-500' : ''}`}>
                            {task.title}
                        </h3>

                        <p className="text-gray-600 text-sm mb-4 line-clamp-3 h-14">
                            {task.description || "No description provided."}
                        </p>

                        <div className="flex flex-wrap gap-2 mb-4">
                            {task.category && (
                                <span className="text-xs bg-indigo-50 text-indigo-700 px-2 py-1 rounded border border-indigo-100">
                                    {task.category}
                                </span>
                            )}
                            {task.tags && (
                                // Handle potential JSON string or array, safely
                                Array.isArray(task.tags) ? task.tags :
                                    (task.tags.startsWith('[') ? JSON.parse(task.tags) : [])
                            ).map((tag, idx) => (
                                <span key={idx} className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded border border-gray-200">
                                    #{tag}
                                </span>
                            ))}
                        </div>
                    </div>

                    <div className="bg-gray-50 px-5 py-3 border-t border-gray-100 flex justify-between items-center bg-white/50">
                        <StatusBadge status={task.status} />

                        <div className="flex gap-2">
                            {task.status !== 'completed' && (
                                <button
                                    onClick={() => onComplete(task.id)}
                                    className="p-1.5 text-green-600 hover:bg-green-50 rounded-lg transition-colors"
                                    title="Complete"
                                >
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
                                </button>
                            )}
                            <button
                                onClick={() => onDelete(task.id)}
                                className="p-1.5 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                                title="Delete"
                            >
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                            </button>
                            <Link href={`/tasks/${task.id}`}>
                                <span className="p-1.5 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors cursor-pointer inline-block">
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path></svg>
                                </span>
                            </Link>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default TaskList;
