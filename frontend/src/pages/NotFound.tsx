// src/pages/Home.tsx
import React from 'react';
import { Outlet } from 'react-router-dom';

const NotFound: React.FC = () => {
    return (
        <div>
            <h1>Not Found</h1>
            <Outlet />
        </div>
    );
};

export default NotFound;