// src/pages/Dashboard.tsx
import React from 'react';
import { Outlet } from 'react-router-dom';

const Dashboard: React.FC = () => {
    return (
        <div>
            <h1>Dashboard</h1>
            <Outlet />
        </div>
    );
};

export default Dashboard;