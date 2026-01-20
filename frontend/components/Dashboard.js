import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Dashboard = () => {
    const [healthData, setHealthData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchHealthData = async () => {
            try {
                const response = await axios.get('/api/health-data');
                setHealthData(response.data);
            } catch (err) {
                setError('Failed to fetch health data');
            } finally {
                setLoading(false);
            }
        };
        fetchHealthData();
    }, []);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div>
            <h1>User Dashboard</h1>
            {healthData ? (
                <div>
                    <h2>Health Insights</h2>
                    <ul>
                        {healthData.map((data, index) => (
                            <li key={index}>
                                <strong>{data.title}</strong>: {data.value}
                            </li>
                        ))}
                    </ul>
                </div>
            ) : (
                <div>No health data available</div>
            )}
        </div>
    );
};

export default Dashboard;