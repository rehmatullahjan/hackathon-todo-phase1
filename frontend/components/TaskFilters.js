import React from 'react';
import { MagnifyingGlassIcon, FunnelIcon } from '@heroicons/react/24/outline'; // Assuming heroicons install or just use SVG

// Simple SVG icons to avoid dependency if not installed
const SearchIcon = () => (
  <svg className="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
    <path fillRule="evenodd" d="M9 3.5a5.5 5.5 0 100 11 5.5 5.5 0 000-11zM2 9a7 7 0 1112.452 4.391l3.328 3.329a.75.75 0 11-1.06 1.06l-3.329-3.328A7 7 0 012 9z" clipRule="evenodd" />
  </svg>
);

const TaskFilters = ({ filters, onChange, onSearch }) => {
  const handleChange = (e) => {
    const { name, value } = e.target;
    onChange({ ...filters, [name]: value });
  };

  return (
    <div className="bg-white p-5 rounded-xl shadow-sm border border-gray-200 mb-8 transition-all hover:shadow-md">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">

        {/* Search */}
        <div className="md:col-span-4 lg:col-span-1">
          <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Search</label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <SearchIcon />
            </div>
            <input
              type="text"
              placeholder="Search tasks..."
              className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg leading-5 bg-gray-50 placeholder-gray-400 focus:outline-none focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-150 ease-in-out sm:text-sm"
              onChange={(e) => onSearch(e.target.value)}
            />
          </div>
        </div>

        {/* Filters Wrapper */}
        <div className="md:col-span-4 lg:col-span-3 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
          {/* Status Filter */}
          <div>
            <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Status</label>
            <select
              name="status"
              value={filters.status || ''}
              onChange={handleChange}
              className="block w-full py-2 px-3 border border-gray-300 bg-white rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            >
              <option value="">All Statuses</option>
              <option value="pending">Pending</option>
              <option value="in_progress">In Progress</option>
              <option value="completed">Completed</option>
              <option value="cancelled">Cancelled</option>
              <option value="paused">Paused</option>
            </select>
          </div>

          {/* Priority Filter */}
          <div>
            <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Priority</label>
            <select
              name="priority"
              value={filters.priority || ''}
              onChange={handleChange}
              className="block w-full py-2 px-3 border border-gray-300 bg-white rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            >
              <option value="">All Priorities</option>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="urgent">Urgent</option>
            </select>
          </div>

          {/* Category Filter */}
          <div>
            <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Category</label>
            <input
              type="text"
              name="category"
              placeholder="Filter by category..."
              value={filters.category || ''}
              onChange={handleChange}
              className="block w-full py-2 px-3 border border-gray-300 bg-white rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
          </div>

          {/* Tag Filter */}
          <div>
            <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Tag</label>
            <input
              type="text"
              name="tags"
              placeholder="Filter by tag..."
              value={filters.tags || ''}
              onChange={handleChange}
              className="block w-full py-2 px-3 border border-gray-300 bg-white rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
          </div>


          {/* Sort By */}
          <div className="flex items-end gap-2">
            <div className="flex-grow">
              <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Sort</label>
              <select
                name="sort_by"
                value={filters.sort_by || ''}
                onChange={handleChange}
                className="block w-full py-2 px-3 border border-gray-300 bg-white rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              >
                <option value="created_at">Created Date</option>
                <option value="priority">Priority</option>
                <option value="title">Title</option>
                <option value="due_date">Due Date</option>
              </select>
            </div>
            <button
              onClick={() => onChange({})}
              className="mb-[1px] px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-600 rounded-lg text-sm font-medium transition-colors"
              title="Clear Filters"
            >
              Clear
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TaskFilters;
