import React from 'react';
import Head from 'next/head';
import Link from 'next/link';
import ChatWidget from './ChatWidget';
import NotificationManager from './NotificationManager';


const Layout = ({ children, title = "Hackathon Todo" }) => {
    return (
        <div className="min-h-screen bg-gray-50 font-sans text-gray-900">
            <Head>
                <title>{title}</title>
            </Head>

            <nav className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-10">
                <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between h-16">
                        <div className="flex">
                            <Link href="/" className="flex-shrink-0 flex items-center cursor-pointer group">
                                <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white font-bold mr-2 group-hover:bg-blue-700 transition">
                                    HT
                                </div>
                                <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">
                                    Hackathon Todo
                                </span>
                            </Link>
                        </div>
                        {/* Add more nav items here if needed */}
                    </div>
                </div>
            </nav>

            <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {children}
            </main>
            <ChatWidget />
            <NotificationManager />
        </div>
    );
};

export default Layout;
