import React, { useState, useEffect } from 'react';

const TaskForm = ({ initialData = {}, onSubmit, onCancel }) => {
    const [formData, setFormData] = useState({
        title: '',
        description: '',
        status: 'pending',
        priority: 'medium',
        tags: '',
        category: '',
        due_date: '',
        start_date: '',
        recurrence_rule: '',
        reminder_at: ''
    });

    useEffect(() => {
        if (initialData && Object.keys(initialData).length > 0) {
            const fmtDate = (d) => d ? new Date(d).toISOString().split('T')[0] : '';
            const fmtDateTime = (d) => d ? new Date(d).toISOString().slice(0, 16) : '';
            setFormData({
                ...initialData,
                tags: initialData.tags ? initialData.tags.replace(/[\[\]"]/g, '') : '',
                due_date: fmtDate(initialData.due_date),
                start_date: fmtDate(initialData.start_date),
                recurrence_rule: initialData.recurrence_rule || '',
                reminder_at: fmtDateTime(initialData.reminder_at),
            });
        }
    }, [initialData]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const submitData = {
            ...formData,
            tags: JSON.stringify(formData.tags.split(',').map(t => t.trim()).filter(Boolean)),
            due_date: formData.due_date ? new Date(formData.due_date).toISOString() : null,
            start_date: formData.start_date ? new Date(formData.start_date).toISOString() : null,
            reminder_at: formData.reminder_at ? new Date(formData.reminder_at).toISOString() : null,
            recurrence_rule: formData.recurrence_rule || null
        };
        onSubmit(submitData);
    };

    return (
        <form onSubmit={handleSubmit} className="bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden">
            <div className="p-8 space-y-8">
                {/* Header Section */}
                <div className="space-y-6">
                    <div>
                        <label className="block text-sm font-semibold text-gray-700 mb-1">Task Title</label>
                        <input
                            required
                            type="text"
                            name="title"
                            value={formData.title}
                            onChange={handleChange}
                            placeholder="e.g., Deploy production build"
                            className="block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-lg py-3 px-4"
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-semibold text-gray-700 mb-1">Description</label>
                        <textarea
                            name="description"
                            rows={4}
                            value={formData.description}
                            onChange={handleChange}
                            placeholder="Describe the task details..."
                            className="block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 py-3 px-4 resize-none"
                        />
                    </div>
                </div>

                <div className="h-px bg-gray-100 w-full" />

                {/* Metadata Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div className="space-y-6">
                        <div>
                            <label className="block text-sm font-semibold text-gray-700 mb-1">Priority</label>
                            <select
                                name="priority"
                                value={formData.priority}
                                onChange={handleChange}
                                className="block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 py-2.5"
                            >
                                <option value="low">Low</option>
                                <option value="medium">Medium</option>
                                <option value="high">High</option>
                                <option value="urgent">Urgent</option>
                            </select>
                        </div>
                        <div>
                            <label className="block text-sm font-semibold text-gray-700 mb-1">Status</label>
                            <select
                                name="status"
                                value={formData.status}
                                onChange={handleChange}
                                className="block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 py-2.5"
                            >
                                <option value="pending">Pending</option>
                                <option value="in_progress">In Progress</option>
                                <option value="completed">Completed</option>
                                <option value="paused">Paused</option>
                            </select>
                        </div>
                    </div>

                    <div className="space-y-6">
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-semibold text-gray-700 mb-1">Start Date</label>
                                <input
                                    type="date"
                                    name="start_date"
                                    value={formData.start_date}
                                    onChange={handleChange}
                                    className="block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 py-2.5"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-semibold text-gray-700 mb-1">Due Date</label>
                                <input
                                    type="date"
                                    name="due_date"
                                    value={formData.due_date}
                                    onChange={handleChange}
                                    className="block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 py-2.5"
                                />
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-semibold text-gray-700 mb-1">Category</label>
                                <input
                                    type="text"
                                    name="category"
                                    placeholder="e.g. Work"
                                    value={formData.category}
                                    onChange={handleChange}
                                    className="block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 py-2.5"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-semibold text-gray-700 mb-1">Tags</label>
                                <input
                                    type="text"
                                    name="tags"
                                    placeholder="top-secret, v1"
                                    value={formData.tags}
                                    onChange={handleChange}
                                    className="block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 py-2.5"
                                />
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-semibold text-gray-700 mb-1">Recurrence</label>
                                <select
                                    name="recurrence_rule"
                                    value={formData.recurrence_rule}
                                    onChange={handleChange}
                                    className="block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 py-2.5"
                                >
                                    <option value="">None</option>
                                    <option value="daily">Daily</option>
                                    <option value="weekly">Weekly</option>
                                    <option value="monthly">Monthly</option>
                                </select>
                            </div>
                            <div>
                                <label className="block text-sm font-semibold text-gray-700 mb-1">Reminder</label>
                                <input
                                    type="datetime-local"
                                    name="reminder_at"
                                    value={formData.reminder_at}
                                    onChange={handleChange}
                                    className="block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 py-2.5"
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Footer Actions */}
            <div className="bg-gray-50 px-8 py-5 flex items-center justify-end space-x-4 border-t border-gray-100">
                <button
                    type="button"
                    onClick={onCancel}
                    className="px-6 py-2.5 border border-gray-300 shadow-sm text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-colors"
                >
                    Cancel
                </button>
                <button
                    type="submit"
                    className="px-6 py-2.5 border border-transparent shadow-sm text-sm font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors shadow-blue-500/30"
                >
                    Save Task
                </button>
            </div>
        </form>
    );
};

export default TaskForm;
