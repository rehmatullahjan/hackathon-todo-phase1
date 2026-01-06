import { useEffect, useRef, useState } from 'react';
import api from '../utils/api';

const NotificationManager = () => {
    const [tasks, setTasks] = useState([]);
    const notifiedRef = useRef(new Set());

    useEffect(() => {
        const fetchTasks = async () => {
            try {
                const response = await api.get('/tasks', { params: { status: 'pending' } });
                setTasks(response.data);
            } catch (error) {
                console.error("NotificationManager failing to fetch:", error);
            }
        };

        fetchTasks();
        const interval = setInterval(fetchTasks, 60000); // Pulse every minute
        return () => clearInterval(interval);
    }, []);

    useEffect(() => {
        // Request permission on mount
        if ('Notification' in window && Notification.permission === 'default') {
            Notification.requestPermission();
        }
    }, []);

    useEffect(() => {
        if (!tasks || !('Notification' in window) || Notification.permission !== 'granted') return;

        const interval = setInterval(() => {
            const now = new Date();

            tasks.forEach(task => {
                if (task.reminder_at && task.status !== 'completed') {
                    const reminderTime = new Date(task.reminder_at);

                    // If reminder time has passed (within the last 10 minutes) 
                    // and we haven't notified for this task yet in this session
                    if (reminderTime <= now &&
                        reminderTime > new Date(now.getTime() - 10 * 60 * 1000) &&
                        !notifiedRef.current.has(task.id)) {

                        new Notification(`Reminder: ${task.title}`, {
                            body: task.description || 'You have a task due!',
                            icon: '/favicon.ico' // Default nextjs favicon
                        });

                        notifiedRef.current.add(task.id);
                    }
                }
            });
        }, 10000); // Check every 10 seconds

        return () => clearInterval(interval);
    }, [tasks]);

    return null; // This is a logic-only component
};

export default NotificationManager;
